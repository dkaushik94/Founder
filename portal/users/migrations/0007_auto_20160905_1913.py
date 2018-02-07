# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_myuser_chat_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='chat_user',
            field=models.CharField(null=True, max_length=50, blank=True),
        ),
    ]
