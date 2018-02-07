# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_post_post_headline'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='reported',
            field=models.BooleanField(default=False),
        ),
    ]
