# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='investor',
            options={'verbose_name': 'investor'},
        ),
        migrations.AlterModelOptions(
            name='mentor',
            options={'verbose_name': 'model'},
        ),
        migrations.AlterModelTable(
            name='investor',
            table=None,
        ),
        migrations.AlterModelTable(
            name='mentor',
            table=None,
        ),
    ]
