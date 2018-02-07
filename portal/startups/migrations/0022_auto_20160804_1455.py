# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0021_auto_20160804_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='type_of_trade',
            field=models.CharField(choices=[('None', 'None'), ('Technology', 'Technology'), ('Logistics', 'Logistics'), ('Marketing', 'Marketing'), ('Ecommerce', 'Ecommerce')], max_length=100, blank=True),
        ),
    ]
