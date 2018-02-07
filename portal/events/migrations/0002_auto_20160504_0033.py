# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='hosted_by',
        ),
        migrations.AddField(
            model_name='event',
            name='hosted_by',
            field=models.ManyToManyField(related_name='hosted_events', blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
