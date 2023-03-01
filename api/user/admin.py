from django.contrib import admin

from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "email",
        "is_staff",
        "image_tier",
    )


admin.site.register(models.User, UserAdmin)
