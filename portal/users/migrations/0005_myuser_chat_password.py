# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20160715_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='chat_password',
            field=models.CharField(blank=True, null=True, max_length=8),
        ),
    ]
