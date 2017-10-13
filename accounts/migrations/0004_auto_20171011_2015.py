# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-12 00:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20171011_2013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditcard',
            name='id',
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='credit_card_number',
            field=models.CharField(default=None, max_length=50, primary_key=True, serialize=False),
        ),
    ]
