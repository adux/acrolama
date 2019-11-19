from django.db import models
from django.db.models.signals import pre_save


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
