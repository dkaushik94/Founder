# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0025_auto_20160829_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='location',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
