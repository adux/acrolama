from django.contrib import admin
from .models import Book, Attendance


class BookAdmin(admin.ModelAdmin):
    list_display = [
        "event__fulltitle",
        "user",
        "price",
        "get_times",
        "status",
        "note",
        "booked_at",
    ]
    list_filter = ["event__category", "event__level", "status"]
    search_fields = [
        "event__title",
        "user__email",
        "user__last_name",
        "user__first_name",
        "note",
        "status",
    ]
    save_as = True


class AttendanceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "book",
    ]


admin.site.register(Book, BookAdmin)
admin.site.register(Attendance, AttendanceAdmin)
