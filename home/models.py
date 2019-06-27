from datetime import datetime, timedelta
from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from home.utils import unique_slug_generator
from django.utils.translation import ugettext as _

User = settings.AUTH_USER_MODEL

# Static Content of Webpage
# Start About Section
class About(models.Model):
    description = models.TextField(max_length=1000)


class AboutImage(models.Model):
    general = models.ForeignKey(About, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="about/general/")


class AboutMember(models.Model):
    name = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    content = models.TextField(max_length=1000)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="about/member/")

    def __str__(self):
        return self.name


class AboutDate(models.Model):
    start = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    description = models.CharField(max_length=50)

    def yearstart(self):
        return self.start.strftime("%b %Y")

    def yearend(self):
        return self.end.strftime("%Y")

    def __str__(self):
        return self.description


# End About Section


# Start FAQ Section
class Faq(models.Model):
    question = models.CharField(max_length=300, null=True, blank=True)
    answer = models.TextField(max_length=2000, null=True, blank=True)


class FaqValues(models.Model):
    image = models.CharField(max_length=15, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.CharField(max_length=120, null=True, blank=True)


# End FAQ Section


# Start Variable Info Pages
class Info(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=5000, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)


def info_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(info_pre_save_receiver, sender=Info)


class InfoImage(models.Model):
    general = models.ForeignKey(Info, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="info/")


# End Info Pages


class NewsList(models.Model):
    email = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)
    inscribed_at = models.DateField(auto_now_add=True)


class Portfolio(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.CharField(max_length=1, blank=True, null=True)
    text = models.TextField(max_length=30, blank=True, null=True)
    sec_text = models.TextField(max_length=30, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.ImageField(upload_to="portfolio/")


class Testimonial(models.Model):
    text = models.TextField(max_length=350)
    author = models.CharField(max_length=30)

    def __str__(self):
        return self.text


# Proyectos
# Events
class Event(models.Model):
    Icon = (
        ("fas fa-redo", "Masterclass"),
        ("fas fa-rocket", "Festival"),
        ("fas fa-cogs", "Cycle"),
        ("fas fa-cog", "Workshop"),
        ("fas fa-star", "Camp"),
        ("fas fa-seedling", "Retreat"),
    )
    Ocurrance = (
        ("Mon", "Monday's"),
        ("Tue", "Tuesday's"),
        ("Wed", "Wednesday's"),
        ("Thu", "Thursday's"),
        ("Fri", "Friday's"),
        ("Sun", "Sunday's"),
        ("WedSun.", "Wed. & Sunday's"),
        ("TueSun.", "Tue. & Sunday's"),
        ("Year", "Yearly"),
        ("One", "One Time"),
    )
    Level = (
        ("A", "Advanced"),
        ("B", "Intermediate"),
        ("C", "Introduction"),
        ("Z", "Multilevel"),
    )
    cat = models.CharField(max_length=15, choices=Icon, default=1)
    level = models.CharField(max_length=1, choices=Level, default=1)
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=3000)
    prerequisites = models.TextField(max_length=1000, null=True, blank=True)
    loc = models.CharField(max_length=60)
    loc_extra = models.CharField(max_length=60, null=True, blank=True)
    city = models.CharField(max_length=20)
    ocurrance = models.CharField(max_length=8, choices=Ocurrance, null=True, blank=True)
    datestart = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    # Why did i need this ?
    dateextra = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    dateend = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    price = models.CharField(max_length=20, null=True, blank=True)
    publication = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    published = models.BooleanField()
    registration = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def get_datestart(self):
        if self.datestart.strftime("%b") == self.dateend.strftime(
            "%b"
        ) and self.dateend.strftime("%d %b") != self.datestart.strftime("%d %b"):
            return self.datestart.strftime("%d")
        else:
            return self.datestart.strftime("%d %b")

    def get_dateend(self):
        if self.dateend.strftime("%d %b") == self.datestart.strftime("%d %b"):
            return self.dateend.strftime("")
        else:
            return self.dateend.strftime(" - %d. %b %Y")

    def get_timestart(self):
        return self.datestart.strftime("%H:%M")

    def get_timeend(self):
        return self.dateend.strftime("%H:%M")

    def get_timeextra(self):
        return self.dateextra.strftime("%H:%M")

    def __str__(self):
        return self.title


""" Signal of Django to generate slug if not created  """


def event_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(event_pre_save_receiver, sender=Event)


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="event/")


