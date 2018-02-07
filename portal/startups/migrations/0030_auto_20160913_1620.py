# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0029_auto_20160913_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='inc_year',
            field=models.CharField(null=True, max_length=4, blank=True),
        ),
    ]
