from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterUserView

urlpatterns = [
    # endpoint for obtaining JWT tokens
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # endpoint for obtaining JWT tokens
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # endpoint for refreshing JWT tokens

    path('auth/register/', RegisterUserView.as_view(), name='register_user'),  # endpoint for user registration
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # endpoint for user login


]