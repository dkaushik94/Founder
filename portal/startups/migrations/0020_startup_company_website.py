# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0019_auto_20160725_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='startup',
            name='company_website',
            field=models.URLField(null=True, blank=True, max_length=50),
        ),
    ]
