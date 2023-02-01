from django.urls import path, include
from app_faultlog import views

urlpatterns = [
    path('', views.index, name="faultlogHome"),
]
