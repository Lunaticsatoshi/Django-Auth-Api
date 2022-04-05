from django.urls import path
from .views import RegisterView, LoginView, get_users, get_current_user, logout
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='user-register'),
    path('auth/login/', LoginView.as_view(), name='user-login'),
    path('auth/logout/', logout, name='user-logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('all/', get_users, name='get-users'),
    path('profile/current/', get_current_user, name='get-profile'),
]