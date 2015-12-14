# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfhistory', '0015_result_numberofusers'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='duration',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='filename',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
