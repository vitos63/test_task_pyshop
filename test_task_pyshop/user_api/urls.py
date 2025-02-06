from django.urls import path
from user_api.views import RegisterAPIView, LoginAPIView, RefreshTokenAPIView, LogoutApiView, ProfileAPIView


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('refresh/', RefreshTokenAPIView.as_view(), name='refresh'),
    path('logout/', LogoutApiView.as_view(), name='logout'),
    path('me/', ProfileAPIView.as_view(), name='me')
]