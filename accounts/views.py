from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer
from .services import register_service, reset_password_service, reset_password_confirm_service


class RegisterAPIView(APIView):

    def post(self, request):
        response = register_service(request.data)
        if response['success']:
            return Response(status=201)
        return Response(response, status=405)


class ResetPasswordAPIView(APIView):

    def post(self, request):
        response = reset_password_service(request)
        if response['success']:
            return Response({'message': 'sent'})
        return Response(response, status=404)


class PasswordResetConfirmAPIView(APIView):

    def post(self, request, token, uuid):
        response = reset_password_confirm_service(request, token, uuid)
        if response['success']:
            return Response({'message': 'Password changed'})
        return Response(response, status=400)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = RefreshToken(request.user)
        token.blacklist()
        return Response(status=200)


class UserLoginAPIView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')

        user = authenticate(request, username=phone, password=password)
        if user is not None:
            login(request, user)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response(
                {
                    'message': 'Login successful',
                    'access_token': access_token,
                    'refresh_token': str(refresh),
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserRegistrationAPIView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        username = request.data.get('username')
        owner = request.data.get('owner')
        phirm = request.data.get('phirm')
        bank = request.data.get('bank')
        mfo = request.data.get('mfo')
        addres = request.data.get('addres')
        inn = request.data.get('inn')
        bank_number = request.data.get('bank_number')
        password = request.data.get('password')

        if User.objects.filter(username=phone).exists():
            return Response({'message': 'Phone number already registered'}, status=status.HTTP_409_CONFLICT)

        user = User.objects.create_user(username=phone, password=password)
        if user is not None:
            return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Registration failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk=None):
        phone = request.data.get('phone')
        password = request.data.get('password')

        user, created = User.objects.get_or_create(pk=pk)
        user.username = phone
        user.set_password(password)
        user.save()

        if created:
            return Response({'message': 'User registration successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'User registration updated successfully'}, status=status.HTTP_200_OK)

    def get(self, request):
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)