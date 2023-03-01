from datetime import timedelta

from core.settings import MAX_SIZE_IMG
from django.core.exceptions import ValidationError
from django.utils import timezone
from images.models import Image
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    expiration_time = serializers.IntegerField(
        min_value=300, max_value=30000, required=False, default=None
    )

    class Meta:
        model = Image
        fields = ("image", "expiration_time")

    def create(self, validated_data):
        expiration_time = validated_data.pop("expiration_time", None)
        if expiration_time is not None:
            now = timezone.now()
            expiration_date = now + timedelta(seconds=expiration_time)
            validated_data["expiration_time"] = expiration_date
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)

    def validate_image(self, image: Image):
        if not image.content_type in ["image/png", "image/jpg"]:
            raise ValidationError("Only png and jpg allowed.")
        if image.size > MAX_SIZE_IMG:
            raise ValidationError("Image size is too big. Max allowed size is 10 MB.")
        return image
