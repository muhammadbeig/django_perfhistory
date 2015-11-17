# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfhistory', '0010_auto_20151112_0054'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='result',
            unique_together=set([('tag', 'version')]),
        ),
    ]
