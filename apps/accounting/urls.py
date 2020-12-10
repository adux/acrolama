from django.urls import path

from accounting.views import (
    accountinglistview,
    InvoiceUpdateView,
)

urlpatterns = [
    # Accounting
    path("", accountinglistview, name="accounting_list"),
    path("<int:pk>/", InvoiceUpdateView.as_view(), name="accounting_update"),
]
