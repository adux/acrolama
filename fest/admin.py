from django.contrib import admin

# Register your models here.

from .models import Workshop


class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('date','teachers','time')


admin.site.register(Workshop, WorkshopAdmin)
