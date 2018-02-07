# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_myuser_chat_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='chat_user',
            field=models.CharField(max_length=15, blank=True, null=True),
        ),
    ]
