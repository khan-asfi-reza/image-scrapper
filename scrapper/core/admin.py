"""
Admin
"""
from django.contrib import admin

from scrapper.core.models import Address, Image


class URLAdmin(admin.ModelAdmin):
    """
    URL Address Admin Size
    View for stored addresses
    """

    list_display = ["id", "url", "created", "updated"]


class ImageAdmin(admin.ModelAdmin):
    """
    Admin view for Image Model
    """

    list_display = ["image_name", "id", "format", "mode", "parent_url"]
    readonly_fields = [
        "image",
    ]


# Registers these models with custom view in /admin route

admin.site.register(Address, URLAdmin)
admin.site.register(Image, ImageAdmin)
