# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_auto_20161003_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_url_description',
            field=models.CharField(null=True, blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_url_image',
            field=models.URLField(null=True, blank=True, max_length=500),
        ),
    ]
