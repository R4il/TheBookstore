# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-13 20:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20171013_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcard',
            name='cvv',
            field=models.CharField(default=None, max_length=25),
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='exp_date',
            field=models.CharField(default=None, max_length=25),
        ),
    ]
