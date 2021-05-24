# import datetime
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from herdi.fields import ArrayField


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
    user = models.ForeignKey("users.User", blank=True, null=True, on_delete=models.PROTECT)
    price = models.ForeignKey("project.PriceOption", on_delete=models.PROTECT)
    times = models.ManyToManyField("project.TimeOption")
    comment = models.TextField(max_length=350, null=True, blank=True)
    comment_response = models.TextField(max_length=350, null=True, blank=True)
    accepted_policy = models.BooleanField(default=False)
    status = models.CharField(max_length=15, choices=BOOKINGSTATUS, default="PE", null=True, blank=True,)
    note = models.TextField(max_length=1000, null=True, blank=True)
    booked_at = models.DateTimeField(auto_now_add=True)
    informed_at = models.DateTimeField(null=True, blank=True)

    # Gets names from TimeOption
    def get_times(self):
        return ",\n".join([p.name for p in self.times.all()])

    def get_user(self):
        if self.user:
            return self.user

        if hasattr(self, 'bookuserinfo'):
            return self.bookuserinfo

        raise AttributeError("No user information in booking")

    def flags(self):
        flags = {
            "user": (lambda x: True if x.user is not None else False)(self),
            "comment": (lambda x: True if (x.comment is not None) and (x.comment != '') else False)(self),
            "response": (lambda x: True if (x.comment_response is not None) and (x.comment != '') else False)(self)
        }
        return flags

    def get_user_email(self):
        return self.get_user().email

    def get_user_phone(self):
        return self.get_user().phone

    def get_user_name(self):
        user = self.get_user()
        return "{} {}".format(user.first_name, user.last_name)

    def get_user_pk(self):
        return self.get_user().pk

    def __str__(self):
        return "%s: %s - %s" % (self.pk, self.event.title, self.get_user_name())


class BookUserInfo(models.Model):
    book = models.OneToOneField("booking.Book", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", blank=True, null=True, on_delete=models.PROTECT)
    first_name = models.CharField(_("first name"), max_length=30, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(_("email address"), blank=True, null=True)


# TODO: If booking gets updated to an User remove the UserInfo associated
def create_userinfo(sender, instance, created, *args, **kwargs):
    """
    Make sure that if there is no user in the booking we have an associated
    userinfo to be filled in
    """
    if created and (instance.user is None):
        BookUserInfo.objects.create(book=instance)


post_save.connect(create_userinfo, sender=Book)


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
        return "%s - %s" % (self.book.event.title, self.book.get_user_name(),)

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
