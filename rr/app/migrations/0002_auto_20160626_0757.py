# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-26 07:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Products',
            new_name='UserDetails',
        ),
    ]