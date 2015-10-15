# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('perfhistory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 8, 21, 40, 0, 426175, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 8, 21, 40, 5, 761836, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
