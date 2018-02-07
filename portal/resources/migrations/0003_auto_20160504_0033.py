# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_auto_20160420_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='type_of_doc',
            field=models.CharField(max_length=100, choices=[('legal', 'Legal'), ('hr', 'Human Resource'), ('finance', 'Finanace'), ('partnership', 'Partnerships')]),
        ),
    ]
