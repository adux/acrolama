from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


PRONOUN = [
    ('NN','None'),
    ('Mr.','Mr'),
    ('Ms.','Ms'),
    ('Mx.','Mx')
]

#class Profil(models.Model):
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
    address = models.ForeignKey('address.Address', on_delete=models.CASCADE)
    pronoun = models.CharField(max_length=10)
    birth_date = models.DateField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
    address = models.ForeignKey('address.Address', on_delete=models.CASCADE, null=True, blank=True)
    pronoun = models.CharField(max_length=10)
    birth_date = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='user/teacher/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.last_name

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
    address = models.ForeignKey('address.Address', on_delete=models.CASCADE, null=True, blank=True)
    pronoun = models.CharField(max_length=10)
    birth_date = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='user/staff/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.last_name

#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)
#
#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()
