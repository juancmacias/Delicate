from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import RedirectView

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
    ])),
]

