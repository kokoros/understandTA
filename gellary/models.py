import datetime

from django.db import models
from django.utils import timezone


class User(models.Model):
    pname = models.CharField(max_length=200)
    photo = models.CharField(max_length=30)
    pdate = models.DateTimeField()
    ptype = models.CharField(max_length=200)
    psex = models.CharField(max_length=20)
    page = models.IntegerField()
    pintro = models.TextField()
    pwords = models.TextField()

    def __str__(self):
        return self.pname


class Bbs(models.Model):
    uname = models.CharField(max_length=30)
    pub_date = models.DateTimeField(auto_now_add=True)
    ubbs = models.CharField(max_length=200)

    class Meta:
        ordering = ['pub_date']
        verbose_name = '用户'

    def __str__(self):
        return self.uname