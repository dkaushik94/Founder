# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0024_startup_trending_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='team_size',
            field=models.CharField(null=True, choices=[('0-10', '0-10'), ('10+', '10+'), ('20+', '20+'), ('30+', '30+'), ('40+', '40+'), ('50+', '50+')], max_length=10, blank=True),
        ),
    ]
