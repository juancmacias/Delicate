from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Agrupar rutas de la API bajo una versión específica
    path('v1/api/', include([
    #     path('company/', include('delicate_apps.company.urls')),
    #     path('users/', include('delicate_apps.users.urls')),
    path('store/', include('delicate_apps.store.urls')),
    #     path('invoices/', include('delicate_apps.invoices.urls')),
    #     path('basket/', include('delicate_apps.basket.urls')),
    path('type/', include('delicate_apps.type.urls')),
    ])),
]

