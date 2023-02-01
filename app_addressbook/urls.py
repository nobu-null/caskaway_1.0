from django.urls import path, include
from app_addressbook import views

urlpatterns = [
    path('', views.index, name="addressbookHome"),
]
