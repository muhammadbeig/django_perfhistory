# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfhistory', '0014_auto_20151116_0136'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='numberofusers',
            field=models.IntegerField(null=True),
        ),
    ]
