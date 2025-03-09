"""
API views for invoice management and CSV export functionality.
"""

import pandas as pd
import io 
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from datetime import datetime
from django.http import HttpResponse
from .models import Invoice, InvoiceItem
from .serializers import InvoiceSerializer, InvoiceDetailSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_invoice_to_csv(request, id):
    """
    Export a single invoice and its details to CSV format.
    
    Available to authenticated users via API.
    """
    if request.user.is_authenticated:
        try:
            invoice = get_object_or_404(Invoice, pk=id)
            
            # Create a DataFrame for the invoice details
            items = invoice.items.all()
            items_data = []
            
            for item in items:
                items_data.append({
                    'Producto': item.product.name if item.product and hasattr(item.product, 'name') else 'N/A',
                    'Cantidad': item.quantity,
                    'Precio_Unitario': item.price,
                    'Subtotal': float(item.get_total()),
                    'IVA': float(item.get_iva_amount()),
                    'Total_con_IVA': float(item.get_total_with_iva())
                })
            
            # Get invoice data with better error handling
            company_name = invoice.fk_company.name if invoice.fk_company and hasattr(invoice.fk_company, 'name') else 'N/A'
            
            # Use name field for user instead of first_name/last_name
            if invoice.fk_user and hasattr(invoice.fk_user, 'name'):
                user_name = invoice.fk_user.name
            elif invoice.fk_user and hasattr(invoice.fk_user, 'email'):
                # If no name available, use email as alternative
                user_name = invoice.fk_user.email
            else:
                user_name = 'N/A'
            
            # Handle type name safely
            if invoice.fk_type and hasattr(invoice.fk_type, 'name'):
                type_name = invoice.fk_type.name
            else:
                type_name = 'N/A'
            
            # Create CSV content manually for better control
            buffer = io.StringIO()
            
            # Write header for the invoice
            buffer.write("DATOS DE FACTURA\n")  
            buffer.write("ID,Fecha,Tipo,Forma_de_Pago,Empresa,Usuario,Total_Neto,IVA_Total,Total\n")
            
            # Write header for items
            buffer.write(f"{invoice.id},{invoice.date},{type_name},{invoice.payment_form},{company_name},{user_name},{invoice.neto},{float(invoice.get_iva_amount())},{float(invoice.get_total())}\n\n")
            
            # Escribir encabezado para los items
            buffer.write("DETALLES DE FACTURA\n")
            buffer.write("Producto,Cantidad,Precio_Unitario,Subtotal,IVA,Total_con_IVA\n")
            
            # Write item data
            for item in items:
                product_name = item.product.name if item.product and hasattr(item.product, 'name') else 'N/A'
                quantity = item.quantity
                price = item.price
                subtotal = float(item.get_total())
                iva = float(item.get_iva_amount())
                total_with_iva = float(item.get_total_with_iva())
                
                buffer.write(f"{product_name},{quantity},{price},{subtotal},{iva},{total_with_iva}\n")
            
            # Create response
            filename = f"factura_{invoice.id}_{datetime.now().strftime('%Y%m%d')}.csv"
            response = HttpResponse(buffer.getvalue(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            return response
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            return HttpResponse(f"Error al exportar la factura: {str(e)}<br><pre>{error_details}</pre>", status=400, content_type='text/html')
    else:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED
        )

@staff_member_required
def admin_export_invoice_to_csv(request, id):
    """
    Export invoice to CSV from the admin panel.
    
    Only available to staff members.
    """
    try:
        invoice = get_object_or_404(Invoice, pk=id)
        
        # Get invoice items
        items = invoice.items.all()
        items_data = []
        
        for item in items:
            items_data.append({
                'Producto': item.product.name if item.product and hasattr(item.product, 'name') else 'N/A',
                'Cantidad': item.quantity,
                'Precio_Unitario': item.price,
                'Subtotal': float(item.get_total()),
                'IVA': float(item.get_iva_amount()),
                'Total_con_IVA': float(item.get_total_with_iva())
            })
        
        # Get invoice data safely
        company_name = invoice.fk_company.name if invoice.fk_company and hasattr(invoice.fk_company, 'name') else 'N/A'
        
        # Get user information safely
        if invoice.fk_user and hasattr(invoice.fk_user, 'name'):
            user_name = invoice.fk_user.name
        elif invoice.fk_user and hasattr(invoice.fk_user, 'email'):
            user_name = invoice.fk_user.email
        else:
            user_name = 'N/A'
        
        # Get type information safely
        if invoice.fk_type and hasattr(invoice.fk_type, 'name'):
            type_name = invoice.fk_type.name
        else:
            type_name = 'N/A'
        
        # Create CSV manually
        buffer = io.StringIO()
        
        # Write invoice header
        buffer.write("DATOS DE FACTURA\n")
        buffer.write("ID,Fecha,Tipo,Forma_de_Pago,Empresa,Usuario,Total_Neto,IVA_Total,Total\n")
        
        # Write invoice data
        buffer.write(f"{invoice.id},{invoice.date},{type_name},{invoice.payment_form},{company_name},{user_name},{invoice.neto},{float(invoice.get_iva_amount())},{float(invoice.get_total())}\n\n")
        
        # Write items header
        buffer.write("DETALLES DE FACTURA\n")
        buffer.write("Producto,Cantidad,Precio_Unitario,Subtotal,IVA,Total_con_IVA\n")
        
        # Write item data
        for item in items:
            product_name = item.product.name if item.product and hasattr(item.product, 'name') else 'N/A'
            quantity = item.quantity
            price = item.price
            subtotal = float(item.get_total())
            iva = float(item.get_iva_amount())
            total_with_iva = float(item.get_total_with_iva())
            
            buffer.write(f"{product_name},{quantity},{price},{subtotal},{iva},{total_with_iva}\n")
        
        # Prepare response
        filename = f"factura_{invoice.id}_{datetime.now().strftime('%Y%m%d')}.csv"
        response = HttpResponse(buffer.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return HttpResponse(f"Error al exportar la factura: {str(e)}<br><pre>{error_details}</pre>", status=400, content_type='text/html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_invoices(request):
    """Get all invoices with optional filtering."""
    # Filter parameters
    type_id = request.query_params.get('type_id', None)
    company_id = request.query_params.get('company_id', None)
    user_id = request.query_params.get('user_id', None)
    
    # Base query
    invoices = Invoice.objects.all()
    
    # Apply filters if present
    if type_id:
        invoices = invoices.filter(fk_type=type_id)
    if company_id:
        invoices = invoices.filter(fk_company=company_id)
    if user_id:
        invoices = invoices.filter(fk_user=user_id)
        
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_invoice_by_id(request, id):
    """Get a specific invoice by ID with all details."""
    try:
        invoice = get_object_or_404(Invoice, pk=id)
        serializer = InvoiceDetailSerializer(invoice)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {"error": f"Error obtaining the invoice: {str(e)}"},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_invoice(request):
    """Create a new invoice with optional items."""
    with transaction.atomic():
        try:
            # Create invoice
            invoice_data = {
                'date': request.data.get('date'),
                'payment_form': request.data.get('payment_form'),
                'neto': request.data.get('neto'),
                'fk_type_id': request.data.get('fk_type'),
                'fk_user_id': request.data.get('fk_user'),
                'fk_company_id': request.data.get('fk_company')
            }
            
            invoice_serializer = InvoiceSerializer(data=invoice_data)
            if not invoice_serializer.is_valid():
                return Response(invoice_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            invoice = invoice_serializer.save()
            
            # Create invoice items if provided
            items_data = request.data.get('items', [])
            for item_data in items_data:
                item_data['invoice'] = invoice.id
                InvoiceItem.objects.create(
                    invoice=invoice,
                    product_id=item_data.get('product'),
                    quantity=item_data.get('quantity'),
                    price=item_data.get('price')
                )
            
            # Return the created invoice with details
            return Response(
                InvoiceDetailSerializer(invoice).data, 
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": f"Error creating invoice: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_invoice_by_id(request, id):
    """Update an existing invoice."""
    try:
        invoice = get_object_or_404(Invoice, pk=id)
        serializer = InvoiceSerializer(invoice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"error": f"Error updating the invoice: {str(e)}"},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_invoice_by_id(request, id):
    """Delete an invoice."""
    try:
        invoice = get_object_or_404(Invoice, pk=id)
        invoice.delete()
        return Response(
            {"message": "Invoice successfully deleted"},
            status=status.HTTP_204_NO_CONTENT
        )
    except Exception as e:
        return Response(
            {"error": f"Error deleting the invoice: {str(e)}"},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_invoices_by_type(request, type_id):
    """Get all invoices for a specific business type."""
    invoices = Invoice.objects.filter(fk_type=type_id)
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_invoices_by_company(request, company_id):
    """Get all invoices for a specific company."""
    invoices = Invoice.objects.filter(fk_company=company_id)
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_invoices_by_user(request, user_id):
    """Get all invoices for a specific user."""
    invoices = Invoice.objects.filter(fk_user=user_id)
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data)