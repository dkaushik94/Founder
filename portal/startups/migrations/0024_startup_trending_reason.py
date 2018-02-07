# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0023_auto_20160825_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='startup',
            name='trending_reason',
            field=models.CharField(null=True, max_length=200, blank=True),
        ),
    ]
