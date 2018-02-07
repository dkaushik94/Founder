# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20160801_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='hosted_by',
            field=models.ManyToManyField(blank=True, related_name='hosted_events', to=settings.AUTH_USER_MODEL),
        ),
    ]
