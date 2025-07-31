"""soyyo_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('auth/', include('apps.authentication.urls')),
                  path('profile/', include('apps.profile.urls')),
                  path('soy-yo/', include('apps.public.urls')),
                  path('email/', include('apps.contact.urls')),
                  path('adm/', include('apps.administration.urls')),
                  path('pay/', include('apps.pay.urls')),
                  path('booking/', include('apps.booking.urls')),
                  path('mercado_pago/', include('apps.mercado_pago.urls')),
                  path('client_contact/', include('apps.client_contact.urls')),
                  path('ecommerce/', include('apps.ecommerce.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
