# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20160714_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='twitter_handle',
            field=models.URLField(max_length=1000, blank=True),
        ),
    ]
