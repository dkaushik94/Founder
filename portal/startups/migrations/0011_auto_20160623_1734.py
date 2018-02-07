# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0010_auto_20160504_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='rank',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
