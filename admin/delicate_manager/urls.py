from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import RedirectView
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuración de la vista de esquema
schema_view = get_schema_view(
    openapi.Info(
        title="Delicaté API Documentation",  # Título de la API
        default_version='v1',                # Versión de la API
        description="Documentación de la API de Delicaté",  # Descripción
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@delicate.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,  # Hacer que el esquema sea público
    permission_classes=[permissions.AllowAny],  # Permisos para acceder a la documentación 
)
urlpatterns = [
    # Redirigir a la página de administración(bbdd local SQLite3)
    path('', RedirectView.as_view(url='/admin/'), name='redirect-to-admin'),
    path('admin/', admin.site.urls),
    # Agrupar rutas de la API bajo una versión específica
    path('v1/api/', include([
        path('store/', include('delicate_apps.store.urls')),
        path('invoices/', include('delicate_apps.invoices.urls')),
        path('basket/', include('delicate_apps.basket.urls')),
        path('type/', include('delicate_apps.type.urls')),
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('company/', include('delicate_apps.company.urls')),
        path('users/', include('delicate_apps.users.urls')),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ])),
]

