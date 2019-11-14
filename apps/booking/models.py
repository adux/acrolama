from django.conf import settings

from django.db import models
from django.db.models.signals import pre_save

from django.core.mail import send_mail
from django.template.loader import render_to_string

from project.models import Irregularity


BOOKINGSTATUS = [
    ("PE", "Pending"),
    ("WL", "Waiting List"),
    ("IN", "Informed"),
    ("PA", "Participant"),
    ("CA", "Canceled"),
    ("SW", "Switched"),
]


class Book(models.Model):
    event = models.ForeignKey("project.Event", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    price = models.ForeignKey("project.PriceOption", on_delete=models.CASCADE)
    times = models.ManyToManyField("project.TimeOption")
    comment = models.TextField(max_length=350, null=True, blank=True)
    status = models.CharField(
        max_length=15,
        choices=BOOKINGSTATUS,
        default="PE",
        null=True,
        blank=True,
    )
    note = models.TextField(max_length=1000, null=True, blank=True)
    booked_at = models.DateTimeField(auto_now_add=True)

    # Gets names from TimeOption
    def get_times(self):
        return ",\n".join([p.name for p in self.times.all()])

    def __str__(self):
        return "%s - %s %s" % (
            self.event,
            self.user.first_name,
            self.user.last_name,
        )


def update_pre(sender, instance, **kwargs):
    pre_save_object = sender.objects.get(pk=instance.pk)

    # Taken from
    # https://stackoverflow.com/questions/2809547/creating-email-templates-with-django
    # Theres another Method with Multi wich helps for headers if needed

    if (pre_save_object.status == "PE") and (instance.status == "IN"):
        subject = "Acrolama - Confirmation - " + str(instance.event)
        sender = "notmonkeys@acrolama.com"
        to = [instance.user.email, "acrolama@acrolama.com"]
        irregularities = Irregularity.objects.filter(
            event__slug=instance.event.slug
        )
        print(instance.times)
        p = {
            "event": instance.event,
            "user": instance.user,
            "price": instance.price,
            "times": instance.times.all(),
            "irregularities": irregularities,
        }

        msg_plain = render_to_string(
            settings.BASE_DIR
            + "/apps/booking/templates/booking/email_informed.txt",
            p,
        )
        msg_html = render_to_string(
            settings.BASE_DIR
            + "/apps/booking/templates/booking/email_informed.html",
            p,
        )

        send_mail(subject, msg_plain, sender, to, html_message=msg_html)


pre_save.connect(update_pre, sender=Book)
# post_save.connect(save_post, sender=Book)
