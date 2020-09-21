from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.utils.translation import ugettext as _
from django.urls import reverse

from django.core.exceptions import ValidationError

from home.utils import unique_slug_generator
from home.services import createInfoFromPolicy

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
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s | " % (self.name) + " - ".join(str(p.first_name) for p in self.manager.all())


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
    address = models.ForeignKey("address.Address", on_delete=models.CASCADE)
    image = models.ForeignKey("audiovisual.Image", on_delete=models.CASCADE)
    max_capacity = models.PositiveIntegerField(default=2, null=True, blank=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    indication = models.TextField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return "%s" % (self.name)


class TimeLocation(models.Model):
    """
    time_options as a many to many was not the best desition ever probably
    it spears no practical time nor space
    """

    name = models.CharField(max_length=120, null=True, blank=True)
    time_options = models.ManyToManyField(TimeOption)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def get_times(self):
        return ",\n".join([p.name for p in self.time_options.all()])

    def __str__(self):
        if self.name is None:
            return str(self.location)
        else:
            return self.name


def timelocation_post_save(sender, instance, *args, **kwargs):
    """
    Solution for recursion to tho the save.
    """
    if not instance:
        return

    if hasattr(instance, '_dirty'):
        return

    instance.name = " - ".join(str(p) for p in instance.time_options.all()) + " | %s" % (instance.location)

    try:
        instance._dirty = True
        print("post_save")
        instance.save()
    finally:
        print("post_dirty")
        del instance._dirty


post_save.connect(timelocation_post_save, sender=TimeLocation)


def timelocation_m2m_change(sender, instance, *args, **kwargs):
    """
    Will call two times the post_save since its saving
    """
    if kwargs.get('action') in {'post_add', 'post_remove'}:
        print(kwargs.get('action'))
        pk_set = kwargs.pop('pk_set', None)
        b = [TimeOption.objects.get(pk=pk) for pk in pk_set]
        instance.name = " - ".join(str(p) for p in b) + " | %s" % (instance.location)
        instance.save()


m2m_changed.connect(timelocation_m2m_change, sender=TimeLocation.time_options.through)


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
    cycles = models.IntegerField(verbose_name="Numbero of Cycles", default=0)

    # Info
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    price_chf = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_euro = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    days_till_pay = models.IntegerField(verbose_name="Days to Pay", default=10)
    published = models.BooleanField(default=False)

    def __str__(self):
        if self.price_euro:
            return "%s, EUR: %s - CHF: %s" % (
                self.name,
                self.price_euro,
                self.price_chf,
            )
        else:
            return "%s, CHF: %s" % (self.name, self.price_chf)

    def clean(self):
        if self.duo and self.single_date:
            raise ValidationError(
                _("Can't be 'Duo' and 'Single Date'"),
                code='invalid',
            )
        if self.single_date and self.cycles > 0:
            raise ValidationError(
                _("Can't usr 'Single date' with Cycle Abos"),
                code='invalid',
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
    createInfoFromPolicy(instance)


pre_save.connect(policy_pre_save_url, sender=Policy)


class Event(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=EVENTCATEGORY)
    cycle = models.IntegerField(default=0, choices=CYCLE, blank=True, null=True)
    title = models.CharField(max_length=100)
    event_startdate = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    event_enddate = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    description = models.TextField(max_length=3000)
    time_locations = models.ManyToManyField(TimeLocation)
    irregularities = models.ManyToManyField(Irregularity, blank=True)
    price_options = models.ManyToManyField(PriceOption)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    max_participants = models.PositiveIntegerField(default=2, null=True, blank=True)
    images = models.ManyToManyField("audiovisual.Image")
    videos = models.ManyToManyField("audiovisual.Video", blank=True)
    level = models.ForeignKey(Level, null=True, blank=True, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, null=True, blank=True, on_delete=models.CASCADE)
    prerequisites = models.TextField(max_length=2000, null=True, blank=True)
    teachers = models.ManyToManyField("users.User", related_name="eventteacher")
    highlights = models.TextField(max_length=2000, null=True, blank=True)
    included = models.TextField(max_length=2000, null=True, blank=True)
    food = models.TextField(max_length=2000, null=True, blank=True)
    team = models.ManyToManyField("users.User", related_name="eventteam", blank=True)
    published = models.BooleanField()
    registration = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    # class Meta:
    #     ordering = [""]

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
