# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-14 08:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jc', '0004_auto_20170714_0712'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitrecord',
            name='bkj_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='visitrecord',
            name='user_id',
            field=models.IntegerField(null=True),
        ),
    ]
