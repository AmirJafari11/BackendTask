from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
        This serializer is for serializing and deserializing the data of model 'User'.
    """

    class Meta:
        model = User
        # fields = '__all__'
        fields = ['username', 'first_name', 'last_name', 'is_staff']
        # exclude = ('password', 'last_login', 'is_superuser', 'is_active', 'date_joined', 'groups', 'user_permissions')


class RegisterSerializer(serializers.Serializer):
    """
        This serializer returns us a form involves "username", "password1" and "password2" for registration.
        We do some validation checks about:
            1. "username" that whether there is any username in the database before or not.
            2. "password" that the user must import the correct password using 'confirm password'.
    """
    username = serializers.CharField()
    password1 = serializers.CharField(label='password')
    password2 = serializers.CharField(label='confirm password')

    def validate_username(self, value):
        user = User.objects.filter(username=value).exists()
        if user:
            raise ValidationError(_("This username already exists"))
        return value

    def validate(self, data):
        password1_value = data.get('password1')
        password2_value = data.get('password2')

        if password1_value and password2_value and password1_value != password2_value:
            raise ValidationError(_("The passwords must match"))
        return data

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        password=validated_data['password1']),
        return user


# --------------------------------------------------------------------------------------------------

class LoginSerializer(serializers.ModelSerializer):
    """
        This serializer returns us a form involves "username" and "password" for login.
    """

    class Meta:
        model = User
        fields = ['username', 'password']

# ------------------------


class LoginSerializerCreateAccessToken(serializers.Serializer):
    """
        This serializer returns us a form involves "refresh_token" for creating new access and refresh tokens.
    """
    refresh_token = serializers.CharField()

# -----------------------------------------------------------------------------------------------------


class LogoutSerializer(serializers.Serializer):
    """
        This serializer returns us a form involves "refresh_token" for logout.
    """
    refresh_token = serializers.CharField()
