# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0005_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='name_of_startup',
            field=models.CharField(verbose_name='Registered name of StartUp', unique=True, max_length=100),
        ),
    ]
