# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-14 20:11
from __future__ import unicode_literals

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('booker', '0057_auto_20170314_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musician',
            name='image',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]