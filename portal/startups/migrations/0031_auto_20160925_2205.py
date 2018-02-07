# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0030_auto_20160913_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='startup',
            name='identity_token',
            field=models.CharField(blank=True, null=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='startup',
            name='team_size',
            field=models.CharField(choices=[('None', 'None'), ('0-10', '0-10'), ('10+', '10+'), ('20+', '20+'), ('30+', '30+'), ('40+', '40+'), ('50+', '50+')], blank=True, null=True, max_length=10),
        ),
    ]
