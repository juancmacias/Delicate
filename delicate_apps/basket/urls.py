from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_basket_items, name='get-all-basket-items'),
    path('<int:id>/', views.get_basket_item_by_id, name='get-basket-item-by-id'),
    path('create/', views.create_basket_item, name='create-basket-item'),
    path('<int:id>/update/', views.update_basket_item_by_id, name='update-basket-item'),
    path('<int:id>/delete/', views.delete_basket_item_by_id, name='delete-basket-item'),
    path('user/<int:user_id>/', views.get_basket_items_by_user, name='basket-items-by-user'),
    path('user/<int:user_id>/summary/', views.get_user_basket_summary, name='user-basket-summary'),
    path('user/<int:user_id>/clear/', views.clear_user_basket, name='clear-user-basket'),
]