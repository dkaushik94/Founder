# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0022_auto_20160804_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='trending',
            field=models.NullBooleanField(default=False),
        ),
    ]
