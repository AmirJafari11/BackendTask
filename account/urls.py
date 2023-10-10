from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='user-register'),
    path('login/token/', views.LoginAPIView.as_view(), name='user-login-token'),
    path('login/token/refresh/', views.LoginAPIViewCreateAccess.as_view(), name='user-login-token-create'),
    path('logout/', views.LogoutAPIView.as_view(), name='user-logout'),
]
