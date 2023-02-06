from django.urls import path, include
from app_finance import views

urlpatterns = [
    path('', views.index, name='financeHome'),
    path('targets/', views.targets, name='targets'),
    path('epos_summary/', views.epos_summary, name='epos-summary'),
    path('income_summary/', views.income_summary, name='income-summary'),
    path('expenses_summary/', views.expenses_summary, name='expenses-summary'),
    path('deposits_summary/', views.deposits_summary, name='deposits-summary'),
    path('hours_summary/', views.hours_summary, name='hours-summary'),
    path('update_epos/<id>/', views.update_epos, name="update-epos"),

]