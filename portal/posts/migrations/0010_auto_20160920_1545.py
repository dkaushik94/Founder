# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0009_confessionpost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='confessionpost',
            name='rank',
        ),
        migrations.AddField(
            model_name='confessionpost',
            name='downvotes',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='confession_downvotes'),
        ),
        migrations.AddField(
            model_name='confessionpost',
            name='upvotes',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='confession_upvotes'),
        ),
    ]
