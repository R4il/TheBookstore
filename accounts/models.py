# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, nickname, email_address, password=None):
        if not email_address:
            raise ValueError("Users must enter an email address")
        if not nickname:
            raise ValueError("Users must enter a nickname")

        user = self.model(email_address=self.normalize_email(email_address), nickname=nickname)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, nickname, email_address, password):
        user = self.create_user(nickname, email_address, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    nickname = models.CharField(unique=True, max_length=255)
    first_name = models.CharField(max_length=50, default=None)
    last_name = models.CharField(max_length=50, default=None)
    password = models.CharField(max_length=255)
    email_address = models.EmailField(unique=True, max_length=255)
    last_login = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'nickname'

    REQUIRED_FIELDS = ['email_address','password']

    def __str__(self):
        return "@{}".format(self.nickname)

    def get_short_name(self):
        return self.nickname

    def get_full_name(self):
        return "{} {}".format(self.nickname,self.email_address)

    class Meta:
        managed = True
        db_table = 'users'


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)

    def __str__(self):
        return "@{}".format(self.user.nickname) + " addr : " + self.street_address

    class Meta:
        managed = True
        db_table = 'addresses'