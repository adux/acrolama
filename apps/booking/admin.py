from django import forms
from django.contrib import admin
from django.db import models
from .models import Book, Attendance
from booking.fields import ArrayField


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
    list_filter = ["event__category", "event__level", "status"]
    search_fields = [
        "event__title",
        "user__email",
        "user__last_name",
        "user__first_name",
        "note",
        "status",
    ]
    list_select_related = [
        "user",
        "price",
        "event",
        "event__level",
    ]

    def get_queryset(self, request):
        return (
            super(BookAdmin, self)
            .get_queryset(request)
            .prefetch_related("times")
        )

    save_as = True


class AttendanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(
            *args, **kwargs
        )  # populate the post
        self.fields["book"].queryset = Book.objects.select_related(
            "user", "event", "event__level"
        )

    # class Meta:
    #     exclude = ['book']

    # TODO: Make this global for all admin
    class Media:
        js = ("booking/project.js",)
        css = {"all": ("booking/project.css",)}


class AttendanceAdmin(admin.ModelAdmin):
    form = AttendanceForm
    # formfield_overrides = {
    #     ArrayField: {'widget': forms.TextInput},
    # }
    list_display = [
        "id",
        "book",
    ]
    list_select_related = [
        "book",
        "book__user",
        "book__event",
        "book__event__level",
    ]

    def get_queryset(self, request):
        return (
            super(AttendanceAdmin, self)
            .get_queryset(request)
            .prefetch_related("book__times")
        )


admin.site.register(Book, BookAdmin)
admin.site.register(Attendance, AttendanceAdmin)
