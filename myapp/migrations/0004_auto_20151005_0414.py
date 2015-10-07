# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_tags_project'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='project_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='project_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='tags',
            old_name='tag_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='tags',
            old_name='tag_name',
            new_name='name',
        ),
    ]
