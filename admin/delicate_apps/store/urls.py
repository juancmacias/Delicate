from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_products, name='get-all-products'),
    path('<int:id>/', views.get_product_by_id, name='get-product-by-id'),
    path('create/', views.create_product, name='create-product'),
    path('<int:id>/update/', views.update_product_by_id, name='update-product'),
    path('<int:id>/delete/', views.delete_product_by_id, name='delete-product'),
    path('company/<int:company_id>/', views.get_products_by_company, name='products-by-company'),
    path('type/<int:type_id>/', views.get_products_by_type, name='products-by-type'),
]