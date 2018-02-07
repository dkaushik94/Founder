# Database Model imports.
from .models import *

# Rest Framework imports.
from rest_framework import serializers

# Serializer imports.
from users.serializers import MyUserSerializerFields
from startups.serializers import StartUpSerializerFields


# Comment Serializer Class
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'comment_text', 'created_timestamp')


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment


class CommentSerializerFields(serializers.ModelSerializer):
    # comment_poster = MyUserSerializerFields(read_only = True)
    commenting_startup = serializers.StringRelatedField(source='comment_poster.startup', read_only = True)
    startup_image = serializers.StringRelatedField(source='comment_poster.startup.startup_logo', read_only=True)

    class Meta:
        model = Comment
        extra_kwargs = {
            'parent_post': {'read_only' : True}
        }
        exclude = ('parent_post',)
        

# Serializer class for Posts.'''
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = post
        exclude = ('poster',)


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = post


# Additional serializer class with selected Fields
class PostSerializerFields(serializers.ModelSerializer):
    class Meta:
        model = post
        exclude = ('likers', 'posting_startup')

        
class Mypostserializer(serializers.ModelSerializer):
    class Meta:
        model = post
        exclude = ('likers',)


class ConfessionPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfessionPost
        fields = ('id', 'post_headline', 'post_text' , 'created_timestamp', 'updated_timestamp',
                  'post_image', 'poster', 'posting_startup', 'confession')


class ConfessionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfessionPost
        fields = ('id', 'post_headline', 'post_text', 'created_timestamp', 'updated_timestamp',
                  'post_image')
