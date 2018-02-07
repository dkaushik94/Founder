# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='startUp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name_of_startup', models.CharField(verbose_name='What is the Registered name of your StartUp?', max_length=100)),
                ('startup_image', models.ImageField(upload_to='startup_pics')),
                ('linkedin_url', models.URLField(max_length=1000)),
                ('facebook_url', models.URLField(max_length=1000)),
                ('twitter_handle', models.CharField(max_length=100)),
                ('type_of_trade', models.CharField(choices=[('newdelhi', 'New Delhi')], max_length=100)),
                ('inc_year', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('team_size', models.PositiveIntegerField()),
                ('location', models.CharField(verbose_name='Where are you based out of?', max_length=60)),
            ],
        ),
    ]
