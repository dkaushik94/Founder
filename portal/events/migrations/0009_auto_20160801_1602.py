# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0020_startup_company_website'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0008_auto_20160801_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='hosted_by',
        ),
        migrations.AddField(
            model_name='event',
            name='hosted_by_mentor',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, related_name='hosted_events_mentor'),
        ),
        migrations.AddField(
            model_name='event',
            name='hosted_by_startup',
            field=models.ManyToManyField(blank=True, to='startups.startUp', related_name='hosted_event_startup'),
        ),
    ]
