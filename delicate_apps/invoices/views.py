from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Invoice
from .serializers import InvoiceSerializer, InvoiceDetailSerializer

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
    serializer = InvoiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update an existing invoice
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_invoice_by_id(request, id):
    try:
        invoice = get_object_or_404(Invoice, pk=id)
        serializer = InvoiceSerializer(invoice, data=request.data)
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
