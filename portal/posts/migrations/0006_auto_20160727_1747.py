# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20160706_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='posting_startup',
            field=models.ForeignKey(related_name='posting_startup', to='startups.startUp', null=True, blank=True),
        ),
    ]
