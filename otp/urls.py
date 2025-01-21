from django.urls import path
from . import views  # Ensure this line is present

urlpatterns = [
    path('', views.login_view, name='login'),  # Default route to login
    path('login/', views.login_view, name='login'),
    path('otp/<int:user_id>/', views.otp_verify, name='otp_verify'),
    path('welcome/', views.welcome, name='welcome'),
    path('register/', views.register_view, name='register'),  # Register route
]
