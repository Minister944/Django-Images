from django.contrib.auth.models import AbstractUser
from django.db.models import (CASCADE, BooleanField, CharField, ForeignKey,
                              IntegerField, ManyToManyField, Model)
from rest_framework.exceptions import PermissionDenied


class Size(Model):
    size = IntegerField()

    def __str__(self) -> str:
        return str(self.size)


class Tier(Model):
    name = CharField(max_length=255, unique=True)
    has_original = BooleanField(default=False)
    has_expiring = BooleanField(default=False)
    thumbnail_sizes = ManyToManyField(Size)

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    image_tier = ForeignKey(Tier, on_delete=CASCADE, null=True)

    def validator_tiers(self, size):
        all_sizes = self.image_tier.thumbnail_sizes.all()
        sizes = [str(s.size) for s in all_sizes]

        if self.image_tier.has_original:
            sizes.append("original")
        if str(size) not in sizes:
            raise PermissionDenied("Invalid thumbnail size.")

    def __str__(self):
        return self.email
