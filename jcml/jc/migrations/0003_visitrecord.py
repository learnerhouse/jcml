# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-14 06:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jc', '0002_article_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('time_stamp', models.TimeField()),
            ],
        ),
    ]
