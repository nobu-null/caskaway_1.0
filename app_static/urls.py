from django.urls import path, include
from app_static import views

urlpatterns = [
    path('', views.index, name="index"),
]
