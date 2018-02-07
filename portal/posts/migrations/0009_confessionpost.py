# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_post_reported'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfessionPost',
            fields=[
                ('post_ptr', models.OneToOneField(primary_key=True, parent_link=True, to='posts.post', serialize=False, auto_created=True)),
                ('rank', models.IntegerField(blank=True, default=0)),
            ],
            bases=('posts.post',),
        ),
    ]
