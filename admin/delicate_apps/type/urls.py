from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_types, name='get-all-types'),
    path('<int:id>/', views.get_type_by_id, name='get-type-by-id'),
    path('create/', views.create_type, name='create-type'),
    path('<int:id>/update/', views.update_type_by_id, name='update-type'),
    path('<int:id>/delete/', views.delete_type_by_id, name='delete-type'),
]