# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('startups', '0004_auto_20160403_1723'),
    ]

    operations = [
        migrations.CreateModel(
            name='post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('post_text', models.TextField()),
                ('post_image', models.FileField(null=True, upload_to='postimages/', blank=True)),
                ('post_url', models.URLField(max_length=1000, null=True, blank=True)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_timestamp', models.DateTimeField(auto_now=True)),
                ('trending', models.NullBooleanField()),
                ('likers', models.ManyToManyField(related_name='liked_post', to=settings.AUTH_USER_MODEL)),
                ('poster', models.ForeignKey(related_name='posting_user', to=settings.AUTH_USER_MODEL)),
                ('posting_startup', models.ForeignKey(related_name='posting_startup', null=True, to='startups.startUp')),
            ],
        ),
    ]
