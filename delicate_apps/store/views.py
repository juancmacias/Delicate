from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import StoreProduct
from .serializers import StoreProductSerializer, StoreProductDetailSerializer
import cloudinary.uploader

# Get all products with optional filtering
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_products(request):
    # Params for filtering existing
    category = request.query_params.get('category', None)
    company_id = request.query_params.get('company_id', None)
    type_id = request.query_params.get('type_id', None)
    name = request.query_params.get('name', None)
    
    # Get all products
    products = StoreProduct.objects.all()
    
    # Apply filters
    if category:
        products = products.filter(category__icontains=category)
    if company_id:
        products = products.filter(fk_company=company_id)
    if type_id:
        products = products.filter(fk_type=type_id)
    if name:
        products = products.filter(name__icontains=name)
    
    serializer = StoreProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product_by_id(request, id):
    try:
        product = get_object_or_404(StoreProduct, pk=id)
        serializer = StoreProductDetailSerializer(product)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {"error": f"Error al obtener el producto: {str(e)}"},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    # Manage image upload to Cloudinary
    if 'image' in request.FILES:
        try:
            # Add the image to Cloudinary
            upload_result = cloudinary.uploader.upload(
                request.FILES['image'], 
                folder='productos/',
                transformation=[
                    {'width': 500, 'height': 500, 'crop': 'limit'},
                    {'quality': 'auto'},
                    {'fetch_format': 'auto'}
                ]
            )
            # Add cloudinary url to the request data
            request.data['image'] = upload_result['public_id']
        except Exception as e:
            return Response(
                {"error": f"Error al subir la imagen: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    serializer = StoreProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product_by_id(request, id):
    try:
        product = get_object_or_404(StoreProduct, pk=id)
        
        # Manage image upload to Cloudinary
        if 'image' in request.FILES:
            try:
                # If the image is existing, delete it from Cloudinary
                if product.image:
                    cloudinary.uploader.destroy(product.image.public_id)
                
                # Upload the new image to Cloudinary
                upload_result = cloudinary.uploader.upload(
                    request.FILES['image'], 
                    folder='productos/',
                    transformation=[
                        {'width': 500, 'height': 500, 'crop': 'limit'},
                        {'quality': 'auto'},
                        {'fetch_format': 'auto'}
                    ]
                )
                # Add cloudinary url to the request data
                request.data['image'] = upload_result['public_id']
            except Exception as e:
                return Response(
                    {"error": f"Error al subir la imagen: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = StoreProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"error": f"Error al actualizar el producto: {str(e)}"},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product_by_id(request, id):
    try:
        product = get_object_or_404(StoreProduct, pk=id)
        
        # Delete the image from Cloudinary
        if product.image:
            cloudinary.uploader.destroy(product.image.public_id)
        
        product.delete()
        return Response(
            {"message": "Producto eliminado correctamente"},
            status=status.HTTP_204_NO_CONTENT
        )
    except Exception as e:
        return Response(
            {"error": f"Error al eliminar el producto: {str(e)}"},
            status=status.HTTP_404_NOT_FOUND
        )

# Get products by company ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_products_by_company(request, company_id):
    products = StoreProduct.objects.filter(fk_company=company_id)
    serializer = StoreProductSerializer(products, many=True)
    return Response(serializer.data)

# Get products by type ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_products_by_type(request, type_id):
    products = StoreProduct.objects.filter(fk_type=type_id)
    serializer = StoreProductSerializer(products, many=True)
    return Response(serializer.data)
