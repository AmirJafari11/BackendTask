from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer, LoginSerializer, LoginSerializerCreateAccessToken, LogoutSerializer, \
                         UserSerializer
from .utils import token_for_user_as_login
from BackendTask.settings import REDIS_JWT_TOKEN, REDIS_REFRESH_TIME


# Create your views here.


class RegisterAPIView(APIView):
    """
        This view is for "registration".
    """
    serializer_class = RegisterSerializer

    def get(self, request: Request) -> Response:
        users = User.objects.all()
        serializer = UserSerializer(instance=users, many=True)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message": "You are registered successfully"},
                            status=status.HTTP_201_CREATED)
        return Response(data={"message": "The passwords do not match."},
                        status=status.HTTP_400_BAD_REQUEST)


# ===================================================================================


class LoginAPIView(APIView):
    """
        This view is for "login".
    """
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        try:
            user = User.objects.get(username=serializer.data['username'])
            if user.check_password(serializer.data['password']):
                token = token_for_user_as_login(user)
                access_token = token['access']
                refresh_token = token['refresh']
                REDIS_JWT_TOKEN.set(name=refresh_token, value=refresh_token, ex=REDIS_REFRESH_TIME)
                data = {
                    "user": {
                        'name': user.username,
                    },
                    "access": access_token,
                    "refresh": REDIS_JWT_TOKEN.get(refresh_token)
                }
                return Response(data={'Token': data},
                                status=status.HTTP_201_CREATED)
            else:
                return Response(data={"message": "Username or Password is Wrong."},
                                status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response(data={"message": "You cannot login. First Register."},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginAPIViewCreateAccess(APIView):
    """
        This view is for "Creating New Access Token".
    """
    serializer_class = LoginSerializerCreateAccessToken

    def post(self, request: Request) -> Response:
        try:
            token = request.data['refresh_token']
            REDIS_JWT_TOKEN.delete(token)
            token = RefreshToken(token)
            user = User.objects.get(id=token['user_id'])
            access_refresh_token = token_for_user_as_login(user)
            access_token = access_refresh_token['access']
            refresh_token = access_refresh_token['refresh']
            REDIS_JWT_TOKEN.set(name=refresh_token, value=refresh_token, ex=REDIS_REFRESH_TIME)
            data = {
                "user": {
                    'name': user.username,
                },
                "new access": access_token,
                "new refresh": REDIS_JWT_TOKEN.get(refresh_token)
            }
            return Response(data={'Token': data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = str(e)
            return Response(data={"message": "Token is expired", "error_message": error_message},
                            status=status.HTTP_400_BAD_REQUEST)


# --------------------------------------------------------------------------


class LogoutAPIView(APIView):
    """
        This view is for "Logout".
    """
    serializer_class = LogoutSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        refresh_token = request.data['refresh_token']
        if REDIS_JWT_TOKEN.exists(refresh_token):
            REDIS_JWT_TOKEN.delete(refresh_token)
            return Response({"message": "You are logged out successfully"})
        else:
            return Response({"message": "There is no refresh token in redis"})
