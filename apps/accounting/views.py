from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import gettext as _
from django.shortcuts import render

from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from booking.utils import (
    build_url,
    email_sender,
    staff_check,
)

from booking.services import updateBookStatus, createNextBookAttendance

from accounting.models import Invoice
from accounting.filters import AccountFilter
from accounting.forms import UpdateInvoiceForm
from accounting.services import get_invoice

# Create your views here.


@login_required
@user_passes_test(staff_check)
def accountinglistview(request):
    template = "accounting/accounting_list.html"
    accounting_filter = AccountFilter(
        request.GET, queryset=(Invoice.objects.all().select_related("book").order_by("-id")),
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

    # TODO: acctions with various invoices
    if request.method == "POST":
        #  checked_list = request.POST.getlist("check")
        if "create" in request.POST:
            pass

    return render(request, template, context)


class InvoiceUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Invoice
    template_name = "accounting/accounting_update.html"
    form_class = UpdateInvoiceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_filter = AccountFilter(self.request.GET, queryset=(Invoice.objects.all().select_related("book")),)

        context["account_filter"] = account_filter
        paginator = Paginator(account_filter.qs, 24)  # Show 25 contacts per page.
        page = self.request.GET.get("page")
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)
        context["page_obj"] = response
        context["filter"] = self.request.GET
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        invoice = get_invoice(instance.id)

        if "update" in self.request.POST:
            if invoice.book:
                if (invoice.status == "PE") and (instance.status == "PY"):  # Pending to Payed
                    try:
                        email_sender(instance, "Paid")
                    except Exception as e:
                        messages.add_message(self.request, messages.WARNING, _("Error in Email: " + e))
                    else:
                        messages.add_message(self.request, messages.INFO, _("Paid Email sent"))

                    try:
                        updateBookStatus(instance.book.id, "PA")  # Update to Participant
                    except Exception as e:
                        messages.add_message(
                            self.request, messages.WARNING, _(
                                "Error updating booking N°" + str(instance.book.id + " : " + e)
                            )
                        )
                    else:
                        messages.add_message(self.request, messages.INFO, _("Updated status Booking"))

                    # Multiple Cycles
                    if invoice.book.price.cycles > 1:
                        try:
                            createNextBookAttendance(invoice.book.id)
                        except Exception as e:
                            messages.add_message(
                                self.request, messages.WARNING, _("Error creating Next Booking for Abo: " + e)
                            )
                        else:
                            messages.add_message(self.request, messages.INFO, _("Booking and Attendance created"))

                elif (invoice.status == "PE" or "PY") and (instance.status == "CA"):

                    # Check if any Attendance True
                    if invoice.book.attendance.count_attendance() < 1:
                        try:
                            updateBookStatus(instance.book.id, "CA")  # Update to Canceled
                        except Exception as e:
                            messages.add_message(
                                self.request, messages.WARNING, _(
                                    "Error updating booking N°" + str(instance.book.id + " : " + e)
                                )
                            )
                        else:
                            messages.add_message(self.request, messages.INFO, _("Updated status Booking"))
                    else:
                        messages.add_message(self.request, messages.WARNING, _("Can't Update"))

            instance.save()
        return super().form_valid(form)

    # TODO: There is probably a way to get all the GETs and process them?
    def get_success_url(self, **kwargs):
        user = self.request.GET.get("book__user", "")
        event = self.request.GET.get("book__event", "")
        status = self.request.GET.get("status", "")
        date = self.request.GET.get("pay_till", "")
        pk = self.object.id
        url = build_url(
            "accounting_update",
            get={"book__user": user, "book__event": event, "status": status, "pay_till": date},
            pk={"pk": pk},
        )
        return url

    def test_func(self):
        return staff_check(self.request.user)
