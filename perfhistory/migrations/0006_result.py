# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfhistory', '0005_auto_20151029_1905'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=400)),
                ('version', models.CharField(max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('successcount', models.IntegerField()),
                ('failurecount', models.IntegerField()),
                ('average', models.FloatField()),
                ('median', models.FloatField()),
                ('minimum', models.FloatField()),
                ('maximum', models.FloatField()),
                ('stddev', models.FloatField()),
                ('p90', models.FloatField()),
                ('p95', models.FloatField()),
                ('p99', models.FloatField()),
                ('p99_99', models.FloatField()),
                ('project', models.ForeignKey(to='perfhistory.Project')),
                ('tag', models.ForeignKey(to='perfhistory.Tag')),
            ],
        ),
    ]
