from django.contrib import admin
from .models import Image, Video


class ImageAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "formImage",
        "image",
        "thumbnail",
        "image_height",
        "image_width",
    ]


admin.site.register(Image, ImageAdmin)
admin.site.register(Video)
# Register your models here.
