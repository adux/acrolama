from django.db import models


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
    # USER
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    # OPTION
    price = models.ForeignKey("project.PriceOption", on_delete=models.CASCADE)
    time = models.ManyToManyField("project.TimeOption")
    # STATUS
    comment = models.TextField(max_length=350, null=True, blank=True)
    status = models.CharField(
        max_length=15, choices=BOOKINGSTATUS, null=True, blank=True
    )
    note = models.TextField(max_length=1000, null=True, blank=True)
    booked_at = models.DateTimeField(auto_now_add=True)

    # Gets names from TimeOption
    def get_times(self):
        return ",\n".join([p.name for p in self.time.all()])

    def __str__(self):
        return "%s - %s %s" % (
            self.event, self.user.first_name, self.user.last_name
        )
