from datetime import datetime, timedelta
from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from home.utils import unique_slug_generator
from django.utils.translation import ugettext as _

User = settings.AUTH_USER_MODEL

#abcdefghijklmnpqrstuvwxyz
#Static and Content
#Projects
#Accounting

COUNTRIES = [
    ('AD', _('Andorra')),
    ('AE', _('United Arab Emirates')),
    ('AF', _('Afghanistan')),
    ('AG', _('Antigua & Barbuda')),
    ('AI', _('Anguilla')),
    ('AL', _('Albania')),
    ('AM', _('Armenia')),
    ('AN', _('Netherlands Antilles')),
    ('AO', _('Angola')),
    ('AQ', _('Antarctica')),
    ('AR', _('Argentina')),
    ('AS', _('American Samoa')),
    ('AT', _('Austria')),
    ('AU', _('Australia')),
    ('AW', _('Aruba')),
    ('AZ', _('Azerbaijan')),
    ('BA', _('Bosnia and Herzegovina')),
    ('BB', _('Barbados')),
    ('BD', _('Bangladesh')),
    ('BE', _('Belgium')),
    ('BF', _('Burkina Faso')),
    ('BG', _('Bulgaria')),
    ('BH', _('Bahrain')),
    ('BI', _('Burundi')),
    ('BJ', _('Benin')),
    ('BM', _('Bermuda')),
    ('BN', _('Brunei Darussalam')),
    ('BO', _('Bolivia')),
    ('BR', _('Brazil')),
    ('BS', _('Bahama')),
    ('BT', _('Bhutan')),
    ('BV', _('Bouvet Island')),
    ('BW', _('Botswana')),
    ('BY', _('Belarus')),
    ('BZ', _('Belize')),
    ('CA', _('Canada')),
    ('CC', _('Cocos (Keeling) Islands')),
    ('CF', _('Central African Republic')),
    ('CG', _('Congo')),
    ('CH', _('Switzerland')),
    ('CI', _('Ivory Coast')),
    ('CK', _('Cook Iislands')),
    ('CL', _('Chile')),
    ('CM', _('Cameroon')),
    ('CN', _('China')),
    ('CO', _('Colombia')),
    ('CR', _('Costa Rica')),
    ('CU', _('Cuba')),
    ('CV', _('Cape Verde')),
    ('CX', _('Christmas Island')),
    ('CY', _('Cyprus')),
    ('CZ', _('Czech Republic')),
    ('DE', _('Germany')),
    ('DJ', _('Djibouti')),
    ('DK', _('Denmark')),
    ('DM', _('Dominica')),
    ('DO', _('Dominican Republic')),
    ('DZ', _('Algeria')),
    ('EC', _('Ecuador')),
    ('EE', _('Estonia')),
    ('EG', _('Egypt')),
    ('EH', _('Western Sahara')),
    ('ER', _('Eritrea')),
    ('ES', _('Spain')),
    ('ET', _('Ethiopia')),
    ('FI', _('Finland')),
    ('FJ', _('Fiji')),
    ('FK', _('Falkland Islands (Malvinas)')),
    ('FM', _('Micronesia')),
    ('FO', _('Faroe Islands')),
    ('FR', _('France')),
    ('FX', _('France, Metropolitan')),
    ('GA', _('Gabon')),
    ('GB', _('United Kingdom (Great Britain)')),
    ('GD', _('Grenada')),
    ('GE', _('Georgia')),
    ('GF', _('French Guiana')),
    ('GH', _('Ghana')),
    ('GI', _('Gibraltar')),
    ('GL', _('Greenland')),
    ('GM', _('Gambia')),
    ('GN', _('Guinea')),
    ('GP', _('Guadeloupe')),
    ('GQ', _('Equatorial Guinea')),
    ('GR', _('Greece')),
    ('GS', _('South Georgia and the South Sandwich Islands')),
    ('GT', _('Guatemala')),
    ('GU', _('Guam')),
    ('GW', _('Guinea-Bissau')),
    ('GY', _('Guyana')),
    ('HK', _('Hong Kong')),
    ('HM', _('Heard & McDonald Islands')),
    ('HN', _('Honduras')),
    ('HR', _('Croatia')),
    ('HT', _('Haiti')),
    ('HU', _('Hungary')),
    ('ID', _('Indonesia')),
    ('IE', _('Ireland')),
    ('IL', _('Israel')),
    ('IN', _('India')),
    ('IO', _('British Indian Ocean Territory')),
    ('IQ', _('Iraq')),
    ('IR', _('Islamic Republic of Iran')),
    ('IS', _('Iceland')),
    ('IT', _('Italy')),
    ('JM', _('Jamaica')),
    ('JO', _('Jordan')),
    ('JP', _('Japan')),
    ('KE', _('Kenya')),
    ('KG', _('Kyrgyzstan')),
    ('KH', _('Cambodia')),
    ('KI', _('Kiribati')),
    ('KM', _('Comoros')),
    ('KN', _('St. Kitts and Nevis')),
    ('KP', _('Korea, Democratic People\'s Republic of')),
    ('KR', _('Korea, Republic of')),
    ('KW', _('Kuwait')),
    ('KY', _('Cayman Islands')),
    ('KZ', _('Kazakhstan')),
    ('LA', _('Lao People\'s Democratic Republic')),
    ('LB', _('Lebanon')),
    ('LC', _('Saint Lucia')),
    ('LI', _('Liechtenstein')),
    ('LK', _('Sri Lanka')),
    ('LR', _('Liberia')),
    ('LS', _('Lesotho')),
    ('LT', _('Lithuania')),
    ('LU', _('Luxembourg')),
    ('LV', _('Latvia')),
    ('LY', _('Libyan Arab Jamahiriya')),
    ('MA', _('Morocco')),
    ('MC', _('Monaco')),
    ('MD', _('Moldova, Republic of')),
    ('MG', _('Madagascar')),
    ('MH', _('Marshall Islands')),
    ('ML', _('Mali')),
    ('MN', _('Mongolia')),
    ('MM', _('Myanmar')),
    ('MO', _('Macau')),
    ('MP', _('Northern Mariana Islands')),
    ('MQ', _('Martinique')),
    ('MR', _('Mauritania')),
    ('MS', _('Monserrat')),
    ('MT', _('Malta')),
    ('MU', _('Mauritius')),
    ('MV', _('Maldives')),
    ('MW', _('Malawi')),
    ('MX', _('Mexico')),
    ('MY', _('Malaysia')),
    ('MZ', _('Mozambique')),
    ('NA', _('Namibia')),
    ('NC', _('New Caledonia')),
    ('NE', _('Niger')),
    ('NF', _('Norfolk Island')),
    ('NG', _('Nigeria')),
    ('NI', _('Nicaragua')),
    ('NL', _('Netherlands')),
    ('NO', _('Norway')),
    ('NP', _('Nepal')),
    ('NR', _('Nauru')),
    ('NU', _('Niue')),
    ('NZ', _('New Zealand')),
    ('OM', _('Oman')),
    ('PA', _('Panama')),
    ('PE', _('Peru')),
    ('PF', _('French Polynesia')),
    ('PG', _('Papua New Guinea')),
    ('PH', _('Philippines')),
    ('PK', _('Pakistan')),
    ('PL', _('Poland')),
    ('PM', _('St. Pierre & Miquelon')),
    ('PN', _('Pitcairn')),
    ('PR', _('Puerto Rico')),
    ('PT', _('Portugal')),
    ('PW', _('Palau')),
    ('PY', _('Paraguay')),
    ('QA', _('Qatar')),
    ('RE', _('Reunion')),
    ('RO', _('Romania')),
    ('RU', _('Russian Federation')),
    ('RW', _('Rwanda')),
    ('SA', _('Saudi Arabia')),
    ('SB', _('Solomon Islands')),
    ('SC', _('Seychelles')),
    ('SD', _('Sudan')),
    ('SE', _('Sweden')),
    ('SG', _('Singapore')),
    ('SH', _('St. Helena')),
    ('SI', _('Slovenia')),
    ('SJ', _('Svalbard & Jan Mayen Islands')),
    ('SK', _('Slovakia')),
    ('SL', _('Sierra Leone')),
    ('SM', _('San Marino')),
    ('SN', _('Senegal')),
    ('SO', _('Somalia')),
    ('SR', _('Suriname')),
    ('ST', _('Sao Tome & Principe')),
    ('SV', _('El Salvador')),
    ('SY', _('Syrian Arab Republic')),
    ('SZ', _('Swaziland')),
    ('TC', _('Turks & Caicos Islands')),
    ('TD', _('Chad')),
    ('TF', _('French Southern Territories')),
    ('TG', _('Togo')),
    ('TH', _('Thailand')),
    ('TJ', _('Tajikistan')),
    ('TK', _('Tokelau')),
    ('TM', _('Turkmenistan')),
    ('TN', _('Tunisia')),
    ('TO', _('Tonga')),
    ('TP', _('East Timor')),
    ('TR', _('Turkey')),
    ('TT', _('Trinidad & Tobago')),
    ('TV', _('Tuvalu')),
    ('TW', _('Taiwan, Province of China')),
    ('TZ', _('Tanzania, United Republic of')),
    ('UA', _('Ukraine')),
    ('UG', _('Uganda')),
    ('UM', _('United States Minor Outlying Islands')),
    ('US', _('United States of America')),
    ('UY', _('Uruguay')),
    ('UZ', _('Uzbekistan')),
    ('VA', _('Vatican City State (Holy See)')),
    ('VC', _('St. Vincent & the Grenadines')),
    ('VE', _('Venezuela')),
    ('VG', _('British Virgin Islands')),
    ('VI', _('United States Virgin Islands')),
    ('VN', _('Viet Nam')),
    ('VU', _('Vanuatu')),
    ('WF', _('Wallis & Futuna Islands')),
    ('WS', _('Samoa')),
    ('YE', _('Yemen')),
    ('YT', _('Mayotte')),
    ('YU', _('Yugoslavia')),
    ('ZA', _('South Africa')),
    ('ZM', _('Zambia')),
    ('ZR', _('Zaire')),
    ('ZW', _('Zimbabwe')),
    ('ZZ', _('Unknown or unspecified country')),
]

