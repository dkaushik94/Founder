# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_post_confession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confessionpost',
            name='downvotes',
            field=models.ManyToManyField(blank=True, related_name='confession_downvotes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='confessionpost',
            name='upvotes',
            field=models.ManyToManyField(blank=True, related_name='confession_upvotes', to=settings.AUTH_USER_MODEL),
        ),
    ]
