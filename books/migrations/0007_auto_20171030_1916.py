# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-30 23:16
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0006_auto_20171016_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('genre', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='best_seller',
            field=models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='N', max_length=3),
        ),
        migrations.AddField(
            model_name='book',
            name='release_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='books.Genre'),
        ),
        migrations.AlterField(
            model_name='review',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set([('book', 'user')]),
        ),
    ]
