# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_auto_20161003_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_url_favicon',
            field=models.URLField(null=True, blank=True),
        ),
    ]
