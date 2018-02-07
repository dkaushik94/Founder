
#Django Related imports
from django import forms



class AddEventForm(forms.Form):
    name_of_event   = forms.CharField(max_length = 200, label='Name of Event :')
    hosted_by       = forms.CharField(max_length = 100 , required = True)
    description     = forms.CharField(widget=forms.Textarea, required = True)
    location        = forms.CharField(max_length = 100)
    start_date      = forms.DateField(widget=forms.TextInput(attrs=
                                { 'class':'datepicker'}),
                                required = True)
    end_date        = forms.DateField(widget=forms.TextInput(attrs=
                                { 'class':'datepicker'})
    ,required = True)
    public_url      = forms.URLField(max_length = 500 , required = False)
    event_image     = forms.FileField(required = False)
