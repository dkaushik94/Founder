# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0013_auto_20160705_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='startup',
            name='location',
            field=models.CharField(null=True, max_length=60, verbose_name='Based out of', blank=True),
        ),
    ]
