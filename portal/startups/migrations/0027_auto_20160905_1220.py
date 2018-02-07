# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0026_auto_20160829_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='inc_year',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
