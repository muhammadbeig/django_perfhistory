# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='tags',
            name='project',
            field=models.ForeignKey(default=1, to='myapp.Project'),
            preserve_default=False,
        ),
    ]
