import datetime

from django.db import models
from django.db.models.signals import pre_save


from project.models import Irregularity, TimeOption

from booking.utils import datelistgenerator

#Original would be from postgres.field fields looks for other widgets
# from django.contrib.postgres.fields import ArrayField
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

    def get_check(self, date):
        for num, d in enumerate(self.attendance_date):
            if d == date:
                return self.attendance_check[num]

    def get_num(self, date):
        for num, d in enumerate(self.attendance_date):
            if d == date:
                return num

    def count_attendance(self):
        count = 0
        for position, check in enumerate(self.attendance_check):
            if check == True:
                count += 1
        return count


class Quotation(models.Model):
    event = models.ForeignKey("project.Event", on_delete=models.CASCADE)
    time_location = models.ForeignKey("project.TimeLocation", on_delete=models.CASCADE)
    teachers = models.ManyToManyField("users.User")

    #Costs
    related_rent = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    direct_costs = models.ManyToManyField("accounting.Invoice")

    #Revenue
    total_attendees = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    direct_revenue = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    #Profit
    fix_profit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    acrolama_profit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    teachers_profit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    #Control
    locked = models.BooleanField(default=False)
    locked_at = models.DateTimeField(blank=True, null=True)

    #Info
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_teachers(self):
        return ",\n".join([p.name for p in self.teachers.all()])
