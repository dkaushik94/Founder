from django import forms


from startups.models import startUp


class LoginForm(forms.Form):
    username = forms.EmailField(max_length=50, required=True)
    password = forms.CharField(max_length=15, widget=forms.PasswordInput)


class AddEventForm(forms.Form):
    name_of_event = forms.CharField(max_length=200, label='Name of Event :', required=True)
    # hosted_by_startup = forms.ModelChoiceField(queryset=startUp.objects.all(), required=False)
    # hosted_by_mentor = forms.ModelChoiceField(queryset=Mentor.objects.all(), required=False)
    hosted_by = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    location = forms.CharField(max_length=100)
    start_date = forms.DateTimeField(required=True)
    end_date = forms.DateTimeField(required=True)
    public_url = forms.URLField(max_length=500, required=False)
    event_image = forms.FileField(required=False)


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
    name_of_startup = forms.CharField(max_length=100, label='Name of Startup', required=True)
    startup_logo = forms.ImageField(required=False)
    linkedin_url = forms.URLField(required=False)
    facebook_url = forms.URLField(required=False)
    company_website = forms.URLField(required=False)
    twitter_handle = forms.CharField(max_length=50, required=False)
    inc_year = forms.IntegerField(required=False)
    type_of_trade = forms.ChoiceField(choices=TYPE_OF_TRADE, widget=forms.Select(), required=True)
    description = forms.CharField(widget=forms.Textarea, required=False)
    team_size = forms.ChoiceField(choices=TEAM_SIZE, widget=forms.Select(), required=False)
    location = forms.CharField(max_length=250, required=False)
    company_tagline = forms.CharField(max_length=100, required=False)


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


class AddMentorForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name', required=False)
    last_name = forms.CharField(max_length=30, label='Last Name', required=False)
    email = forms.EmailField(required=True)
    image = forms.FileField(required=False)
    linkedin_url = forms.URLField(required=False)
    facebook_url = forms.URLField(required=False)
    twitter_handle = forms.URLField(required=False)
    company_name = forms.CharField(max_length=200, required=False)
    expertise = forms.CharField(max_length=100, required=False)
    past_experience = forms.CharField(widget=forms.Textarea, required=False)
    about = forms.CharField(widget=forms.Textarea, required=False)

