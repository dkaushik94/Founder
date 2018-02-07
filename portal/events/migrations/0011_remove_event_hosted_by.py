# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20160801_1606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='hosted_by',
        ),
    ]
