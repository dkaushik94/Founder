# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0012_auto_20160628_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='background_startup_image',
            field=models.URLField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='startup',
            name='startup_logo',
            field=models.URLField(max_length=250, null=True, blank=True),
        ),
    ]
