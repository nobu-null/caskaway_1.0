from django.urls import path
from app_users import views

urlpatterns = [
    path('login_user', views.login_user, name="login_users"),
    path('logout_user', views.logout_user, name="logout_users"),
]
