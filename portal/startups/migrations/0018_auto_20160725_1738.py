# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0017_auto_20160715_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='approval_status',
            field=models.CharField(null=True, blank=True, max_length=10),
        ),
    ]
