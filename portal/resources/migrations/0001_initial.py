# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name_of_file', models.CharField(max_length=75)),
                ('file', models.FileField(upload_to='resources/')),
                ('type_of_doc', models.CharField(choices=[('legal', 'Legal'), ('hr', 'Humar Resource'), ('finance', 'Finanace'), ('partnership', 'Partnerships')], max_length=100)),
            ],
        ),
    ]
