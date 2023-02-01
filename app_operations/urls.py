from django.urls import path, include
from app_operations import views

urlpatterns = [
    path('', views.index, name="operationsHome"),
]
