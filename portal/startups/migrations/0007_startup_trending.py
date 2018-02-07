# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0006_auto_20160405_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='startup',
            name='trending',
            field=models.NullBooleanField(),
        ),
    ]
