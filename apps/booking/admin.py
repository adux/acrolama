from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = [
        "event",
        "user",
        "price",
        "time",
        "status",
        "note",
        "booked_at",
    ]

    list_filter = ["event", "user", "status"]
    seach_fields = ["event", "user", "note"]
    save_as = True


admin.site.register(Book, BookAdmin)
