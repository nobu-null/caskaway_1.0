from django.urls import path, include
from app_finance import views

urlpatterns = [
    path('', views.index, name='financeHome'),
    path('targets/', views.targets, name='targets'),
    path('summary/', views.summary, name='summary'),
]