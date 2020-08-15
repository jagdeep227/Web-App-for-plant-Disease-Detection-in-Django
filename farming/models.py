from django.db import models
from django.contrib.auth.models import Permission, User
# Create your models here.


class Person(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email=models.EmailField(max_length=100,primary_key=True)
    address=models.CharField(max_length=255)
    age=models.IntegerField()
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female'),
        (2, 'not specified'),
    )
    gender = models.IntegerField(choices=GENDER_CHOICES)
    profession=models.CharField(max_length=255)

    
class photo_data(models.Model):
    email1=models.CharField(max_length=255)
    disease = models.CharField(max_length=255)
    suggestion = models.CharField(max_length=1000)
    photo = models.ImageField(upload_to='photo_datas')
    