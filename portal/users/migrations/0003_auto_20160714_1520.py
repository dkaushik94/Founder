# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20160714_1408'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mentor',
            options={'verbose_name': 'mentor'},
        ),
    ]
