# Django Related imports.
from django.views.decorators.csrf import csrf_exempt
import traceback

# Rest Framework Imports.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, api_view
from rest_framework import status

# Model imports.
from .models import Event

# Serializer class imports.
from .serializers import EventSerializer, EventSerializerFields
from users.serializers import MentorAttendees, EventHosts
from startups.serializers import StartupAttendees


class EventHandler(APIView):

    @authentication_classes((TokenAuthentication,))
    def get(self, request):

        try:
            user = request.user
            queryset = Event.objects.all().order_by("-start_date")
            assert queryset.exists() is True
            serialized = EventSerializer(queryset, many=True, context={'request': request})
            data = serialized.data
            i = 0
            for event in queryset:
                attendees = []
                data[i]['hosted_by'] = event.hosted_by
                

                for attendee in event.attendees.all():
                    if attendee.startup:
                        serialized_startup = StartupAttendees(attendee.startup)
                        startup_data = serialized_startup.data
                        startup_data['image'] = startup_data.pop('startup_logo')
                        startup_data['name'] = startup_data.pop('name_of_startup')

                        attendees.append(startup_data)
                    else:
                        serialized_mentor = MentorAttendees(attendee)
                        mentor_data = serialized_mentor.data
                        mentor_name = str(mentor_data['first_name']) + ' ' + str(mentor_data['last_name'])
                        mentor_data.pop('first_name')
                        mentor_data.pop('last_name')
                        mentor_data['name'] = mentor_name
                        attendees.append(mentor_data)

                data[i]['attendees'] = attendees

                if request.user.startup:

                    if request.user in event.attendees.all():
                        attending = True
                    else:
                        attending = False
                else:
                    if request.user in event.attendees.all():
                        attending = True
                    else:
                        attending = False

                data[i]['attending'] = attending

                i += 1

            return Response({
                "success": True,
                "data": data,
                "status": status.HTTP_200_OK,
            })
        except Exception as e:

            return Response({
                "success": False,
                "error": "No events Exists for this request parameter.",
                "status": status.HTTP_400_BAD_REQUEST
            }, status.HTTP_400_BAD_REQUEST)

    @authentication_classes((TokenAuthentication,))
    def post(self, request):

        try:
            assert 'id' in request.data
            assert 'going' in request.data

            event = Event.objects.get(id=request.data['id'])
            going = int(request.data['going'])
            user = request.user

            if going:
                event.attendees.add(user)
                return Response({
                    "success": True,
                    "message": 'The user has been added to the attendees list of the event.',
                    "status": status.HTTP_200_OK,
                })
            else:
                event.attendees.remove(user)
                return Response({
                    "success": True,
                    "message": 'The user has been removed from the attendees list of the event.',
                    "status": status.HTTP_200_OK,
                })

        except AssertionError as e:
            return Response({
                "success": False,
                "error": "Please check parameters. one or more  parameters seem to be missing.",
                "status": status.HTTP_400_BAD_REQUEST
            }, status.HTTP_400_BAD_REQUEST)
        except Event.DoesNotExist:
            return Response({
                "success": False,
                "error": "Please check parameters. No such event is present with us.",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR
            }, status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes((TokenAuthentication,))
@api_view(["GET"])
def EventDetails(request):

    if request.method == "GET":
        try:
            assert request.GET.get("event_id")

            e_id = request.GET.get("event_id")
            event = Event.objects.get(id=e_id)

            serialized_event = EventSerializer(event, context={'request': request})

            if request.user.startup:

                if request.user in event.attendees.all():
                    attending = True
                else:
                    attending = False
            else:
                if request.user in event.attendees.all():
                    attending = True
                else:
                    attending = False
            a = {}
            a.update(serialized_event.data)
            a['going'] = attending
            # serialized_event.data.update({"going": attending})

            return Response({
                "success": True,
                "data": a,  # serialized_event.data ,
                "status": status.HTTP_200_OK,
            })

        except Event.DoesNotExist:
            return Response({
                "success": False,
                "error": "Please check parameters. No such event is present with us.",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR
            }, status.HTTP_500_INTERNAL_SERVER_ERROR)

        except AssertionError as e:
            return Response({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'error': 'Please Check parameters. event_id is missing.'
            }, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'error': 'Some error occurred with our server. Please report this so that we may take action.'
            }, status.HTTP_500_INTERNAL_SERVER_ERROR)
