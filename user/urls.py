from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import (
    RegisterAPIView, LogoutAPIView,
    VerifyAccountAPIView, ProjectDetailRetrieveAPIView,
    SendMailAPIView, PasswordResetConfirmAPIView, ResetPasswordAPIView, ForgotPasswordAPIView
)

routers = DefaultRouter()
# routers.register('project', AllProjectModelViewSet)

urlpatterns = [
    # path('', include(routers.urls)),
    path('register', RegisterAPIView.as_view(), name='register'),
    # path('resetconfirm', PasswordResetConfirmAPIView.as_view(), name='reset'),
    # path('reset', ResetPasswordAPIView.as_view(), name='resete'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    # path('verify/<str:uid>/<str:token>', VerifyAccountAPIView.as_view(), name='verify'),
    path('project_detail/<int:pk>', ProjectDetailRetrieveAPIView.as_view()),
    # path('project_search', ProjectSearchListAPIView.as_view()),
    # path('send_mail', SendMailAPIView.as_view(), name='send_mail'),
    path('reset', ResetPasswordAPIView.as_view(), name='reset'),
    path('forgot/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
]
