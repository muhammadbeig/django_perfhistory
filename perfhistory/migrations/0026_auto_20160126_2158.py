# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-26 21:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfhistory', '0025_auto_20160126_2153'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='result',
            unique_together=set([('project', 'tag', 'version', 'name')]),
        ),
    ]
