import datetime

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.translation import ugettext as _
from django.utils.functional import cached_property
from django.urls import reverse

from django.core.exceptions import ValidationError

from home.utils import unique_slug_generator
from home.services import create_info_from_policy

# Reference Data

EVENTCATEGORY = [
    ("MC", "Masterclass"),
    ("FT", "Festival"),
    ("CY", "Cycle"),
    ("WS", "Workshop"),
    ("CA", "Camp"),
    ("RT", "Retreat"),
]

EXCEPTIONCATEGORY = [
    ("TI", "Time"),
    ("LO", "Location"),
    ("TL", "TimeLocation"),
]

LEVEL = [
    ("0", "Multilevel"),
    ("1", "Introduction"),
    ("2", "Intermediate I"),
    ("3", "Intermediate II"),
    ("4", "Advanced"),
    ("5", "Profesional"),
]

CYCLE = [(i, i) for i in range(13)]

DAYS = [
    ("0", "Monday"),
    ("1", "Tuesday"),
    ("2", "Wednesday"),
    ("3", "Thursday"),
    ("4", "Friday"),
    ("5", "Saturday"),
    ("6", "Sunday"),
]


# FIXME: To be deleted.
class Day(models.Model):
    day = models.CharField(max_length=10, choices=DAYS)

    def __str__(self):
        return "%s" % (self.get_day_display())


