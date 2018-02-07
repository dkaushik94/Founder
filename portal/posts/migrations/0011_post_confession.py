# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20160920_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='confession',
            field=models.BooleanField(default=False),
        ),
    ]
