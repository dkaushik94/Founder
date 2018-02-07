# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20160913_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='identity_token',
            field=models.CharField(blank=True, null=True, max_length=1000),
        ),
    ]
