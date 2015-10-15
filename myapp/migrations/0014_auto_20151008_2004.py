# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_auto_20151008_1920'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='project',
            new_name='project_id',
        ),
    ]
