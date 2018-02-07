# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0016_auto_20160909_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='hosted_by_mentor',
        ),
        migrations.RemoveField(
            model_name='event',
            name='hosted_by_startup',
        ),
        migrations.RemoveField(
            model_name='event',
            name='event_hosted_by',
        ),
        migrations.AddField(
            model_name='event',
            name='event_hosted_by',
            field=models.ForeignKey(null=True, related_name='hosted_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
