# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfhistory', '0026_auto_20160126_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
    ]
