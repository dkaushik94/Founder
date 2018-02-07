# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20160905_1913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='chat_password',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='chat_user',
        ),
        migrations.AddField(
            model_name='mentor',
            name='chat_password',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='mentor',
            name='chat_user',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
