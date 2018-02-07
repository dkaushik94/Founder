# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0003_auto_20160225_0338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='location',
            field=models.CharField(verbose_name='Based out of', max_length=60),
        ),
        migrations.AlterField(
            model_name='startup',
            name='name_of_startup',
            field=models.CharField(verbose_name='Registered name of StartUp', max_length=100),
        ),
    ]
