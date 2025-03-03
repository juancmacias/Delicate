from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import BasketTemp
from delicate_apps.invoices.models import Invoice, InvoiceItem
from delicate_apps.store.models import StoreProduct
from .serializers import BasketTempSerializer, BasketTempDetailSerializer
from django.utils import timezone
from django.db import transaction

# Obtain all basket items with optional filtering
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_basket_items(request):
    # Filter parameters
    user_id = request.query_params.get('user_id', None)
    
    # Base query
    items = BasketTemp.objects.all()
    
    # Apply filters if present
    if user_id:
        items = items.filter(user_id=user_id)
        
    serializer = BasketTempSerializer(items, many=True)
    return Response(serializer.data)

# Obtain a basket item by ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_basket_item_by_id(request, id):
    try:
        item = get_object_or_404(BasketTemp, pk=id)
        serializer = BasketTempDetailSerializer(item)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {"error": f"Error al obtener el artículo de la cesta: {str(e)}"},
            status=status.HTTP_404_NOT_FOUND
        )


# Add products to the basket
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_basket(request):
    user_id = request.data.get('user_id')
    product_id = request.data.get('product_id')
    try:
        quantity = int(request.data.get('quantity', 1))
        if quantity <= 0:
            return Response({"error": "La cantidad debe ser un número positivo"}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({"error": "Cantidad no válida"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Verify if the product exists
    product = get_object_or_404(StoreProduct, pk=product_id)
    
    # Verify if the product exists in the basket
    existing_item = BasketTemp.objects.filter(user_id=user_id, product_id=product_id).first()
    
    # Calculate the price based on the product's price
    price = product.get_total_price()

    if existing_item:
        # If exists, update the quantity
        existing_item.quantity += quantity
        existing_item.save()
        serializer = BasketTempSerializer(existing_item)
        return Response({
            "message": "Producto actualizado en la cesta",  
            "item": serializer.data
        })
    else:
        # If not exists, create a new item
        data = {
            'user_id': user_id,
            'product_id': product_id,
            'quantity': quantity,
            'price': product.get_total_price(),
            'temp_date': timezone.now()
        }
        serializer = BasketTempSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Producto añadido a la cesta", 
                "item": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create invoice with  basket items
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request, user_id):
    """Create invoice with basket items"""
    with transaction.atomic():
        # Obtain all the items in the basket of the user
        basket_items = BasketTemp.objects.filter(user_id=user_id)
        
        if not basket_items.exists():
            return Response(
                {"error": "La cesta está vacía"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Total calculation (price already includes VAT)
        total_amount = sum(item.get_total() for item in basket_items)
        
        # Obtain the data from the request
        payment_form = request.data.get('payment_form', 'Efectivo')
        company_id = request.data.get('company_id')
        type_id = request.data.get('type_id')
        
        # Create a new invoice
        invoice = Invoice.objects.create(
            date=timezone.now().date(),
            payment_form=payment_form,
            neto=total_amount,
            fk_user_id=user_id,
            fk_company_id=company_id,
            fk_type_id=type_id
        )
        
        # Create invoice items
        for basket_item in basket_items:
            InvoiceItem.objects.create(
                invoice=invoice,
                product=basket_item.product_id,  
                quantity=basket_item.cantidad,
                price=basket_item.precio
            )
        
        # Empty the basket
        basket_items.delete()
        
        return Response({
            "message": "Compra completada con éxito",
            "invoice_id": invoice.id,
            "total": total_amount
        }, status=status.HTTP_201_CREATED)

# Update an existing basket item
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_basket_item_by_id(request, id):
    try:
        item = get_object_or_404(BasketTemp, pk=id)
        serializer = BasketTempSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"error": f"Error al actualizar el artículo de la cesta: {str(e)}"},
            status=status.HTTP_404_NOT_FOUND
        )

# Delete a basket item
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_basket_item_by_id(request, id):
    try:
        item = get_object_or_404(BasketTemp, pk=id)
        item.delete()
        return Response(
            {"message": "Artículo de la cesta eliminado con éxito"},
            status=status.HTTP_204_NO_CONTENT
        )
    except Exception as e:
        return Response(
            {"error": f"Error al eliminar el artículo de la cesta: {str(e)}"},
            status=status.HTTP_404_NOT_FOUND
        )

# Get basket items by user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_basket_items_by_user(request, user_id):
    items = BasketTemp.objects.filter(user_id=user_id)
    serializer = BasketTempSerializer(items, many=True)
    return Response(serializer.data)

# Get user's basket summary (total number of items and total price)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_basket_summary(request, user_id):
    items = BasketTemp.objects.filter(user_id=user_id)
    
    if not items.exists():
        return Response({
            'user_id': user_id,
            'total_items': 0,
            'total_price': 0.0,
            'items': []
        })
    
    # Calculate totals
    total_items = sum(item.quantity for item in items)
    total_price = sum(item.get_total() for item in items)
    
    # Serialize items
    serializer = BasketTempSerializer(items, many=True)
    
    return Response({
        'user_id': user_id,
        'total_items': total_items,
        'total_price': total_price,
        'items': serializer.data
    })

# Removes all items from a user's basket
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_user_basket(request, user_id):
    try:
        items = BasketTemp.objects.filter(user_id=user_id)
        if items.exists():
            items_count = items.count()
            items.delete()
            return Response(
                {"message": f"Se eliminaron con éxito {items_count} artículos de la cesta del usuario"},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"message": "La cesta del usuario ya está vacía"},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"error": f"Error al vaciar la cesta del usuario: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )
