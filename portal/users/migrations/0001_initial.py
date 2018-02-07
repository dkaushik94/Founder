# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings
import django.core.validators
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('startups', '0015_auto_20160713_1505'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(max_length=30, verbose_name='username', help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', error_messages={'unique': 'A user with that username already exists.'}, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], unique=True)),
                ('first_name', models.CharField(max_length=30, blank=True, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, blank=True, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, blank=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(verbose_name='staff status', default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(verbose_name='active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('designation', models.CharField(max_length=25, blank=True)),
                ('image', models.URLField(max_length=250, blank=True, null=True)),
                ('about', models.TextField(blank=True)),
                ('linkedin_url', models.URLField(max_length=1000, blank=True)),
                ('twitter_handle', models.CharField(max_length=50, blank=True)),
                ('facebook_url', models.URLField(max_length=500, blank=True)),
                ('tagline', models.CharField(max_length=80, blank=True)),
                ('skills', models.CharField(max_length=100, blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('myuser_ptr', models.OneToOneField(serialize=False, primary_key=True, parent_link=True, auto_created=True, to=settings.AUTH_USER_MODEL)),
                ('company_name', models.CharField(max_length=75, blank=True)),
                ('expertise', models.CharField(max_length=100, blank=True)),
                ('past_experience', models.TextField(blank=True)),
                ('investing_startup', models.ManyToManyField(related_name='investors', to='startups.startUp')),
            ],
            options={
                'db_table': 'investor',
            },
            bases=('users.myuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('myuser_ptr', models.OneToOneField(serialize=False, primary_key=True, parent_link=True, auto_created=True, to=settings.AUTH_USER_MODEL)),
                ('company_name', models.CharField(max_length=75, blank=True)),
                ('expertise', models.CharField(max_length=100, blank=True)),
                ('past_experience', models.TextField(blank=True)),
                ('mentoring_startup', models.ManyToManyField(blank=True, to='startups.startUp', related_name='mentors')),
            ],
            options={
                'db_table': 'mentor',
            },
            bases=('users.myuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='myuser',
            name='following_startup',
            field=models.ManyToManyField(blank=True, to='startups.startUp', related_name='following_company'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='groups',
            field=models.ManyToManyField(blank=True, verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', to='auth.Group', related_name='user_set'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='startup',
            field=models.ForeignKey(blank=True, to='startups.startUp', null=True, related_name='cofounders'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, verbose_name='user permissions', help_text='Specific permissions for this user.', related_query_name='user', to='auth.Permission', related_name='user_set'),
        ),
    ]
