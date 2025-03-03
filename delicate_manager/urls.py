from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Urls de las aplicaciones
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/company/', include('delicate_apps.company.urls')),
    path('api/users/', include('delicate_apps.users.urls')),
    # path('api/store/', include('delicate_apps.store.urls')),
    # path('api/invoices/', include('delicate_apps.invoices.urls')),
    # path('api/basket/', include('delicate_apps.basket.urls')),
    # Agrupar rutas de la API bajo una versión específica
    path('v1/api/', include([
    #     path('company/', include('delicate_apps.company.urls')),
    #     path('users/', include('delicate_apps.users.urls')),
    path('store/', include('delicate_apps.store.urls')),
    path('invoices/', include('delicate_apps.invoices.urls')),
    path('basket/', include('delicate_apps.basket.urls')),
    path('type/', include('delicate_apps.type.urls')),
    ])),
]

