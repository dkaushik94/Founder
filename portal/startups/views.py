# Django related imports

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string

from portal import boto_helper
from portal.settings import startup_images_file_path, CDN_DOMAIN
import datetime
import os
import traceback
from django.db.models import Q

# Rest Framework Imports.
from rest_framework.authentication import  TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.views import APIView
from rest_framework import status, views
from rest_framework import filters
from rest_framework import generics

# Database model related imports.
from users.models import MyUser
from .models import startUp

# Serializer class Imports.
from .serializers import *
from users.serializers import *

# Form Imports
from startups.forms import *


class StartUpHandler(APIView):

    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def post(self, request):

        file_path = startup_images_file_path

        try:
            user = request.user
            s_id = request.data['id']
            Startup = startUp.objects.get(id=s_id)

            if user in Startup.cofounders.all():

                # if request.data['company_tagline']:
                #     a = request.data['company_tagline'].split(' ')[0:5]
                #     company_tagline = ' '.join(a)
                #     request.data['company_tagline'] = company_tagline

                if request.FILES.get('startup_logo'):
                    try:
                        startup_logo = request.FILES.get('startup_logo')
                        file_name = 'sl_' + str(startup_logo)
                        image_file = open(os.path.join(file_path, file_name), 'wb')
                        image_file.write(startup_logo.read())
                        image_file.close()
                        startup_logo_path = boto_helper.upload_image(file_path, file_name)
                        startup_logo_s3 = "https://" + CDN_DOMAIN + "/" + file_name
                        request.data['startup_logo'] = startup_logo_s3
                        Startup.startup_logo = startup_logo_s3
                        Startup.save()

                    except Exception as e:
                        err = repr(e)

                        return Response({
                            "success": False,
                            "error": err,
                            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                        }, status.HTTP_500_INTERNAL_SERVER_ERROR)

                startup_edited = StartupEditSerializer(Startup, data=request.data)
                if startup_edited.is_valid():
                    startup_edited.save()
                    startup_edited = StartupEditedSerializer(Startup)

                    return Response({
                        'success': True,
                        'message': 'Data successfully edited',
                        'startup': startup_edited.data,
                        'status': status.HTTP_200_OK,
                    })
                else:
                    return Response({
                        'success': False,
                        'error': 'Serializer data is invalid.',
                        'serialized_data': startup_edited.data,
                        'serializer_errors': startup_edited.errors,
                        'status': status.HTTP_400_BAD_REQUEST,
                    }, status.HTTP_400_BAD_REQUEST)

            else:
                return Response({
                    'success': False,
                    'error': 'Cannot edit this Startup, not a cofounder ',
                    'status': status.HTTP_403_FORBIDDEN
                }, status.HTTP_403_FORBIDDEN)

        except startUp.DoesNotExist:
            return Response({
                'success': False,
                'error': 'No startup found. ',
                'status': status.HTTP_404_NOT_FOUND,
            }, status.HTTP_404_NOT_FOUND)
        except AssertionError:
            return Response({
                'success': False,
                'error': 'Parameter Error startup_id Not provided',
                'status': status.HTTP_400_BAD_REQUEST,
            }, status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            err = repr(e)
            return Response({
                'success': False,
                'error': err,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            }, status.HTTP_500_INTERNAL_SERVER_ERROR)


class StartUpSearch(generics.ListAPIView):

    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def get(self, request):

        user = request.user
        startup_name = self.request.query_params.get('startup_name', None)
        view_all = request.GET.get('view_all')
        view_all = int(view_all)

        if startup_name is not None:
            if view_all:
                queryset = startUp.objects.filter(Q(name_of_startup__icontains=startup_name),
                                                  Q(approval_status=1))
                serialized_startups = StartUpSerializerFields(queryset, many=True)
                i = 0
                data = serialized_startups.data

                for current_startup in data:
                    startup = startUp.objects.get(name_of_startup=current_startup['name_of_startup'])

                    if user in startup.cofounders.all():
                        data[i]['own_startup'] = True
                    else:
                        data[i]['own_startup'] = False

                    if user.startup:

                        if user in startup.following_company.all():
                            data[i]['followed'] = True
                        else:
                            data[i]['followed'] = False
                    else:
                        if user in user.following_startup.all():
                            data[i]['followed'] = True
                        else:
                            data[i]['followed'] = False
                    i = i + 1

                return Response({
                    'success': True,
                    'startups': data,
                    'status': status.HTTP_200_OK,
                })
            else:
                queryset = startUp.objects.filter(Q(name_of_startup__icontains=startup_name),
                                                  Q(approval_status=1))[0:10]
                serialized_startups = StartUpSerializerFields(queryset, many=True)

                i = 0
                data = serialized_startups.data
                for current_startup in data:
                    startup = startUp.objects.get(name_of_startup=current_startup['name_of_startup'])

                    if user in startup.cofounders.all():
                        data[i]['own_startup'] = True
                    else:
                        data[i]['own_startup'] = False

                    if user.startup:

                        if user in startup.following_company.all():
                            data[i]['followed'] = True
                        else:
                            data[i]['followed'] = False
                    else:
                        if user in user.following_startup.all():
                            data[i]['followed'] = True
                        else:
                            data[i]['followed'] = False
                    i = i + 1
                return Response({
                    'success': True,
                    'startups': data,
                    'status': status.HTTP_200_OK,
                })
        else:
            return Response({
                'sucess': False,
                'error': 'No name specified',
                'status': status.HTTP_400_BAD_REQUEST,
            }, status.HTTP_400_BAD_REQUEST)


# Endpoint for StartUp Details
@authentication_classes((TokenAuthentication,))
@api_view(['GET'])
def StartUpDetails(request):

    try:

        s_id = request.GET.get('id')
        assert s_id
        startup = startUp.objects.get(id=s_id)
        serialized_data_startups = StartUpSerializer(startup, context={'request': request})
        return Response({
            'success': True,
            'startup': serialized_data_startups.data,
            'status_code': status.HTTP_200_OK
        })

    except startUp.DoesNotExist:
        return Response({
            'success': False,
            'error': 'No such startup found.',
            'status_code': status.HTTP_404_NOT_FOUND,
        }, status.HTTP_404_NOT_FOUND)
    except AssertionError:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'success': False,
            'error': 'Please Check parameters.'
        }, status.HTTP_400_BAD_REQUEST)


