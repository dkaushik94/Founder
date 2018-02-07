#Django package Imports.
from django.db import models


#Database Models imports.
from users.models import MyUser, Mentor
from startups.models import startUp

class Event(models.Model):
    name_of_event       = models.CharField('Name of Event :' , max_length = 200)
#    hosted_by_mentor   = models.ForeignKey(Mentor , related_name = "hosted_events_mentor", null=True, blank = True)
#    hosted_by_startup  = models.ForeignKey(startUp, related_name = "hosted_event_startup", null=True, blank = True)
    event_hosted_by     = models.ForeignKey('users.MyUser', related_name = 'hosted_by', null = True)
    hosted_by           = models.CharField(max_length=100, null=True)
    description         = models.TextField()
    location            = models.CharField(max_length=100)
    start_date          = models.DateTimeField("When does it start?", null=True)
    end_date            = models.DateTimeField("When does it end?", null=True)
    public_url          = models.URLField(max_length = 500 , blank = True)
    event_image         = models.URLField(blank = True, null = True)
    attendees           = models.ManyToManyField('users.MyUser' , symmetrical = False , related_name = "events_attending" , blank = True)
    lat                 = models.FloatField(blank=True,null=True)
    lon                 = models.FloatField(blank=True,null=True)
    
    def __str__(self):
        return self.name_of_event
