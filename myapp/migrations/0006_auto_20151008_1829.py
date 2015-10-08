# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20151005_0424'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='last_modified',
            field=models.DateField(default=datetime.datetime(2015, 10, 8, 18, 29, 39, 961233, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='published_date',
            field=models.DateField(default=datetime.datetime(2015, 10, 8, 18, 29, 50, 288813, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
