# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0014_auto_20160712_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='startup',
            name='location',
            field=models.CharField(max_length=60, verbose_name='Based out of', null=True),
        ),
    ]
