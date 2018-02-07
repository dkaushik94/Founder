# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0008_startup_approval_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='startup',
            name='rank',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='startup',
            name='type_of_trade',
            field=models.CharField(choices=[('tech', 'Technology(Software)'), ('logistics', 'Logistics')], blank=True, max_length=100),
        ),
    ]