class Project(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=2000)
    manager = models.ManyToManyField("users.User")
    public_chat_link = models.CharField(max_length=120, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % (self.name)


class TimeOption(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    regular_day = models.CharField(max_length=10, choices=DAYS, blank=True, null=True)
    class_starttime = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    class_endtime = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    open_starttime = models.TimeField(auto_now=False, auto_now_add=False)
    open_endtime = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        # return "%s" % (self.name)
        # Classes will have regular days
        if self.regular_day:
            return "%s, %s: %s - %s" % (
                self.name,
                self.get_regular_day_display(),
                self.class_starttime.strftime("%H:%M"),
                self.class_endtime.strftime("%H:%M"),
            )
        # Events should not have and Name is used
        else:
            return "%s: %s - %s" % (
                self.name,
                self.open_starttime.strftime("%H:%M"),
                self.open_endtime.strftime("%H:%M"),
            )

    def get_class_start_times(self):
        if self.class_starttime is not None:
            return "%s - %s" % (
                self.class_starttime.strftime("%H:%M"),
                self.class_endtime.strftime("%H:%M"),
            )
        else:
            return None

    def get_open_start_times(self):
        return "%s - %s" % (
            self.open_starttime.strftime("%H:%M"),
            self.open_endtime.strftime("%H:%M"),
        )


class Location(models.Model):
    name = models.CharField(max_length=120)
    address = models.ForeignKey("address.Address", on_delete=models.PROTECT)
    image = models.ForeignKey("audiovisual.Image", on_delete=models.PROTECT)
    max_capacity = models.PositiveIntegerField(default=2, null=True, blank=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    indication = models.TextField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return "%s" % (self.name)


class TimeLocation(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    time_option = models.ForeignKey(TimeOption, on_delete=models.PROTECT, related_name="timelocation")
    location = models.ForeignKey(Location, on_delete=models.PROTECT)

    def __str__(self):
        if self.name is None:
            return str(self.location)
        else:
            return self.name

    def capsule(self):
        cap = {
            "location": self.location,
            "regular_day": self.time_option.get_regular_day_display(),
            "open_starttime": self.time_option.open_starttime,
            "open_endtime": self.time_option.open_endtime,
            "class_starttime": self.time_option.class_starttime,
            "class_endtime": self.time_option.class_endtime,
        }
        return cap


def timelocation_post_save(sender, instance, *args, **kwargs):
    """
    Solution for recursion to tho the save.
    """
    if not instance:
        return

    if hasattr(instance, "_dirty"):
        return

    instance.name = "{} | {}".format(instance.time_option, instance.location)

    try:
        instance._dirty = True
        instance.save()
    finally:
        del instance._dirty


post_save.connect(timelocation_post_save, sender=TimeLocation)


class Irregularity(models.Model):
    category = models.CharField(max_length=15, choices=EXCEPTIONCATEGORY)
    description = models.TextField(max_length=2000)
    time_location = models.ManyToManyField(TimeLocation)

    class Meta:
        verbose_name_plural = "Irregularities"

    def __str__(self):
        return "%s, %s" % (self.description, self.category)


class PriceOption(models.Model):
    # Options
    duo = models.BooleanField(default=False)
    single_date = models.BooleanField(default=False)
    cycles = models.IntegerField(verbose_name="Number of Cycles", default=0)

    # Info
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    price_chf = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_euro = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    days_till_pay = models.IntegerField(verbose_name="Days to Pay", default=10)
    published = models.BooleanField(default=False)

    def __str__(self):
        if self.price_euro and self.price_chf:
            return "{} - EUR{:.0f} - CHF{:.0f}".format(
                self.name,
                self.price_euro,
                self.price_chf,
            )
        else:
            return "%s - CHF %s" % (self.name, self.price_chf)

    def get_price(self):
        if self.price_euro:
            return "EUR {:.0f}.-".format(self.price_euro)
        else:
            return "CHF {:.0f}.-".format(self.price_chf)

    def clean(self):
        if self.duo and self.single_date:
            raise ValidationError(
                _("Can't be 'Duo' and 'Single Date'"),
                code="invalid",
            )
        if self.single_date and self.cycles > 0:
            raise ValidationError(
                _("Can't usr 'Single date' with Cycle Abos"),
                code="invalid",
            )
        if self.price_euro and not self.price_chf:
            raise ValidationError(
                _("For price in Euro, there needs to be a intern CHF price."),
                code="invalid",
            )


# Sport Info
class Level(models.Model):
    name = models.CharField(max_length=20, choices=LEVEL)
    description = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.get_name_display()


class Discipline(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name


class Policy(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=5000)

    class Meta:
        verbose_name_plural = "Policies"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("info", args=[str(self.name.replace(" ", ""))])


def policy_pre_save_url(sender, instance, *args, **kwargs):
    create_info_from_policy(instance)


pre_save.connect(policy_pre_save_url, sender=Policy)


class Event(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    category = models.CharField(max_length=50, choices=EVENTCATEGORY)
    cycle = models.IntegerField(default=0, choices=CYCLE, blank=True, null=True)
    title = models.CharField(max_length=100)
    event_startdate = models.DateField(auto_now=False, default=datetime.date.today)
    event_enddate = models.DateField(auto_now=False, default=datetime.date.today)
    description = models.TextField(max_length=3000)
    time_locations = models.ManyToManyField(TimeLocation)
    irregularities = models.ManyToManyField(Irregularity, blank=True)
    price_options = models.ManyToManyField(PriceOption)
    policy = models.ForeignKey(Policy, on_delete=models.PROTECT)
    max_participants = models.PositiveIntegerField(default=2, null=True, blank=True)
    images = models.ManyToManyField("audiovisual.Image", blank=True)
    videos = models.ManyToManyField("audiovisual.Video", blank=True)
    level = models.ForeignKey(Level, null=True, blank=True, on_delete=models.PROTECT)
    discipline = models.ForeignKey(Discipline, null=True, blank=True, on_delete=models.PROTECT)
    prerequisites = models.TextField(max_length=2000, null=True, blank=True)
    teachers = models.ManyToManyField("users.User", related_name="eventteacher")
    highlights = models.TextField(max_length=2000, null=True, blank=True)
    included = models.TextField(max_length=2000, null=True, blank=True)
    food = models.TextField(max_length=2000, null=True, blank=True)
    team = models.ManyToManyField("users.User", related_name="eventteam", blank=True)
    published = models.BooleanField(default=False)
    registration = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    # class Meta:
    #     ordering = [""]

    @cached_property
    def fulltitle(self):
        if self.category == "CY" and self.cycle:
            if self.level.name == "2":
                return "Cycle 0." + str(self.cycle) + " - " + self.title
            elif self.level.name == "3":
                return "Cycle " + str(self.cycle) + " - " + self.title
            else:
                return self.title

    def get_absolute_url(self):
        if self.category == "CY":
            return reverse("class", args=[str(self.slug)])
        else:
            return reverse("event", args=[str(self.slug)])

    def get_regular_days_list(self):
        regular_days = set()
        tls = self.time_locations.all()
        for tl in tls:
            if tl.time_option.regular_day:
                regular_days.add(tl.time_option.get_regular_day_display())
            else:
                return None
        return regular_days

    def get_timelocations_capsule(self):
        cap = []
        for obj in self.time_locations.all():
            print(obj.capsule())
            cap.append(obj.capsule())
        return cap

    def __str__(self):
        return "(%s) %s %s - %s" % (
            self.event_startdate.strftime("%d %b"),
            self.level,
            self.get_category_display(),
            self.title,
        )


def event_pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(event_pre_save_slug, sender=Event)
