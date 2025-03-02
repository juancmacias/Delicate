from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Type
from .serializers import TypeSerializer

# Obtain all types with optional filtering by name
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_types(request):
    name_filter = request.query_params.get('name', '')
    if name_filter:
        types = Type.objects.filter(name_type__icontains=name_filter)
    else:
        types = Type.objects.all()
    serializer = TypeSerializer(types, many=True)
    return Response(serializer.data)

# Obtain a specific type by ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_type_by_id(request, id):
    try:
        type_obj = get_object_or_404(Type, pk=id)
        serializer = TypeSerializer(type_obj)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {"error": f"Error al obtener el tipo: {str(e)}"}, 
            status=status.HTTP_404_NOT_FOUND
        )

# Create a new type
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_type(request):
    serializer = TypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update a type by ID
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_type_by_id(request, id):
    try:
        type_obj = get_object_or_404(Type, pk=id)
        serializer = TypeSerializer(type_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"error": f"Error al actualizar el tipo: {str(e)}"},
            status=status.HTTP_404_BAD_REQUEST
        )

# Delete a type by ID
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_type_by_id(request, id):
    try:
        type_obj = get_object_or_404(Type, pk=id)
        type_obj.delete()
        return Response({"message": "Tipo eliminado correctamente"},
            status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response(
            {"error": f"Error al eliminar el tipo: {str(e)}"},
            status=status.HTTP_404_NOT_FOUND
            )



