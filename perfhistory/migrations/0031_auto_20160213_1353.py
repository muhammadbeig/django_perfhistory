# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-13 21:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfhistory', '0030_auto_20160212_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='failure_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='failure_qps',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='latency_average',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='latency_maximum',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='latency_median',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='latency_minimum',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='latency_p90',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='latency_p95',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='latency_p99',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='latency_p99_99',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='latency_stddev',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='responsetime_average',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='responsetime_maximum',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='responsetime_median',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='responsetime_minimum',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='responsetime_p90',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='responsetime_p95',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='responsetime_p99',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='responsetime_p99_99',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='responsetime_stddev',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='success_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='success_qps',
            field=models.FloatField(blank=True, null=True),
        ),
    ]