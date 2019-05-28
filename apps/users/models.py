from django.db import models

PRONOUN = [
    ('NN','None'),
    ('Mr.','Mr'),
    ('Ms.','Ms'),
    ('Mx.','Mx')
]

#class Profil(models.Model):
class Profile(models.Model):
    phone = models.CharField(max_length=50)
    address = models.ForeignKey('address.Address', on_delete=models.CASCADE)
    pronoun = models.CharField(max_length=10)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Teacher(models.Model):
    phone = models.CharField(max_length=50)
    address = models.ForeignKey('address.Address', on_delete=models.CASCADE)
    pronoun = models.CharField(max_length=10)
    title = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='user/teacher/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Staff(models.Model):
    phone = models.CharField(max_length=50)
    address = models.ForeignKey('address.Address', on_delete=models.CASCADE)
    pronoun = models.CharField(max_length=10)
    title = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='user/staff/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


