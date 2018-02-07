# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0028_auto_20160913_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='team_size',
            field=models.CharField(max_length=10, choices=[('---', '---'), ('0-10', '0-10'), ('10+', '10+'), ('20+', '20+'), ('30+', '30+'), ('40+', '40+'), ('50+', '50+')], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='startup',
            name='type_of_trade',
            field=models.CharField(max_length=100, choices=[('None', 'None'), ('Technology', 'Technology'), ('Logistics', 'Logistics'), ('Marketing', 'Marketing'), ('Ecommerce', 'Ecommerce'), ('Services', 'Services')], blank=True),
        ),
    ]
