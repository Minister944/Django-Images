from django.contrib import admin
from user.models import Size, Tier

from .models import Image


class TierAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "size_list",
        "has_expiring",
        "has_original",
    )

    def size_list(self, obj):
        return ", ".join([str(size) for size in obj.thumbnail_sizes.all()])

    size_list.short_description = "Thumbnail sizes"


class ImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "image",
        "expiration_time",
    )


class SizeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "size",
    )


admin.site.register(Tier, TierAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Size, SizeAdmin)
