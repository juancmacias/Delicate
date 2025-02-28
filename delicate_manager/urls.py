"""
URL configuration for delicate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Agrupar rutas de la API bajo una versión específica
    path('v1/api/', include([
        path('company/', include('delicate_apps.company.urls')),
        path('users/', include('delicate_apps.users.urls')),
        path('store/', include('delicate_apps.store.urls')),
        path('invoices/', include('delicate_apps.invoices.urls')),
        path('basket/', include('delicate_apps.basket.urls')),
        path('type/', include('delicate_apps.type.urls')),
    ])),
]