class Booking(models.Model):
    Abo = [
        ("SS", "Single Season Abo"),
        ("DS", "Double Season Abo"),
        ("SC", "Single Cycle Abo"),
        ("DC", "Double Cycle Abo"),
        ("ST", "Single Day Ticket"),
    ]
    Category = [
        ("EI", "Einkommen"),
        ("KO", "Kosten"),
        ("AU", "Ausgaben"),
        ("IN", "Inversion"),
        ("LO", "Lohn"),
        ("SP", "Spargeld"),
    ]
    Reduction = [("ST", "Student Price"), ("NM", "Normal Price")]
    Day = [
        ("Wed", "Wednesday's"),
        ("Tue", "Tuesday's"),
        ("Sun", "Sunday's"),
        ("WedSun.", "Wed. & Sunday's"),
        ("TueWed.", "Tue. & Wednesday's"),
        ("TueSun.", "Tue. & Sunday's"),
    ]
    Status = [
        ("IN", "Informed"),
        ("CA", "Canceled"),
        ("PA", "Payed"),
        ("PE", "Pending"),
        ("SW", "Switched"),
    ]
    Method = [
        ("BT", "Bank"),
        ("TW", "Twint"),
        ("PP", "PayPal"),
        ("CS", "Cash"),
        ("CR", "Credit Card"),
        ("UN", "Unclasified"),
    ]
    category = models.CharField(max_length=10, choices=Category, default="EI")
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    abo = models.CharField(max_length=8, choices=Abo, null=True, blank=True)
    day = models.CharField(max_length=8, choices=Day, null=True, blank=True)
    reduction = models.CharField(
        max_length=12, choices=Reduction, null=True, blank=True
    )
    option = models.CharField(max_length=50, null=True, blank=True)
    comment = models.TextField(max_length=350, null=True, blank=True)
    amount = models.CharField(max_length=30, null=True, blank=True)
    pay_till = models.DateField(
        auto_now_add=False, auto_now=False, null=True, blank=True
    )
    pay_date = models.DateField(
        auto_now_add=False, auto_now=False, null=True, blank=True
    )
    methode = models.CharField(
        max_length=15, choices=Method, default="UN", null=True, blank=True
    )
    status = models.CharField(max_length=15, choices=Status, null=True, blank=True)
    note = models.TextField(max_length=1000, null=True, blank=True)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.event, self.name)


# Contabilidad
class Accounting(models.Model):
    Category = [
        ("EI", "Einkommen"),
        ("KO", "Kosten"),
        ("AU", "Ausgaben"),
        ("IN", "Inversion"),
        ("LO", "Lohn"),
        ("SP", "Spargeld"),
    ]
    Status = [
        ("IN", "Informed"),
        ("CA", "Canceled"),
        ("PA", "Payed"),
        ("PE", "Pending"),
        ("SW", "Switched"),
    ]
    Method = [
        ("BT", "Bank"),
        ("TW", "Twint"),
        ("PP", "PayPal"),
        ("CS", "Cash"),
        ("CR", "Credit Card"),
        ("UN", "Unclasified"),
    ]
    category = models.CharField(max_length=10, choices=Category)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.CharField(max_length=9)
    pay_till = models.DateField(
        auto_now_add=False, auto_now=False, null=True, blank=True
    )
    pay_date = models.DateField(
        auto_now_add=False, auto_now=False, null=True, blank=True
    )
    methode = models.CharField(
        max_length=15, choices=Method, default="UN", null=True, blank=True
    )
    status = models.CharField(max_length=15, choices=Status, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    degistered_at = models.DateTimeField(auto_now_add=True)
