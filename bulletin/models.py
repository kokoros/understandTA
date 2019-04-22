from django.db import models

# Create your models here.

class Find_pet(models.Model):
    username = models.CharField(max_length=80,unique=True, db_index=True)
    title = models.CharField(max_length=120)
    main = models.CharField(max_length=4096)
    time = models.CharField(max_length=120)
    area = models.CharField(max_length=80)
    thanks = models.CharField(max_length=120)
    pic = models.CharField(max_length=80)


class Adopter(models.Model):
    username = models.CharField(max_length=80, unique=True, db_index=True)
    title = models.CharField(max_length=120)
    main = models.CharField(max_length=4096)
    time = models.CharField(max_length=120)
    area = models.CharField(max_length=80)
    pet_type = models.CharField(max_length=120)
    pic = models.CharField(max_length=80)