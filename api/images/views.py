from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import exceptions, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from user.authentication import CustomUserAuthentication
from user.models import Tier, User

from .models import Image
from .serializer import ImageSerializer


class ImageUploadView(CreateAPIView):
    serializer_class = ImageSerializer
    authentication_classes = (CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = ImageSerializer(
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            user_tier: Tier = request.user.image_tier
            all_thumbnail_sizes = user_tier.thumbnail_sizes.all()

            if (
                not user_tier.has_expiring
                and serializer.validated_data.get("expiration_time") is not None
            ):
                raise PermissionDenied(
                    "You do not have permission expiration time to perform this action."
                )
            image: Image = serializer.save()
            thumbnail_links = {}

            if user_tier.has_original is True:
                thumbnail_links[f"Original"] = request.build_absolute_uri(
                    reverse("get-image", args=[image.id, "original"])
                )

            for size in [s.size for s in all_thumbnail_sizes]:
                thumbnail_links[f"{size}px"] = request.build_absolute_uri(
                    reverse("get-image", args=[image.id, size])
                )

            response_data = {
                "id": image.id,
                "thumbnails": thumbnail_links,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IsAuthenticatedIfExpirationTimeNotNull(permissions.BasePermission):
    """
    Allows access only to authenticated users if the expiration time is not None.
    """

    def has_permission(self, request, view):
        image_id = view.kwargs.get("image_id")
        image = get_object_or_404(Image, id=image_id)

        if image.expiration_time is not None:
            return True

        return request.user.is_authenticated


class ImageDetailView(APIView):
    model = Image
    authentication_classes = (CustomUserAuthentication,)
    permission_classes = (IsAuthenticatedIfExpirationTimeNotNull,)

    def get(self, request, image_id, size):
        image = get_object_or_404(Image, id=image_id)

        image.validate_expiration()

        # if it has an expiration time then there is a public link
        if image.expiration_time is None:
            user: User = request.user
            if user != image.owner:
                raise exceptions.PermissionDenied()

            user.validator_tiers(size)

        if size == "original":
            image_data = image.image.read()
        else:
            image_data = image.resize(int(size))

        response = HttpResponse(image_data, content_type=f"image/{image.extension()}")
        response["Content-Disposition"] = "inline"
        return response
