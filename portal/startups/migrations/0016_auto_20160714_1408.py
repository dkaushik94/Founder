# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0015_auto_20160713_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='location',
            field=models.CharField(max_length=60, null=True, blank=True, verbose_name='Based out of'),
        ),
        migrations.AlterField(
            model_name='startup',
            name='team_size',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
