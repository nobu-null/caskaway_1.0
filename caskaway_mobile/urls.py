"""caskaway_mobile URL Configuration

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
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Caskaway Admin Panel'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_static.urls')),
    path('finance/', include('app_finance.urls')),
    path('operations/', include('app_operations.urls')),
    path('faultlog/', include('app_faultlog.urls')),
    path('compliance/', include('app_compliance.urls')),
    path('addressbook/', include('app_addressbook.urls')),
    path('users/', include('app_users.urls')),
    path('users/', include('django.contrib.auth.urls')),

]
