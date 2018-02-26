from django.contrib import admin

from .models import (
    AboutMember,
    AboutGeneral,
    AboutDate,
    Event,
)

admin.site.register(AboutMember)
admin.site.register(AboutGeneral)
admin.site.register(AboutDate)
admin.site.register(Event)
