# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0020_startup_company_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='type_of_trade',
            field=models.CharField(choices=[('None', 'None'), ('Technology', 'Technology'), ('Logistics', 'Logistics'), ('Markeeting', 'Marketing')], max_length=100, blank=True),
        ),
    ]
