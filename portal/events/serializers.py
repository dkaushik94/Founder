#Rest Framework imports.
from rest_framework import serializers

#Database model imports
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (('id' , 'name_of_event' , 'start_date' , 'end_date' , 'event_image', 'description',
                   'public_url', 'location'))


class EventSerializerFields(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = (('id' , 'name_of_event' , 'start_date' , 'end_date' , 'event_image', 'description',
                   'public_url', 'location' ))

