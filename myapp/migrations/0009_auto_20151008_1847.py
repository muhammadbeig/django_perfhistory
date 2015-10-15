# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_auto_20151008_1839'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='published_date',
        ),
        migrations.AddField(
            model_name='project',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 8, 18, 47, 2, 771153)),
        ),
    ]
