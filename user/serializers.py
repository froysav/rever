from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, CharField, EmailField
from rest_framework import serializers
from user.models import Project


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class ResetPasswordSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    new_password = serializers.CharField(write_only=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class RegisterSerializer(ModelSerializer):
    password1 = CharField()
    password2 = CharField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')


# class AllProjectsModelSerializer(ModelSerializer):
#     class Meta:
#         model = Project
#         fields = (
#         'id', 'title_en', 'title_ru', 'title_uz', 'description_en', 'description_ru', 'description_uz', 'image')


class ProjectDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class SendEmailSerializer(serializers.Serializer):
    message = CharField(max_length=500)
    name = CharField(max_length=100)
    phone = CharField(max_length=55)
    email = EmailField()
