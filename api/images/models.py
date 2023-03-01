import os
from io import BytesIO

from django.db.models import (CASCADE, DateTimeField, ForeignKey, ImageField,
                              Model)
from django.utils import timezone
from PIL import Image as PilImage
from user.models import User

from .exceptions import ExpiredLinkException


class Image(Model):
    owner = ForeignKey(User, on_delete=CASCADE)
    image = ImageField(upload_to="images/")
    expiration_time = DateTimeField(blank=True, null=True)

    def resize(self, size):
        image = PilImage.open(BytesIO(self.image.read()))

        w, h = image.size
        ratio = h / w
        new_height = size
        new_width = int(size / ratio)

        new_size = (new_width, new_height)

        image = image.resize(new_size, PilImage.ANTIALIAS)
        output = BytesIO()
        image.save(output, format=self.extension())
        output.seek(0)
        return output.read()

    def validate_expiration(self):
        if self.expiration_time is not None and timezone.now() > self.expiration_time:
            raise ExpiredLinkException()

    def __str__(self) -> str:
        return os.path.basename(self.image.name)

    def extension(self):
        _, extension = os.path.splitext(self.image.name)
        return extension[1:]
