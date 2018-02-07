# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20160715_1458'),
        ('events', '0011_remove_event_hosted_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='hosted_by_mentor',
            field=models.ManyToManyField(blank=True, to='users.Mentor', related_name='hosted_events_mentor'),
        ),
    ]
