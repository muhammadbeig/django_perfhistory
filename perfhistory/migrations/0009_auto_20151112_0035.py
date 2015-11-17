# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfhistory', '0008_auto_20151112_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='version',
            field=models.CharField(max_length=100),
        ),
    ]
