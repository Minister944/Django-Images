from django.shortcuts import get_object_or_404
from rest_framework import exceptions, generics, permissions, response, views

from . import authentication
from . import serializer as user_serializer
from . import services
from .models import User


class LoginApi(generics.CreateAPIView):
    serializer_class = user_serializer.LoginUserSerializer

    def post(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        user = get_object_or_404(User, username=username)

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid Credentials")

        if not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Invalid Credentials")

        token = services.create_token(user_id=user.id)

        resp = response.Response()

        resp.set_cookie(key="jwt", value=token, httponly=True)

        return resp


class UserApi(views.APIView):
    """
    This endpoint can only be used
    if the user is authenticated
    """

    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user

        serializer = user_serializer.UserSerializer(user)

        return response.Response(serializer.data)
