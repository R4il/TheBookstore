from __future__ import unicode_literals
from django.db import models

# Create your models here.


class Author(models.Model):
    authoID = models.AutoField(primary_key=True)
    first = models.CharField(max_length=50)
    last = models.CharField(max_length=50)
    about = models.CharField(max_length=3000)

    def __str__(self):
        return f'{self.first} {self.last}'


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=30)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    rating = models.DecimalField(decimal_places=2, max_digits=3)
    publisher = models.CharField(max_length=255)
    about = models.CharField(max_length=3000)

    def __str__(self):
        return self.title
