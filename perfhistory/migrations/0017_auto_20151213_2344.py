# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfhistory', '0016_auto_20151130_2333'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('name',)]),
        ),
    ]
