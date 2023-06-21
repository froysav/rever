from django.urls import path
from .views import RegisterAPIView, LogoutAPIView

urlpatterns = [
    path('registere/', RegisterAPIView.as_view(), name='register'),
    path('logoute/', LogoutAPIView.as_view(), name='logout'),
]