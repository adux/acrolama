from django.contrib import admin
from .models import Invoice, Partner


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "balance", "partner", "book", "referral_code", "status")


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Partner)
# Register your models here.