class CountryField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 2)
        kwargs.setdefault('choices', COUNTRIES)
        super(CountryField, self).__init__(*args, **kwargs)
    def get_internal_type(self):
        return "CharField"

# Static Content of Webpage
#Start About Section
class About(models.Model):
    description     = models.TextField(max_length=1000)

class AboutImage(models.Model):
    general         = models.ForeignKey(About, on_delete=models.CASCADE)
    uploaded_at     = models.DateTimeField(auto_now_add=True)
    image           = models.ImageField(upload_to='about/general/')


class AboutMember(models.Model):
    name            = models.CharField(max_length=30)
    position        = models.CharField(max_length=30)
    content         = models.TextField(max_length=1000)
    uploaded_at     = models.DateTimeField(auto_now_add=True)
    image           = models.ImageField(upload_to='about/member/')
    def __str__(self):
        return self.name


class AboutDate(models.Model):
    start           = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end             = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    description     = models.CharField(max_length=50)
    def yearstart(self):
        return self.start.strftime('%b %Y')
    def yearend(self):
        return self.end.strftime('%Y')
    def __str__(self):
         return self.description
#End About Section


#Start FAQ Section
class Faq(models.Model):
    question         = models.CharField(max_length=300, null=True, blank=True)
    answer           = models.TextField(max_length=2000, null=True, blank=True)