@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def StartupList(request):
    startups = startUp.objects.filter(approval_status=1)
    serialzed_startups = StartUpSerializerFields(startups, many=True)
    return Response({
        'status': status.HTTP_200_OK,
        'success': True,
        'startups': serialzed_startups.data
    }, status.HTTP_200_OK)


# View for following startups.
class FollowCompany(APIView):
    @authentication_classes((TokenAuthentication,))
    @csrf_exempt
    def post(self, request):
        try:
            assert request.data["follow"]
            if int(request.data['follow']):
                try:
                    assert 'id' in request.data
                    s_id = request.data['id']
                    assert s_id != ''
                    startup = startUp.objects.get(id=s_id)
                    user = request.user
                    user.following_startup.add(startup)
                    return Response({
                        'success': True,
                        'status': status.HTTP_200_OK,
                        'message': "Followed the startup successfully.",
                    })
                except AssertionError:
                    return Response({
                        'success': False,
                        'error': 'Check parameters.ID of startup not provided.',
                        'status': status.HTTP_400_BAD_REQUEST,
                    }, status.HTTP_400_BAD_REQUEST)
                except startUp.DoesNotExist:
                    return Response({
                        'success': False,
                        'error': 'No such startup exists with us.',
                        'status': status.HTTP_404_NOT_FOUND,
                    }, status.HTTP_404_NOT_FOUND)
            else:
                # Unfollow A startup.
                try:
                    assert 'id' in request.data
                    s_id = request.data['id']
                    assert s_id != ''

                    startup = startUp.objects.get(id=s_id)
                    user = request.user
                    user.following_startup.remove(startup)

                    return Response({
                        'success': True,
                        'status': status.HTTP_200_OK,
                        'message': "Un-Followed the startup successfully.",
                    })
                except AssertionError:
                    return Response({
                        'success': False,
                        'error': 'Check parameters. ID of startup not provided.',
                        'status': status.HTTP_400_BAD_REQUEST,
                    }, status.HTTP_400_BAD_REQUEST)
                except startUp.DoesNotExist:
                    return Response({
                        'success': False,
                        'error': 'No such startup exists with us.',
                        'status': status.HTTP_404_NOT_FOUND,
                    }, status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({
                'success': False,
                'error': 'Check parameters.ID of startup not provided.',
                'status': status.HTTP_400_BAD_REQUEST,
            }, status.HTTP_400_BAD_REQUEST)


# RankList Endpoint

@authentication_classes((TokenAuthentication,))
@api_view(["GET"])
def StartUpRankList(request):

    if request.method == "GET":
        try:
            rank_list = startUp.objects.filter(Q(trending=True), ~Q(rank=0)).order_by('rank')
            assert rank_list.exists()

            # Serialzied Data for Rank List
            serialized_list = RankListSerializer(rank_list, many=True, context={'request': request})

            i = 0
            for d in serialized_list.data:
                startup_id = dict(serialized_list.data[i])['id']
                current_startup = startUp.objects.get(id=startup_id)
                cofounders = current_startup.cofounders.all()
                serialized_cofounders = CofounderSerializer(cofounders, many=True)
                if request.user in current_startup.following_company.all():
                    startup_followed = True
                else:
                    startup_followed = False

                if request.user in current_startup.cofounders.all():
                    own_startup = True
                else:
                    own_startup = False

                serialized_list.data[i].update({"followed": startup_followed})
                serialized_list.data[i].update({"own_startup": own_startup})
                serialized_list.data[i].update({"cofounders": serialized_cofounders.data})

                i += 1

            return Response({
                'status': status.HTTP_200_OK,
                'data': serialized_list.data,
                'success': True,
            })

        except AssertionError:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "No Rank list is available. Contact Admin to publish it.",
                'success': True,
            }, status.HTTP_400_BAD_REQUEST)


