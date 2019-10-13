from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=8)
    age = models.IntegerField()
    info = models.OneToOneField(to='Info')

class Info(models.Model):
    birthday = models.DateField()
    phone = models.IntegerField()

class Book(models.Model):
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    publish = models.ForeignKey(to='Publish')
    author = models.ManyToManyField(to='Author')

class Publish(models.Model):
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=32)