class FaqValues(models.Model):
    image            = models.CharField(max_length=15, null= True, blank=True)
    title            = models.CharField(max_length=100, null=True, blank=True)
    content          = models.CharField(max_length=120, null=True, blank=True)
#End FAQ Section


#Start Variable Info Pages
class Info(models.Model):
    title            = models.CharField(max_length=50)
    content          = models.TextField(max_length=5000, null=True, blank=True)
    slug             = models.SlugField(unique=True, null=True, blank=True)
def info_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(info_pre_save_receiver,sender=Info)

class InfoImage(models.Model):
    general          = models.ForeignKey(Info, on_delete=models.CASCADE)
    uploaded_at      = models.DateTimeField(auto_now_add=True)
    image            = models.ImageField(upload_to='info/')
#End Info Pages

class NewsList(models.Model):
    email           = models.CharField(max_length=100, blank=True, null=True)
    active          = models.BooleanField(default=True)
    inscribed_at    = models.DateField(auto_now_add=True)

class Portfolio(models.Model):
    owner           = models.ForeignKey(User, on_delete=models.CASCADE)
    order           = models.CharField(max_length=1, blank=True, null=True)
    text            = models.TextField(max_length=30, blank=True, null=True)
    sec_text        = models.TextField(max_length=30, blank=True, null=True)
    uploaded_at     = models.DateTimeField(auto_now_add=True)
    upload          = models.ImageField(upload_to='portfolio/')

