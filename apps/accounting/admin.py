from django.contrib import admin
from .models import (
    Account,
    Invoice,
    Payment,
    Partner,
    Transaction,
)

admin.site.register(Account)
admin.site.register(Invoice)
admin.site.register(Payment)
admin.site.register(Partner)
admin.site.register(Transaction)
# Register your models here.
