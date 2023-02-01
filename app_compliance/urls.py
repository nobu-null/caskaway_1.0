from django.urls import path, include
from app_compliance import views

urlpatterns = [
    path('', views.index, name="complianceHome"),
]
