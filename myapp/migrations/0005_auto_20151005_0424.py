# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20151005_0414'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=400)),
                ('project', models.ForeignKey(to='myapp.Project')),
            ],
        ),
        migrations.RemoveField(
            model_name='tags',
            name='project',
        ),
        migrations.DeleteModel(
            name='Tags',
        ),
    ]
