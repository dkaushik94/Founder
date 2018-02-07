# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0009_auto_20160416_0112'),
    ]

    operations = [
        migrations.RenameField(
            model_name='startup',
            old_name='startup_image',
            new_name='background_startup_image',
        ),
        migrations.AddField(
            model_name='startup',
            name='company_tagline',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='startup',
            name='startup_logo',
            field=models.ImageField(upload_to='startup_pics/', blank=True),
        ),
        migrations.AlterField(
            model_name='startup',
            name='type_of_trade',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
