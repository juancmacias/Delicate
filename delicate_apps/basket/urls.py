from django.urls import path
from . import views

urlpatterns = [
    path('basket/', views.get_all_basket_items, name='basket-list'),
    path('basket/<int:id>/', views.get_basket_item_by_id, name='basket-detail'),
    path('basket/add/', views.add_to_basket, name='basket-add'),
    path('basket/update/<int:id>/', views.update_basket_item, name='basket-update'),
    path('basket/delete/<int:id>/', views.delete_basket_item, name='basket-delete'),
    path('basket/checkout/', views.checkout, name='basket-checkout'),
]