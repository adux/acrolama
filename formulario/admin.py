from django.contrib import admin


# Register your models here.

from .models import Fest

class FestAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'name', 'email','numero', 'address', 'option', 'allergies')
    list_filter = ('datetime', 'option')
    search_fields = ('name', 'email')


admin.site.register(Fest, FestAdmin)
