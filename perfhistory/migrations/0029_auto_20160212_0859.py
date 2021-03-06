# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-12 16:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfhistory', '0028_auto_20160211_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='failure_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='failure_qps',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='responsetime_average',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='responsetime_maximum',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='responsetime_median',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='responsetime_minimum',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='responsetime_p90',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='responsetime_p95',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='responsetime_p99',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='responsetime_p99_99',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='responsetime_stddev',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='success_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='success_qps',
            field=models.FloatField(null=True),
        ),
    ]
