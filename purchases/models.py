from django.db import models
from accounts.models import User
from books.models import Book

# Create your models here.


class PreviousOrder(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    qty = models.IntegerField(default=1)
    
    def __str__(self):
        return f'{self.user} {self.book}'

    class Meta:
        unique_together = ('book', 'user')
        managed = True


class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    qty = models.IntegerField(default=1)
    
    def __str__(self):
        return f'{self.user} {self.book}'

    class Meta:
        unique_together = ('book', 'user')
        managed = True


class WishList(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    qty = models.IntegerField(default=1)
    
    def __str__(self):
        return f'{self.user} {self.book}'

    class Meta:
        unique_together = ('book', 'user')
        managed = True
