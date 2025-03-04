from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_invoices, name='get-all-invoices'),
    path('<int:id>/', views.get_invoice_by_id, name='get-invoice-by-id'),
    path('create/', views.create_invoice, name='create-invoice'),
    path('<int:id>/update/', views.update_invoice_by_id, name='update-invoice'),
    path('<int:id>/delete/', views.delete_invoice_by_id, name='delete-invoice'),
    path('type/<int:type_id>/', views.get_invoices_by_type, name='invoices-by-type'),
    path('company/<int:company_id>/', views.get_invoices_by_company, name='invoices-by-company'),
    path('user/<int:user_id>/', views.get_invoices_by_user, name='invoices-by-user'),
    path('<int:id>/export-csv/', views.export_invoice_to_csv, name='export-invoice-csv'),
]