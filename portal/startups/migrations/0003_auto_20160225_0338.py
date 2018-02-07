# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0002_auto_20160220_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='facebook_url',
            field=models.URLField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='startup',
            name='linkedin_url',
            field=models.URLField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='startup',
            name='startup_image',
            field=models.ImageField(upload_to='startup_pics/', blank=True),
        ),
        migrations.AlterField(
            model_name='startup',
            name='twitter_handle',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='startup',
            name='type_of_trade',
            field=models.CharField(blank=True, choices=[('tech', 'Technology(Software)')], max_length=100),
        ),
    ]
