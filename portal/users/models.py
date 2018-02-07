# Django Related imports.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
import uuid

# Database models related imports.
from startups.models import startUp


# Model For Founder profiles
class MyUser(AbstractUser):
    designation = models.CharField(max_length=25, blank=True)
    image = models.URLField(max_length=250, blank=True, null=True)
    about = models.TextField(blank=True)
    linkedin_url = models.URLField(max_length=1000, blank=True)
    twitter_handle = models.URLField(max_length=1000, blank=True)
    facebook_url = models.URLField(max_length=500, blank=True)
    startup = models.ForeignKey(startUp, related_name='cofounders', null=True, blank=True)
    following_startup = models.ManyToManyField(startUp, symmetrical=False, related_name='following_company', blank=True)
    tagline = models.CharField(max_length=80, blank=True)
    skills = models.CharField(max_length=100, blank=True)


class Mentor(MyUser):
    company_name = models.CharField(max_length=75, blank=True)
    expertise = models.CharField(max_length=100, blank=True)
    past_experience = models.TextField(blank=True)
    mentoring_startup = models.ManyToManyField(startUp, related_name="mentors", blank=True)
    chat_password = models.CharField(max_length=8, null=True, blank=True)
    chat_user = models.CharField(max_length=50, null=True, blank=True)
    identity_token = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = "mentor"

    def __str__(self):
        return str(self.username)


class Investor(MyUser):
    company_name = models.CharField(max_length=75, blank=True)
    expertise = models.CharField(max_length=100, blank=True)
    past_experience = models.TextField(blank=True)
    investing_startup = models.ManyToManyField(startUp, related_name="investors")

    class Meta:
        verbose_name = "investor"

    def __str__(self):
        return str(self.username)
