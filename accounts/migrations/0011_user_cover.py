# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-05 21:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20171016_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cover',
            field=models.CharField(default='nouserpic.jpg', max_length=255),
        ),
    ]
