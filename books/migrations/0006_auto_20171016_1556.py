# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-16 19:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_auto_20171010_0320'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BookReview',
            new_name='Review',
        ),
    ]
