# Framework Imports
from rest_framework import serializers
# Model imports
from .models import startUp
# Serializer class imports.
from users.serializers import MyUserSerializerFields , UserSerializer


# Serializer class for StartUps Instances
class StartUpSerializer(serializers.ModelSerializer):
    cofounders = MyUserSerializerFields(read_only=True, many=True)

    class Meta:
        fields = ('cofounders', 'name_of_startup', 'company_website', 'id', 'inc_year', 'linkedin_url',
                  'facebook_url', 'twitter_handle', 'type_of_trade', 'description', 'team_size',
                  'location', 'company_tagline', 'startup_logo', 'identity_token')
        model = startUp
        extra_kwargs = {
            'name_of_startup': {'read_only': True},
            'inc_year': {'read_only': True},
        }


# Serializer for editing startup
class StartupEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = startUp
        fields = ('inc_year',  'linkedin_url' , 'facebook_url', 'twitter_handle',
                  'type_of_trade', 'description', 'team_size', 'company_website',
                  'location', 'startup_logo')


# This is to be used for returning whole data after the startup has been edited. includes non-editables fields too
class StartupEditedSerializer(serializers.ModelSerializer):
    class Meta:
        model = startUp
        fields = ('name_of_startup', 'id', 'inc_year', 'linkedin_url', 'company_website',
                  'facebook_url', 'twitter_handle' , 'type_of_trade' , 'description',
                  'team_size', 'location', 'company_tagline', 'startup_logo')


class StartUpSerializerFields(serializers.ModelSerializer):
    class Meta:
        model = startUp
        fields = ('id', 'name_of_startup', 'startup_logo')


class StartupPostCreatedSerializer(serializers.ModelSerializer):

    class Meta:
        model = startUp
        fields = ('id', 'name_of_startup', 'startup_logo')
    
        
# Serializer class particularly for Rank list Publishing. Not Create method performed with this serializer class
class RankListSerializer(serializers.ModelSerializer):
    class Meta:
        model = startUp
        fields = ('id', 'name_of_startup', 'startup_logo', 'rank', 'trending_reason',)


class StartupAttendees(serializers.ModelSerializer):
    class Meta:
        model = startUp
        fields = ('id', 'name_of_startup', 'startup_logo')