# function for adding startup ny the user through the form
def AddStartupfromForm(request):

    if request.method == 'POST':

        file_path = startup_images_file_path

        form = AddStartupForm(request.POST, request.FILES)
        if form.is_valid():
            name_of_startup = form.cleaned_data['name_of_startup']
            linkedin_url = form.cleaned_data['linkedin_url']
            facebook_url = form.cleaned_data['facebook_url']
            twitter_handle = form.cleaned_data['twitter_handle']
            inc_year = form.cleaned_data['inc_year']
            type_of_trade = form.cleaned_data['type_of_trade']
            description = form.cleaned_data['description']
            team_size = form.cleaned_data['team_size']
            location = form.cleaned_data['location']
            company_tagline = form.cleaned_data['company_tagline']


            # reading startup_logo and uploading to s3 and saving the url to database
            if request.FILES['startup_logo']:
                startup_logo = request.FILES['startup_logo']
                startup_logo_file_name = 'startup' + ('-').join(str(datetime.now()).split(' ')) + ('-').join(str(startup_logo).split(' '))
                startup_logo_file = open(os.path.join(file_path, startup_logo_file_name), 'wb')
                startup_logo_file.write(startup_logo.read())
                startup_logo_file.close()
                startup_logo_path = boto_helper.upload_image(file_path, startup_logo_file_name)
                startup_logo_s3 = "https://" + CDN_DOMAIN + "/" + startup_logo_file_name

            chat_username = ('').join(name_of_startup.split(' '))
            chat_password = get_random_string(length=8)
            startup = startUp.objects.create(name_of_startup=name_of_startup, linkedin_url=linkedin_url,
                                             facebook_url=facebook_url, twitter_handle=twitter_handle,
                                             inc_year=inc_year, description=description, team_size=team_size,
                                             location=location, company_tagline=company_tagline,
                                             startup_logo=startup_logo_s3, chat_user=chat_username,
                                             chat_password=chat_password)
            startup.save()

            return redirect('/user/addfounder')
        else:
            return render(request, 'startups/addstartup.html', {'form': form, 'errors': form.errors})


    else:
        form = AddStartupForm()
        return render(request, 'startups/addstartup.html', {'form': form})
