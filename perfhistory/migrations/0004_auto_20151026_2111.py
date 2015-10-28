# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('perfhistory', '0003_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 26, 21, 11, 41, 777950, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 26, 21, 11, 51, 297734, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.CharField(max_length=400, blank=True),
        ),
    ]
