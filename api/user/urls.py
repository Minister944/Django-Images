from django.urls import path

from . import apis

urlpatterns = [
    path("login/", apis.LoginApi.as_view(), name="login"),
    path("me/", apis.UserApi.as_view(), name="me"),
]
