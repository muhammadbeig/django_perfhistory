# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20151008_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='published_date',
            field=models.DateField(default=datetime.datetime(2015, 10, 8, 18, 36, 30, 695302, tzinfo=utc)),
        ),
    ]
