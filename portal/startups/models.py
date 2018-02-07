# Django related imports
from django.db import models


class startUp(models.Model):
    APPROVAL_STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'Approved')
    )
    TEAM_SIZE = (
        ('None', 'None'),
        ('0-10', '0-10'),
        ('10+', '10+'),
        ('20+', '20+'),
        ('30+', '30+'),
        ('40+', '40+'),
        ('50+', '50+')
    )
    TYPE_OF_TRADE = (
        ('None', 'None'),
        ('Technology', 'Technology'),
        ('Logistics', 'Logistics'),
        ('Marketing', 'Marketing'),
        ('Ecommerce', 'Ecommerce'),
        ('Services', 'Services')
    )
    # Choices will be added soon.

    name_of_startup = models.CharField('Registered name of StartUp', max_length=100, unique=True)
    background_startup_image = models.URLField(max_length=250, blank=True, null=True)
    startup_logo = models.URLField(max_length=250, blank=True, null=True)
    company_website = models.URLField(max_length=50, blank=True, null=True)
    linkedin_url = models.URLField(max_length=1000, blank=True)
    facebook_url = models.URLField(max_length=1000, blank=True)
    twitter_handle = models.URLField(max_length=1000, blank=True)
    type_of_trade = models.CharField(choices=TYPE_OF_TRADE, max_length=100, blank=True)
    inc_year = models.CharField(max_length=4,null=True, blank=True)
    description = models.TextField(null=True)
    team_size = models.CharField(choices=TEAM_SIZE, max_length=10, null=True, blank=True)
    location = models.CharField(max_length=250, null=True, blank=True)
    trending = models.NullBooleanField(default=False)
    rank = models.IntegerField(default=0, blank=True)
    approval_status = models.PositiveIntegerField(choices=APPROVAL_STATUS_CHOICES, default=0)
    company_tagline = models.CharField(max_length=200, blank=True)
    trending_reason = models.CharField(max_length=200, blank=True, null=True)
    chat_password = models.CharField(max_length=8, null=True, blank=True)
    chat_user = models.CharField(max_length=50, null=True, blank=True)
    identity_token = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name_of_startup
