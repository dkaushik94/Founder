# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0013_auto_20160802_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_hosted_by',
            field=models.ManyToManyField(related_name='hosted_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
