# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfhistory', '0013_auto_20151116_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=400, null=True, blank=True)),
                ('version', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('baseline', models.NullBooleanField(default=False)),
                ('project', models.ForeignKey(to='perfhistory.Project')),
                ('tag', models.ForeignKey(to='perfhistory.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=400, null=True, blank=True)),
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
                ('result', models.ForeignKey(to='perfhistory.Result')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='resultdetail',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='resultdetail',
            name='project',
        ),
        migrations.RemoveField(
            model_name='resultdetail',
            name='tag',
        ),
        migrations.DeleteModel(
            name='ResultDetail',
        ),
        migrations.AlterUniqueTogether(
            name='result',
            unique_together=set([('project', 'tag', 'version', 'name')]),
        ),
    ]
