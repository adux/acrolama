from django.urls import path

from accounting.views import (
    accountinglistview,
    InvoiceUpdateView,
)

urlpatterns = [
    # Accounting
    path("invoices/", accountinglistview, name="accounting_list"),
    path("invoice/<int:pk>/update/", InvoiceUpdateView.as_view(), name="accounting_update"),
]
