from __future__ import unicode_literals
from django.db import models
from accounts.models import User

# Create your models here.


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    first = models.CharField(max_length=50)
    last = models.CharField(max_length=50)
    about = models.CharField(max_length=3000)

    def __str__(self):
        return f'{self.first} {self.last}'

class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.genre


class Book(models.Model):
    YES = 'Y'
    NO = 'N'
    BS_OPTIONS = (
        (YES, 'Yes'),
        (NO, 'No'),
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    rating = models.DecimalField(decimal_places=2, max_digits=3)
    publisher = models.CharField(max_length=255)
    about = models.CharField(max_length=3000)
    cover = models.CharField(max_length=255, default="nocover.jpg")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    best_seller = models.CharField(max_length=3, choices=BS_OPTIONS, default=NO)

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    title = models.CharField(max_length=100)
    body = models.TextField()
    anonymous = models.BooleanField(default=False)

    def __str__(self):
        return f'Book: {self.book}-{self.user} '

    class Meta:
        unique_together = ('book', 'user')
        managed = True
        db_table = 'BookReviews'

