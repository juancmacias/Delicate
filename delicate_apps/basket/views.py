from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import BasketTemp
from .serializers import BasketTempSerializer, BasketTempDetailSerializer

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

# Create a new basket item
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_basket_item(request):
    serializer = BasketTempSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    total_items = sum(item.cantidad for item in items)
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
