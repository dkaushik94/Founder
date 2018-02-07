# Framework Imports
from rest_framework import serializers
# from django.contrib.auth import update_session_auth_hash

# Model Imports.
from .models import MyUser, Mentor
from startups.models import startUp

# Mentor fields tuple. KEEP CODE DRY.
mentor_fields = ('id', 'first_name', 'last_name', 'image')


# Duplicate Instance of StartUpSerializerFields to avoid Circular dependency with User model.
class StartUpSerializerFields(serializers.ModelSerializer):
    class Meta:
        model = startUp
        fields = ('id', 'name_of_startup', 'background_startup_image', 'startup_logo')


# Serializer class for User Instances
class MyuserSerializer(serializers.ModelSerializer):
    startup = StartUpSerializerFields(read_only=True)

    class Meta:
        model = MyUser
        exclude = ('username', 'password', 'is_active', 'user_permissions', 'is_staff', 'date_joined',\
                   'last_login', 'is_superuser', 'groups')


class StartUpSerializerLogin(serializers.ModelSerializer):
    class Meta:
        model = startUp
        fields = ('name_of_startup', 'id', 'inc_year', 'linkedin_url', 'facebook_url', 'twitter_handle',\
                  'type_of_trade', 'description', 'team_size', 'location', 'company_tagline',\
                  'background_startup_image', 'startup_logo',)

class UserloginSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        exclude = ('username', 'about', 'skills', 'tagline', 'following_startup', 'password', 'is_active',
                   'user_permissions', 'is_staff', 'date_joined', 'last_login', 'is_superuser', 'groups')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'email', 'first_name', 'last_name', 'image', 'linkedin_url', 'twitter_handle',
                  'facebook_url', 'about')


class CofounderSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
#        fields = ('id', 'email', 'first_name', 'last_name', 'image', 'linkedin_url',
#                  'twitter_handle', 'facebook_url' , 'about')
        exclude = ('username', 'password', 'is_active', 'user_permissions', 'is_staff', 'date_joined',\
                   'last_login', 'is_superuser', 'groups')


# for changing the password ,
class UserPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=False, max_length=128)
    confirm_password = serializers.CharField(required=False, max_length=128)


class MyUserSerializerFields(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'first_name', 'last_name', 'image', 'email', 'designation',
                  'startup', 'twitter_handle', 'facebook_url', 'linkedin_url', 'about')


class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ('id', 'first_name', 'last_name', 'email', 'about', 'image', 'linkedin_url',
                  'twitter_handle', 'designation', 'facebook_url', 'company_name', 'expertise',
                  'past_experience', 'identity_token')


# Mentor serializer to be used in Influncer List
class MentorFieldsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mentor
        fields = ('id', 'image','first_name', 'last_name', )


class MentorAttendees(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ('id', 'image', 'first_name', 'last_name')


class MentorPostCreatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = mentor_fields


class EventHosts(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name')


# class QuestionAskerSerializerField(serializers.ModelSerializer):
#     class Meta:
#         model = MyUser
#         fields = ('username', 'first_name', 'last_name',)


# class AnswerWriterSerializerField(serializers.ModelSerializer):
#     class Meta:
#         model = MyUser
#         fields = ('username', 'first_name', 'last_name',)
