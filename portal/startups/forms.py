#Django Related imports
from django import forms
from django.forms import ModelForm

#Model imports

from .models import startUp



class AddStartupForm(forms.Form):
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

    name_of_startup      = forms.CharField(max_length= 100, label = 'Name of Startup', required = True)
    startup_logo         = forms.ImageField(required = False)
    linkedin_url         = forms.URLField(required=False)
    facebook_url         = forms.URLField(required=False)
    company_website      = forms.URLField(required=True)
    twitter_handle       = forms.CharField(max_length=50, required=False)
    inc_year             = forms.IntegerField(required = True)
    type_of_trade        = forms.ChoiceField(choices=TYPE_OF_TRADE,widget = forms.Select(), required = True)
    description          = forms.CharField(widget=forms.Textarea,required = True)
    team_size            = forms.ChoiceField(choices=TEAM_SIZE, widget = forms.Select(), required = False)
    location             = forms.CharField(max_length=200, required = True)
    company_tagline      = forms.CharField(max_length=100, required = False)

