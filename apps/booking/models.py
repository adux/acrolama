# import datetime
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save

# Original would be from postgres.field, booking.fields looks for other widgets
# from django.contrib.postgres.fields import ArrayField
from booking.fields import ArrayField

from django.utils.translation import ugettext_lazy as _


BOOKINGSTATUS = [
    ("PE", "Pending"),
    ("WL", "Waiting List"),
    ("IN", "Informed"),
    ("PA", "Participant"),
    ("CA", "Canceled"),
    ("SW", "Switched"),
]


class Book(models.Model):
    event = models.ForeignKey("project.Event", on_delete=models.PROTECT)
    user = models.ForeignKey("users.User", on_delete=models.PROTECT)
    price = models.ForeignKey("project.PriceOption", on_delete=models.PROTECT)
    times = models.ManyToManyField("project.TimeOption")
    comment = models.TextField(max_length=350, null=True, blank=True)
    accepted_policy = models.BooleanField(default=False)
    status = models.CharField(max_length=15, choices=BOOKINGSTATUS, default="PE", null=True, blank=True,)
    note = models.TextField(max_length=1000, null=True, blank=True)
    booked_at = models.DateTimeField(auto_now_add=True)
    informed_at = models.DateTimeField(null=True, blank=True)

    # Gets names from TimeOption
    def get_times(self):
        return ",\n".join([p.name for p in self.times.all()])

    def __str__(self):
        return "%s: %s - %s" % (self.pk, self.event.title, self.user.get_full_name())


class BookDuoInfo(models.Model):
    book = models.OneToOneField("booking.Book", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", blank=True, null=True, on_delete=models.PROTECT)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(_("email address"), blank=True)


class BookDateInfo(models.Model):
    book = models.OneToOneField("booking.Book", on_delete=models.CASCADE)
    single_date = models.DateField(auto_now_add=False, auto_now=False, blank=True)


class Attendance(models.Model):
    """
    Contains the dates a Person should participate depending on the booking they did

    NOTE: This could be done with JSON. But to make us of date operations its better to have an Array that can
    store them in date format. If done with JSON we would have to transform and parse the date constantly.
    """
    book = models.OneToOneField("booking.Book", on_delete=models.PROTECT)
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
            if check:
                count += 1
        return count

    def count_dates(self):
        count = 0
        for position, date in enumerate(self.attendance_date):
            if date:
                count += 1
        return count


class Quotation(models.Model):
    event = models.ForeignKey("project.Event", on_delete=models.PROTECT)
    time_location = models.ForeignKey("project.TimeLocation", on_delete=models.PROTECT)
    teachers = models.ManyToManyField("users.User")

    # Costs
    related_rent = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    direct_costs = models.ManyToManyField("accounting.Invoice")

    # Revenue
    total_attendees = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    direct_revenue = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Profit
    fix_profit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    admin_profit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    partner_profit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Control
    locked = models.BooleanField(default=False)
    locked_at = models.DateTimeField(blank=True, null=True)

    # Info
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.check_duplicate()
        super(Quotation, self).save(*args, **kwargs)

    def get_teachers(self):
        return ",\n".join([p.first_name for p in self.teachers.all()])

    def check_duplicate(self):
        if Quotation.objects.filter(
                event=self.event, time_location=self.time_location
        ).exists():
            raise Exception(_("Quotation with this Event and Time Location allready exists"))


class AboCounter(models.Model):
    """
    TODO: We need to re think this since now space aint a problem anymore we might
    want to keep a register of all the bookings associated to a AboCounter
    Json should have the form
    data={
        'count': 0,
        'first_book': '123', #number of the first booking
        'last_book': '123',
    }
    """
    data = JSONField()


def aboutcounter_post_save(sender, instance, *args, **kwargs):
    if instance.data['count'] < 1:
        instance.delete()


post_save.connect(aboutcounter_post_save, sender=AboCounter)
