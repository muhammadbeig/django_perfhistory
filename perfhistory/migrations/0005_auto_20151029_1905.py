# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfhistory', '0004_auto_20151026_2111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='project_id',
            new_name='project',
        ),
    ]
