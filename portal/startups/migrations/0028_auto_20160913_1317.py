# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0027_auto_20160905_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='startup',
            name='chat_password',
            field=models.CharField(max_length=8, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='startup',
            name='chat_user',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
