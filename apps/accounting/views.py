from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import gettext as _


from django.views.generic import (
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from booking.utils import (
    teacher_check,
    staff_check,
)

from accounting.models import Invoice
from accounting.filters import AccountFilter
from accounting.forms import UpdateInvoiceForm

# Create your views here.

def accountinglistview(request):
    template = "accounting/accounting_list.html"
    accounting_filter = AccountFilter(
        request.GET,
        queryset=(
            Invoice.objects.all()
        ),
    )

    # Pagination
    paginator = Paginator(accounting_filter.qs, 15)  # Show 25 contacts per page.
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

    if request.method == "POST":
        checked_list = request.POST.getlist("check")
        if "create" in request.POST:
            pass

    return render(request, template, context)


class InvoiceUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Invoice
    template_name = "accounting/accounting_update.html"
    form_class = UpdateInvoiceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_filter = AccountFilter(
            self.request.GET,
            queryset=(
                Invoice.objects.all()
            ),
        )

        context["account_filter"] = account_filter
        paginator = Paginator(
            account_filter.qs, 20
        )  # Show 25 contacts per page.
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

        if "update" in self.request.POST:
            instance.save()
        elif "create" in self.request.POST:
            pass
        return super().form_valid(form)

    # TODO: There is probably a way to get all the GETs and process them?
    def get_success_url(self, **kwargs):
        url = build_url(
            "booking_update",
            get={"user": user, "event": event, "status": status},
            pk={"pk": pk},
        )
        return url

    def test_func(self):
        return staff_check(self.request.user)
