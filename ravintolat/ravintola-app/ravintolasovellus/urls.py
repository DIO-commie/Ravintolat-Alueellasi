"""
URL configuration for ravintolasovellus project.

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
from django.urls import path

from django.contrib import admin
from django.urls import path, include

from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('ravintolat.urls')),
    path('', views.index, name='index'),
    path('ravintola/<int:ravintola_id>/', views.ravintola_detail, name='ravintola_detail'),
    path('lisää_arvostelu/<int:ravintola_id>/', views.lisaa_arvostelu, name='lisaa_arvostelu'),
    path('profiili/', views.profiili, name='profiili'),
    path('suosikit/', views.suosikit, name='suosikit'),
]