class Testimonial(models.Model):
    text = models.TextField(max_length=350)
    author = models.CharField(max_length=30)
    def __str__(self):
        return self.text

#Proyectos
#Events
class Event(models.Model):
    Icon             = (
        ('fas fa-redo','Masterclass'),
        ('fas fa-rocket','Festival'),
        ('fas fa-cogs','Cycle'),
        ('fas fa-cog','Workshop'),
        ('fas fa-star','Camp'),
        ('fas fa-seedling','Retreat'),
    )
    Ocurrance        = (
        ('Mon','Monday\'s'),
        ('Tue','Tuesday\'s'),
        ('Wed','Wednesday\'s'),
        ('Thu','Thursday\'s'),
        ('Fri','Friday\'s'),
        ('Sun','Sunday\'s'),
        ('WedSun.','Wed. & Sunday\'s'),
        ('TueSun.','Tue. & Sunday\'s'),
        ('Year','Yearly'),
        ('One','One Time'),
    )
    Level            = (
        ('A', 'Advanced'),
        ('B', 'Intermediate'),
        ('C', 'Introduction'),
        ('Z', 'Multilevel'),
    )
    cat              = models.CharField(max_length=15, choices=Icon, default=1)
    level            = models.CharField(max_length=1, choices=Level, default=1)
    title            = models.CharField(max_length=60)
    description      = models.TextField(max_length=3000)
    prerequisites    = models.TextField(max_length=1000, null=True, blank=True)
    loc              = models.CharField(max_length=60)
    loc_extra        = models.CharField(max_length=60, null=True, blank=True)
    city             = models.CharField(max_length=20)
    ocurrance        = models.CharField(max_length=8, choices=Ocurrance, null=True,blank=True)
    datestart        = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    #Why did i need this ? 
    dateextra        = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    dateend          = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    price            = models.CharField(max_length=20, null=True, blank=True)
    publication      = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    published        = models.BooleanField()
    registration     = models.BooleanField(default=True)
    slug             = models.SlugField(unique=True, null=True, blank=True)
    def get_datestart(self):
        if self.datestart.strftime('%b') == self.dateend.strftime('%b') and self.dateend.strftime('%d %b') != self.datestart.strftime('%d %b'):
            return self.datestart.strftime('%d')
        else:
            return self.datestart.strftime('%d %b')
    def get_dateend(self):
        if self.dateend.strftime('%d %b') == self.datestart.strftime('%d %b'):
            return self.dateend.strftime('')
        else:
            return self.dateend.strftime(' - %d. %b %Y')
    def get_timestart(self):
        return self.datestart.strftime('%H:%M')
    def get_timeend(self):
        return self.dateend.strftime('%H:%M')
    def get_timeextra(self):
        return self.dateextra.strftime('%H:%M')
    def __str__(self):
        return self.title
''' Signal of Django to generate slug if not created  '''
def event_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(event_pre_save_receiver, sender=Event)


class EventImage(models.Model):
    event           = models.ForeignKey(Event, on_delete=models.CASCADE)
    uploaded_at     = models.DateTimeField(auto_now_add=True)
    image           = models.ImageField(upload_to='event/')


class Teacher(models.Model):
    name            = models.CharField(max_length=30)
    event           = models.ForeignKey(Event, on_delete=models.CASCADE)
    position        = models.CharField(max_length=30, null=True, blank=True)
    content         = models.TextField(max_length=1000)
    uploaded_at     = models.DateTimeField(auto_now_add=True)
    image           = models.ImageField(upload_to='about/teacher/', null=True, blank=True)
    def __str__(self):
        return self.name


