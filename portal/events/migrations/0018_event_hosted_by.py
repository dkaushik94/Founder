# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_auto_20160909_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='hosted_by',
            field=models.CharField(null=True, max_length=100),
        ),
    ]
