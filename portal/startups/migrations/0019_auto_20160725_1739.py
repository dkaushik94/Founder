# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0018_auto_20160725_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='approval_status',
            field=models.PositiveIntegerField(choices=[(0, 'Pending'), (1, 'Approved')], default=0),
        ),
    ]
