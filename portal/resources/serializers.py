'''--------------------------------------------------------------------------------------------'''

#Rest Framework imports.
from rest_framework import serializers

'''--------------------------------------------------------------------------------------------'''

#Database model imports

'''--------------------------------------------------------------------------------------------'''

#Serializer Class imports.
from .models import Resource
'''--------------------------------------------------------------------------------------------'''


"""Serializer Class for Resource Handling."""
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource