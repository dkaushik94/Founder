# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_post_post_url_favicon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='post_url_favicon',
            new_name='post_url_image',
        ),
        migrations.AddField(
            model_name='post',
            name='post_url_description',
            field=models.CharField(blank=True, null=True, max_length=300),
        ),
        migrations.AddField(
            model_name='post',
            name='post_url_title',
            field=models.CharField(blank=True, null=True, max_length=200),
        ),
    ]
