# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name_of_event', models.CharField(verbose_name='Name of Event :', max_length=200)),
                ('hosted_by', models.CharField(verbose_name='Who is hosting this Event', max_length=100)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('start_date', models.CharField(verbose_name='When does it start?', max_length=50)),
                ('end_date', models.CharField(verbose_name='When does it end?', max_length=50)),
                ('public_url', models.URLField(blank=True, max_length=500)),
                ('event_image', models.ImageField(upload_to='event_pics/')),
                ('attendees', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, related_name='events_attending')),
            ],
        ),
    ]
