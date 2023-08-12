from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.permissions import (IsAuthenticated)
from rest_framework.response import (Response)
from rest_framework.views import (APIView)
from rest_framework_simplejwt.tokens import (RefreshToken)

from user.models import Project
from user.serializers import ProjectDetailModelSerializer, \
    RegisterSerializer, ResetPasswordSerializer, ForgotPasswordSerializer, SendEmailSerializer
from user.services import (register_service, reset_password_service, reset_password_confirm_service,
                           send_password_reset_email)
from user.tasks import send_email_customer


# Register API
class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = ()

    def post(self, request):
        response = register_service(request.data, request)
        if response['success']:
            return Response(status=201)
        return Response(response, status=400)


class ResetPasswordAPIView(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        new_password = serializer.validated_data['new_password']

        response = reset_password_service(user, new_password)
        if response['success']:
            return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
        return Response({'message': 'Password reset failed.'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmAPIView(APIView):
    def post(self, request, token, uuid):
        response = reset_password_confirm_service(request, token, uuid)
        if response['success']:
            return Response({'message': 'Password changed'})
        return Response(response, status=400)


class ForgotPasswordAPIView(GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        users = User.objects.filter(email=email)

        if not users.exists():
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if users.count() > 1:
            user = users.order_by('-date_joined').first()
        else:
            user = users.first()

        reset_link = f"http://127.0.0.1:8000/accounts/reset/{user.pk}"

        send_password_reset_email(user, reset_link)

        return Response({'message': 'Password reset link sent successfully.'}, status=status.HTTP_200_OK)


# Logout API
class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = RefreshToken(request.user)
        token.blacklist()
        return Response(status=200)


class VerifyAccountAPIView(APIView):
    permission_classes = ()

    def get(self, request, uid, token):
        pk = int(urlsafe_base64_decode(uid))
        print(pk)
        user = User.objects.get(pk=pk)
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

        return Response({
            'success': True,
            'message': 'Successfully active'
        })


# class AllProjectModelViewSet(ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = AllProjectsModelSerializer


class ProjectDetailRetrieveAPIView(RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailModelSerializer


# class ProjectSearchListAPIView(ListAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectDetailModelSerializer
#     filter_backends = [SearchFilter]
#     search_fields = ['title_en', 'title_uz', 'title_ru', 'keyword_uz', 'keyword_en', 'keyword_ru']

class SendMailAPIView(GenericAPIView):
    serializer_class = SendEmailSerializer
    permission_classes = ()

    @swagger_auto_schema(
        request_body=SendEmailSerializer,
        responses={200: 'Success', 400: 'Bad Request'}
    )

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get('email')
            message = serializer.validated_data.get('message')
            name = serializer.validated_data.get('name')
            phone = serializer.validated_data.get('phone')

            my_email = ''

            send_email_customer.delay(email, message, name, phone)
        except Exception as e:
            return Response({'success': False, 'message': str(e)})

        return Response({'success': True, 'message': 'Email sent!'})
