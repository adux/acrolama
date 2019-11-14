from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = [
        "event",
        "user",
        "price",
        "get_times",
        "status",
        "note",
        "booked_at",
    ]

    list_filter = ["event", "event__level", "status"]

    search_fields = [
        "event__title",
        "user__email",
        "user__last_name",
        "user__first_name",
        "note",
        "status",
    ]

    save_as = True


admin.site.register(Book, BookAdmin)
