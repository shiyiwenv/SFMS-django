# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-15 06:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crs', '0006_auto_20181114_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='inter_ip',
            field=models.CharField(max_length=150, null=True, verbose_name='外网ip'),
        ),
        migrations.AddField(
            model_name='host',
            name='label',
            field=models.CharField(max_length=50, null=True, verbose_name='主机标签'),
        ),
    ]
