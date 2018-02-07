# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0011_auto_20160623_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='background_startup_image',
            field=models.ImageField(blank=True, null=True, upload_to='startup_pics/'),
        ),
        migrations.AlterField(
            model_name='startup',
            name='rank',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='startup',
            name='startup_logo',
            field=models.ImageField(blank=True, null=True, upload_to='startup_pics/'),
        ),
    ]
