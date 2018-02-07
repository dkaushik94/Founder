# Django Related imports
from django import forms

# Model imports

from startups.models import startUp


class AddUserForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name', required=False)
    last_name = forms.CharField(max_length=30, label='Last Name', required=False)
    email = forms.EmailField(required=True)
    image = forms.FileField(required=False)
    linkedin_url = forms.URLField(required=False)
    facebook_url = forms.URLField(required=False)
    twitter_handle = forms.URLField(required=False)
    startup = forms.ModelChoiceField(queryset=startUp.objects.all())
    add_another_founder = forms.BooleanField(required=False)
    about = forms.CharField(widget=forms.Textarea, required=False)
