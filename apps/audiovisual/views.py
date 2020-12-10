from django.contrib import messages
from django.utils.translation import gettext as _

from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from herdi.utils import (
    build_url,
    herd_check,
)


from audiovisual.models import Image
from audiovisual.forms import ImageCreateForm

# Create your views here.


class ImageCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Image
    template_name = "audiovisual/image_create.html"
    form_class = ImageCreateForm

    def get_success_url(self, **kwargs):
        success_url = build_url(
            "event_list",
        )
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("Book created, we'll get back to you soon!"),
        )
        return success_url

    def test_func(self):
        return herd_check(self.request.user)
