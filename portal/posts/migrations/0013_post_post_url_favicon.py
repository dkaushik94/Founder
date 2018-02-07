# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_auto_20160928_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_url_favicon',
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
    ]
