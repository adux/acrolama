from django.contrib import admin
from audiovisual.models import Avatar, Image, Video


class ImageAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "formImage",
        "image",
        "thumbnail",
        "mob",
        "image_height",
        "image_width",
    ]


class AvatarAdmin(admin.ModelAdmin):
    list_display = [
        "formImage",
        "image",
        "thumbnail",
        "image_height",
        "image_width",
    ]


admin.site.register(Avatar, AvatarAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Video)
