import pandas as pd
import io
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Invoice, InvoiceItem
from .serializers import InvoiceSerializer, InvoiceDetailSerializer
from datetime import datetime
from django.http import HttpResponse


# Obtain all invoices with optional filtering
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_invoices(request):
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

# Obtain an invoice by ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_invoice_by_id(request, id):
    try:
        invoice = get_object_or_404(Invoice, pk=id)
        serializer = InvoiceDetailSerializer(invoice)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {"error": f"Error obtaining the invoice: {str(e)}"},
            status=status.HTTP_404_NOT_FOUND
        )

# Create a new invoice
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_invoice(request):
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

# Update an existing invoice
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_invoice_by_id(request, id):
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

# Delete an invoice
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_invoice_by_id(request, id):
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

# Get invoices by type
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_invoices_by_type(request, type_id):
    invoices = Invoice.objects.filter(fk_type=type_id)
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data)

# Get invoices by company
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_invoices_by_company(request, company_id):
    invoices = Invoice.objects.filter(fk_company=company_id)
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data)

# Get invoices by user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_invoices_by_user(request, user_id):
    invoices = Invoice.objects.filter(fk_user=user_id)
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data)

# Export an invoice and its details to CSV format
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_invoice_to_csv(request, id):
    """Export a single invoice and its details to CSV format"""
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
        
        # Create DataFrame for invoice header with better error handling
        company_name = invoice.fk_company.name if invoice.fk_company and hasattr(invoice.fk_company, 'name') else 'N/A'
        
        # Usar el campo name para el usuario en lugar de first_name/last_name
        if invoice.fk_user and hasattr(invoice.fk_user, 'name'):
            user_name = invoice.fk_user.name
        elif invoice.fk_user and hasattr(invoice.fk_user, 'email'):
            # Si no hay nombre disponible, usar el email como alternativa
            user_name = invoice.fk_user.email
        else:
            user_name = 'N/A'
        
        # Handle type name safely
        if invoice.fk_type and hasattr(invoice.fk_type, 'name'):
            type_name = invoice.fk_type.name
        else:
            type_name = 'N/A'
        
        # Crear el contenido CSV manualmente para mayor control
        buffer = io.StringIO()
        
        # Escribir encabezado para la factura
        buffer.write("DATOS DE FACTURA\n")  # Quitamos el # para evitar que se interprete como comentario
        buffer.write("ID,Fecha,Tipo,Forma_de_Pago,Empresa,Usuario,Total_Neto,IVA_Total,Total\n")
        
        # Escribir datos de la factura
        buffer.write(f"{invoice.id},{invoice.date},{type_name},{invoice.payment_form},{company_name},{user_name},{invoice.neto},{float(invoice.get_iva_amount())},{float(invoice.get_total())}\n\n")
        
        # Escribir encabezado para los items
        buffer.write("DETALLES DE FACTURA\n")
        buffer.write("Producto,Cantidad,Precio_Unitario,Subtotal,IVA,Total_con_IVA\n")
        
        # Escribir datos de los items
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