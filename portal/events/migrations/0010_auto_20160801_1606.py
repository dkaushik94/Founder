# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0009_auto_20160801_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='hosted_by_mentor',
        ),
        migrations.AddField(
            model_name='event',
            name='hosted_by',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, related_name='hosted_events'),
        ),
    ]
