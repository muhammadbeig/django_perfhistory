# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfhistory', '0007_auto_20151111_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='description',
            field=models.CharField(max_length=400, null=True, blank=True),
        ),
    ]
