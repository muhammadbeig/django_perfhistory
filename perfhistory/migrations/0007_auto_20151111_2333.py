# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfhistory', '0006_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='description',
            field=models.CharField(max_length=400, blank=True),
        ),
    ]
