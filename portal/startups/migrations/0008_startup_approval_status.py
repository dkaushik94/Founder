# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0007_startup_trending'),
    ]

    operations = [
        migrations.AddField(
            model_name='startup',
            name='approval_status',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
