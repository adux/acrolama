from django.db import models
# Create your models here.

class AboutMember(models.Model):
        member_name     = models.CharField(max_length=30)
        member_position = models.CharField(max_length=30)
        member_content  = models.CharField(max_length=300)
        def __str__(self):
            return self.member_name

class AboutGeneral(models.Model):
        general_description = models.CharField(max_length=300)

class AboutDate(models.Model):
    date_start          = models.DateTimeField(auto_now=False,auto_now_add=False,null=True,blank=True)
    date_end            = models.DateTimeField(auto_now=False,auto_now_add=False,null=True,blank=True)
    date_description    = models.CharField(max_length=50)
    def yearstart(self):
        return self.date_start.strftime('%b %Y')
    def yearend(self):
            return self.date_end.strftime('%Y')

class Event(models.Model):
    Event_Icon = (
        ('fas fa-redo','Masterclass'),
        ('fas fa-rocket','Festival'),
        ('fas fa-cogs','Cycle'),
        ('fas fa-cog','Workshop'),
        ('fas fa-star','Camp'),
    )
    Ocurrance_Event = (
        ('Wed','Weekly Wednesday'),
        ('Tue','Weekly Thursday'),
        ('Sun','Weekly Sunday'),
        ('Once','One Time Event'),
        ('Year','Yearly Event'),
    )
    type_event          = models.CharField(max_length=13, choices=Event_Icon)
    title_event         = models.CharField(max_length=60)
    description_event   = models.CharField(max_length=300)
    prerequisites_event = models.CharField(max_length=300, null=True, blank=True)
    location_event      = models.CharField(max_length=60)
    city_event          = models.CharField(max_length=20)
    datestart_event     = models.DateTimeField(auto_now=False,auto_now_add=False,null=True,blank=True)
    dateend_event       = models.DateTimeField(auto_now=False,auto_now_add=False,null=True,blank=True)
    ocurrance_event     = models.CharField(max_length=7, choices=Ocurrance_Event)
    duration_event      = models.CharField(max_length=5, null=True,blank=True)
    def get_datestart(self):
        return self.datestart_event.strftime('%d %b')
    def get_dateend(self):
        if self.dateend_event.strftime('%d %b') == self.datestart_event.strftime('%d %b'):
            return self.dateend_event.strftime('')
        else:
            return self.dateend_event.strftime(' - %d %b')
    def __str__(self):
        return self.title_event
