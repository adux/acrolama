import datetime

from django.db import models
from django.db.models.signals import pre_save
# from django.contrib.postgres.fields import ArrayField

from project.models import Irregularity, TimeOption

from booking.utils import datelistgenerator
from booking.fields import ArrayField


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
        return "%s: %s - %s %s" % (
            self.pk,
            self.event,
            self.user.first_name,
            self.user.last_name,
        )


class Attendance(models.Model):
    """
    Contains the dates a Person should participate depending on the booking they did
    TODO: This could be done with JSON.
    Not to much to use those, nor see the practical advantage now.
    TODO: num should be position
    """
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    attendance_date = ArrayField(models.DateField())
    attendance_check = ArrayField(models.BooleanField())

    def __str__(self):
        return "%s - %s" % (self.book.event, self.book.user,)

    def get_date_today(self):
        for num, date in enumerate(self.attendance_date):
            if date == datetime.datetime.now().date():
                return date

    def get_check_today(self):
        for num, date in enumerate(self.attendance_date):
            if date == datetime.datetime.now().date():
                return self.attendance_check[num]

    def get_num_today(self):
        for num, date in enumerate(self.attendance_date):
            if date == datetime.datetime.now().date():
                return num

    def count_attendance(self):
        count = 0
        for position,check in enumerate(self.attendance_check):
            if check == True:
                count += 1
        return count
