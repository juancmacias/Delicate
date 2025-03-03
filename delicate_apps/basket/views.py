from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import transaction
from .models import BasketTemp
from delicate_apps.invoices.models import Invoice, InvoiceItem
from delicate_apps.store.models import StoreProduct
from .serializers import BasketTempSerializer, BasketTempDetailSerializer

# Obtain all items from the basket
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_basket_items(request):
    # Filtrar por usuario si se proporciona
    user_id = request.query_params.get('user_id')
    items = BasketTemp.objects.all()
    
    if user_id:
        items = items.filter(user_id=user_id)
        
    serializer = BasketTempSerializer(items, many=True)
    return Response(serializer.data)

# Obtain a specific item from the basket by ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_basket_item_by_id(request, id):
    try:
        item = get_object_or_404(BasketTemp, pk=id)
        serializer = BasketTempDetailSerializer(item)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {"error": f"Error al obtener el artículo: {str(e)}"},
            status=status.HTTP_404_NOT_FOUND
        )

# Add a new item to the basket
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_basket(request):
    with transaction.atomic():
        try:
            # Obtain and validate data
            user_id = request.data.get('user_id')
            product_id = request.data.get('product_id')
            quantity = int(request.data.get('quantity', 1))

            if quantity <= 0:
                return Response(
                    {"error": "La cantidad debe ser positiva"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Verify product stock and update stock
            product = get_object_or_404(StoreProduct, pk=product_id)
            if product.stock < quantity:
                return Response(
                    {"error": "Stock insuficiente"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create or update basket item
            basket_item, created = BasketTemp.objects.get_or_create(
                user_id_id=user_id,
                product_id=product,
                defaults={
                    'cantidad': quantity,
                    'precio': product.get_total_price(),
                    'temp_date': timezone.now()
                }
            )

            if not created:
                basket_item.cantidad += quantity
                basket_item.save()

            # Create auto invoice
            invoice = Invoice.objects.create(
                date=timezone.now().date(),
                payment_form='Efectivo',
                neto=product.get_total_price() * quantity,
                fk_user_id=user_id,
                fk_company=product.fk_company,
                fk_type=product.fk_type
            )

            # Create invoice details
            InvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=quantity,
                price=product.get_total_price()
            )

            # Update stock
            product.stock -= quantity
            product.save()

            serializer = BasketTempSerializer(basket_item)
            return Response({
                "message": "Producto añadido y factura generada",
                "item": serializer.data,
                "invoice_id": invoice.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

# Update an item in the basket
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_basket_item(request, id):
    with transaction.atomic():
        try:
            item = get_object_or_404(BasketTemp, pk=id)

            # Validate new quantity if provided
            new_quantity = request.data.get('cantidad')
            if new_quantity is not None:
                if new_quantity <= 0:
                    return Response(
                        {"error": "La cantidad debe ser positiva"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if new_quantity > item.product_id.stock:
                    return Response(
                        {"error": "Stock insuficiente"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            serializer = BasketTempSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

# Delete an item from the basket
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_basket_item(request, id):
    try:
        item = get_object_or_404(BasketTemp, pk=id)
        item.delete()
        return Response(
            {"message": "Item eliminado correctamente"},
            status=status.HTTP_204_NO_CONTENT
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

# Process the checkout of the basket
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    with transaction.atomic():
        try:
            user_id = request.data.get('user_id')
            
            # Verify items in the basket
            basket_items = BasketTemp.objects.filter(user_id=user_id)
            if not basket_items.exists():
                return Response(
                    {"error": "El carrito está vacío"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Total calculation
            total = sum(item.get_total() for item in basket_items)

            # Create  invoice
            invoice = Invoice.objects.create(
                date=timezone.now().date(),
                payment_form=request.data.get('payment_form', 'Efectivo'),
                neto=total,
                fk_user_id=user_id,
                fk_company_id=request.data.get('company_id'),
                fk_type_id=request.data.get('type_id')
            )

            # Create invoice and invoice details
            for item in basket_items:
                InvoiceItem.objects.create(
                    invoice=invoice,
                    product=item.product_id,
                    quantity=item.cantidad,
                    price=item.precio
                )
                
                # Update stock
                product = item.product_id
                product.stock -= item.cantidad
                product.save()

            # Clean basket
            basket_items.delete()

            return Response({
                "message": "Compra procesada correctamente",
                "invoice_id": invoice.id,
                "total": total
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )