from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import gettext as _
from django.shortcuts import render

from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from booking.utils import (
    build_url,
    staff_check,
)

from accounting.services import (
    invoice_get,
    invoice_send_paid,
    invoice_reminder,
)

from booking.services import update_book_status

from accounting.models import Invoice
from accounting.filters import AccountFilter
from accounting.forms import InvoiceUpdateForm

# Create your views here.


@login_required
@user_passes_test(staff_check)
def accountinglistview(request):
    template = "accounting/accounting_list.html"
    accounting_filter = AccountFilter(
        request.GET, queryset=(
            Invoice.objects.filter(balance="CR").select_related("book__user", "book__event").order_by("-id")
        )
    )

    # Pagination
    paginator = Paginator(accounting_filter.qs, 24)  # Show 24 contacts per page.
    page = request.GET.get("page")
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    # End Paginator

    context = {
        "account_filter": accounting_filter,
        "filter": request.GET,
        "page_obj": response,
    }

    return render(request, template, context)


class InvoiceUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Invoice
    template_name = "accounting/accounting_update.html"
    form_class = InvoiceUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accounting_filter = AccountFilter(
            self.request.GET, queryset=(
                Invoice.objects.all().select_related("book__user", "book__event").order_by("-id")
            )
        )

        # Paginator
        paginator = Paginator(accounting_filter.qs, 24)  # Show 24 contacts per page.
        page = self.request.GET.get("page")
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        context["account_filter"] = accounting_filter
        context["page_obj"] = response
        context["filter"] = self.request.GET

        return context

    def form_valid(self, form):
        print("Get to form_valid")
        instance = form.save(commit=False)

        # Get the invoice before save
        invoice = invoice_get(instance.id)

        if "update" in self.request.POST:
            if invoice.book and (invoice.status != instance.status):
                # To Paid
                if (invoice.status == "PE") and (instance.status == "PY"):

                    # Send Paid email
                    try:
                        invoice_send_paid(instance)
                    except Exception as e:
                        messages.add_message(self.request, messages.WARNING, _("Error in email: " + e))
                    else:
                        messages.add_message(self.request, messages.INFO, _("Paid email sent"))

                    # Update related book status
                    try:
                        update_book_status(instance.book.id, "PA")  # Update to Participant
                    except Exception as e:
                        messages.add_message(
                            self.request, messages.WARNING, _(
                                "Error Book N°" + str(instance.book.id + " : " + e)
                            )
                        )
                    else:
                        messages.add_message(self.request, messages.INFO, _("Updated status booking"))

                # To First Reminder
                elif (invoice.status in ("PE", "FR", "SR")) and (instance.status in ("FR", "SR", "TR")):

                    # Send Reminder email
                    try:
                        invoice_reminder(instance, invoice)
                    except Exception as e:
                        messages.add_message(self.request, messages.WARNING, str(e))
                    else:
                        messages.add_message(self.request, messages.SUCCESS, _("Reminder sent."))

                # To Canceled
                elif (invoice.status in ("PE", "PY")) and (instance.status == "CA"):

                    # Check if no Attendance
                    if not invoice.book.attendance.count_attendance():
                        try:
                            update_book_status(instance.book.id, "CA")
                        except Exception as e:
                            messages.add_message(
                                self.request, messages.WARNING, _(
                                    "Error updating booking N°" + str(instance.book.id + " : " + e)
                                )
                            )
                        else:
                            messages.add_message(
                                self.request, messages.INFO, _("Updated status Booking, Attendance Pending"))
                    else:
                        messages.add_message(self.request, messages.WARNING, _("Can't Update. Open Attendance"))

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        pk = self.object.id
        url = build_url(
            "accounting_update",
            get=self.request.GET.items(),
            pk={"pk": pk},
        )
        return url

    def test_func(self):
        return staff_check(self.request.user)
