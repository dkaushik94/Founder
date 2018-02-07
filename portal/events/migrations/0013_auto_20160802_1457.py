# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20160715_1458'),
        ('startups', '0020_startup_company_website'),
        ('events', '0012_event_hosted_by_mentor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='hosted_by_mentor',
        ),
        migrations.AddField(
            model_name='event',
            name='hosted_by_mentor',
            field=models.ForeignKey(to='users.Mentor', blank=True, related_name='hosted_events_mentor', null=True),
        ),
        migrations.RemoveField(
            model_name='event',
            name='hosted_by_startup',
        ),
        migrations.AddField(
            model_name='event',
            name='hosted_by_startup',
            field=models.ForeignKey(to='startups.startUp', blank=True, related_name='hosted_event_startup', null=True),
        ),
    ]
