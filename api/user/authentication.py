import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import authentication, exceptions

from .models import User


class CustomUserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("jwt")
        if not token:
            return None

        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed("Invalid token.")
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired.")
        except:
            raise exceptions.AuthenticationFailed("Other problem with token.")
        user: User = get_object_or_404(User, id=payload["id"])

        return (user, None)