class Booking(models.Model):
    Abo             = [
        ('SS','Single Season Abo'),
        ('DS','Double Season Abo'),
        ('SC','Single Cycle Abo'),
        ('DC','Double Cycle Abo'),
        ('ST','Single Day Ticket'),
    ]
    Category           = [
        ('EI','Einkommen'),
        ('KO','Kosten'),
        ('AU','Ausgaben'),
        ('IN','Inversion'),
        ('LO','Lohn'),
        ('SP','Spargeld'),
    ]
    Reduction       =[
        ('ST','Student Price'),
        ('NM','Normal Price'),
    ]
    Day             = [
        ('Wed','Wednesday\'s'),
        ('Tue','Tuesday\'s'),
        ('Sun','Sunday\'s'),
        ('WedSun.','Wed. & Sunday\'s'),
        ('TueWed.','Tue. & Wednesday\'s'),
        ('TueSun.','Tue. & Sunday\'s'),
    ]
    Status          = [
        ('IN','Informed'),
        ('CA','Canceled'),
        ('PA','Payed'),
        ('PE','Pending'),
        ('SW','Switched')
    ]
    Method          = [
        ('BT','Bank'),
        ('TW','Twint'),
        ('PP','PayPal'),
        ('CS','Cash'),
        ('CR','Credit Card'),
        ('UN','Unclasified'),
    ]
    category        = models.CharField(max_length=10, choices=Category, default='EI')
    event           = models.ForeignKey('project.Event', on_delete=models.CASCADE)
    name            = models.CharField(max_length=40)
    email           = models.CharField(max_length=50)
    phone           = models.CharField(max_length=30)
    abo             = models.CharField(max_length=8, choices=Abo, null=True, blank=True)
    day             = models.CharField(max_length=8, choices=Day, null=True, blank=True)
    reduction       = models.CharField(max_length=12, choices=Reduction, null=True, blank=True)
    option          = models.CharField(max_length=50, null=True, blank=True)
    comment         = models.TextField(max_length=350, null=True, blank=True)
    amount          = models.CharField(max_length=30, null=True, blank=True)
    pay_till        = models.DateField(auto_now_add=False,auto_now=False, null=True, blank=True)
    pay_date        = models.DateField(auto_now_add=False,auto_now=False, null=True, blank=True)
    methode         = models.CharField(max_length=15, choices=Method, default='UN', null=True, blank=True)
    status          = models.CharField(max_length=15, choices=Status, null=True, blank=True)
    note            = models.TextField(max_length=1000, null=True, blank=True)
    booked_at       = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s - %s' % (self.event, self.name)


#Contabilidad
class Accounting(models.Model):
    Category           = [
        ('EI','Einkommen'),
        ('KO','Kosten'),
        ('AU','Ausgaben'),
        ('IN','Inversion'),
        ('LO','Lohn'),
        ('SP','Spargeld'),
    ]
    Status          = [
        ('IN','Informed'),
        ('CA','Canceled'),
        ('PA','Payed'),
        ('PE','Pending'),
        ('SW','Switched')
    ]
    Method          = [
        ('BT','Bank'),
        ('TW','Twint'),
        ('PP','PayPal'),
        ('CS','Cash'),
        ('CR','Credit Card'),
        ('UN','Unclasified'),
    ]
    category        = models.CharField(max_length=10, choices=Category)
    event           = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    amount          = models.CharField(max_length=9)
    pay_till        = models.DateField(auto_now_add=False,auto_now=False, null=True, blank=True)
    pay_date        = models.DateField(auto_now_add=False,auto_now=False, null=True, blank=True)
    methode         = models.CharField(max_length=15, choices=Method, default='UN', null=True, blank=True)
    status          = models.CharField(max_length=15, choices=Status, null=True, blank=True)
    description     = models.CharField(max_length=300, null=True, blank=True)
    degistered_at   = models.DateTimeField(auto_now_add=True)

##### DATA BASE
class Address(models.Model):
    country = CountryField()
    city = models.CharField(max_length=50) # City / Town
    postalcode = models.CharField(max_length=10, null=True, blank=True) # Postal code / ZIP Code
    street = models.CharField(max_length=50)# Street address
    premise = models.CharField(max_length=10, null=True, blank=True)# Apartment, Suite, Box number, etc.
    def __str__(self):
        return '%s, %s %s' % (self.street, self.postalcode, self.city)


