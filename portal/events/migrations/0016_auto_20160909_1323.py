# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0015_auto_20160906_0753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_hosted_by',
        ),
        migrations.AddField(
            model_name='event',
            name='event_hosted_by',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='hosted_by'),
        ),
    ]
