from django.urls import path

from .views import ImageDetailView, ImageUploadView

urlpatterns = [
    path("upload/", ImageUploadView.as_view(), name="upload-image"),
    path(
        "image/<int:image_id>/<str:size>", ImageDetailView.as_view(), name="get-image"
    ),
]
