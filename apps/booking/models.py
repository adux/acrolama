from django.db import models


BOOKINGSTATUS = [
    ('PE','Pending'),
    ('WL','Waiting List'),
    ('IN','Informed'),
    ('PA','Participant'),
    ('CA','Canceled'),
    ('SW','Switched')
]


class Book(models.Model):
    event = models.ForeignKey('project.Event', on_delete=models.CASCADE)
    #USER
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    # address = models.CharField(max_length=120)
    #Options
    price = models.ForeignKey('project.PriceOption', on_delete=models.CASCADE)
    time= models.ForeignKey('project.TimeOption', on_delete=models.CASCADE)
    #STATUS
    comment = models.TextField(max_length=350, null=True, blank=True)
    status = models.CharField(max_length=15, choices=BOOKINGSTATUS , null=True, blank=True)
    note = models.TextField(max_length=1000, null=True, blank=True)
    booked_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s - %s' % (self.event, self.name)

