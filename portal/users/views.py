#  Django Related imports

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils.crypto import get_random_string
import boto.ses 
import datetime
import traceback
from portal import boto_helper
from portal.settings import  user_images_file_path, CDN_DOMAIN

#  Rest Framework imports.
from rest_framework.response import Response
from rest_framework.authentication import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, views
from rest_framework.decorators import api_view
from rest_framework import generics

# layer imports
from .layer import generate_identity_token


#  Importing models
from .models import MyUser
from startups.models import startUp

# Importing serializers
from .serializers import *
from startups.serializers import StartUpSerializer

#  Form imports
from users.forms import AddUserForm

# Form imports
from users.forms import *

#  Miscellaneous Imports.
import subprocess , os


# CBV for User Login.
class Login(views.APIView):

    def post(self, request):

        try:
            assert 'username' in request.data
            assert 'password' in request.data
            
            email = request.data['username']
            password = request.data['password']
            nonce = request.data['nonce']
            username = MyUser.objects.get(email=email).username
            user = authenticate(username=username, password=password)
            if user is not None:

                login(request, user)

                # If token exists then get else create it for the user
                token = Token.objects.get_or_create(user = user)

                if type(token) == type((1,2)):
                    token_key = token[0].key
                else:
                    token_key = token.key

                try:
                    mentor = Mentor.objects.get(id=user.id)
                    user_id = str(user.id)
#                     if mentor.identity_token:
#                         pass
#                     else:

                    identityToken = generate_identity_token(email, nonce, mentor.image)
                    mentor.identity_token = identityToken
                    mentor.save()
                    serialized_mentor = MentorSerializer(mentor)
                    data = serialized_mentor.data
                    data['auth_token'] = token_key
                    data['chat_password'] = mentor.chat_password
                    data['chat_user'] = mentor.chat_user
                    # data['identity_token'] = identityToken
                    return Response({
                        'success'       : True,
                        'mentor'        : data,
                        'status_code'   : status.HTTP_200_OK
                        })

                except Mentor.DoesNotExist:
                    startup = user.startup
                    startup_id = str(startup.id)
#                     if startup.identity_token:
#                         pass
#                     else:
                    identityToken = generate_identity_token(startup.name_of_startup, nonce, startup.startup_logo)
                    startup.identity_token = identityToken
                    startup.save()
                    serialized_user = UserloginSerializer(user)
                    serialized_cofounders = StartUpSerializer(startup)
                    data = serialized_cofounders.data
                    data['auth_token'] = token_key

                    return Response({
                        'success': True,
                        # 'auth_token'    : token_key,
                        'startup': data,
                        'status_code': status.HTTP_200_OK,
                        })
            else:
                    user = None
                    token_key = None
                    return Response({
                    'success'       : False,
                    'auth_token'    : token_key,
                    'user'          : user,
                    'error'         : 'Username or password invalid',
                    'status_code' : status.HTTP_400_BAD_REQUEST
                    }, status.HTTP_400_BAD_REQUEST)

        except MyUser.DoesNotExist:
            user = None
            token_key = None
            return Response({
            'success': False,
            'auth_token': token_key,
            'user': user,
            'error': 'No such user exists',
            'status': status.HTTP_404_NOT_FOUND,
            }, status.HTTP_404_NOT_FOUND)

        except AssertionError  as e:
            return Response({
                'error' : 'parameter not recieved',
                'status_code'   : status.HTTP_400_BAD_REQUEST
                }, status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            err = repr(e)
            return Response({
                'success':False,
                'error': err,
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                }, status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes((TokenAuthentication,))
@api_view(["POST"])
def ReturnIdentityToken(request):
    try:
        assert request.data["nonce"]
        nonce_string = request.data["nonce"]
        try:
            mentor = Mentor.objects.get(id=request.user.id)
            user_id = str(request.user.id)

            identityToken = generate_identity_token(request.user.email, nonce_string, mentor.image)
            mentor.identity_token = identityToken
            mentor.save()
            return Response({
                'success'       : True,
                'identity_token': identityToken,
                'status_code'   : status.HTTP_200_OK
            })

        except Mentor.DoesNotExist:
            startup = request.user.startup
            startup_id = str(startup.id)
            identityToken = generate_identity_token(startup.name_of_startup, nonce_string, startup.startup_logo)
            startup.identity_token = identityToken
            startup.save()
            return Response({
                'success': True,
                'identity_token': identityToken,
                'status_code': status.HTTP_200_OK,
            })
    except MyUser.DoesNotExist:
        user = None
        token_key = None
        return Response({
            'success'       : False,
            'auth_token'    : token_key,
            'user'          : user,
            'error'         : 'No such user exists',
            'status'        : status.HTTP_404_NOT_FOUND,
        }, status.HTTP_404_NOT_FOUND)

    except AssertionError  as e:
        return Response({
            'error': 'parameter not recieved',
            'status_code': status.HTTP_400_BAD_REQUEST
        }, status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        err = repr(e)
        return Response({
            'success':False,
            'error': err,
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
        }, status.HTTP_500_INTERNAL_SERVER_ERROR)

 
# CBV for adding cofounder via App
class AddCoFounder(views.APIView):

    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def post(self, request):
        try:
            assert 'email' in request.data
            email = request.data['email']

            # finding the current user
            current_user = request.user
            # selecting the  current startup 
            startup = current_user.startup

            # connecting to boto using  key_id and access_key
            conn = boto.ses.connect_to_region(
                    'us-west-2',
                    aws_access_key_id='AKIAJDC3JOCQK3LCVTHA',
                    aws_secret_access_key='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')

            # setting email as username and email and startup for the cofounder
            user = MyUser.objects.create(email=email, username=email,startup=startup)
            # Generating a random 8_length token string
            invite_token = get_random_string(length=8)
            # setting the invite token as password
            user.set_password(invite_token)
            user.save()

            html = '<html><head><title>Approved</title><head><body> ' + \
                   '<div><p>Hello your request for Founders has been approved.' + \
                   'Below are your attached username and password <br> username : ' + \
                   email + '<br> password : ' + invite_token + '<br>' + \
                   'You can now login to the app <br><br>Regards<br>Founder</body></html>'

            # sending the mail
            try:
                conn.send_email(
                    'karan@grappus.com',
                    'Request Approved',
                    None,
                    [email],
                    format='html',
                    html_body=html,
                  )
                return Response({
                            'success'   : True ,
                            'msg'       : 'mail sent to cofounder',
                            'status'    : status.HTTP_200_OK,
                            })
            except Exception as e:
                err = repr(e)
                MyUser.objects.filter(email = email).delete()
                return Response({
                'error': err,
                'status': status.HTTP_400_BAD_REQUEST,
                })
        except AssertionError:
            return Response({
                'error': 'email not recieved'
                })
        except Exception as e:
                err = repr(e)
                return Response({
                'error' : err,
                'status' : status.HTTP_400_BAD_REQUEST,
                })


# CBV for User Related Queries
class UserHandler(views.APIView):

    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def get(self, request):
        try:
            assert request.GET.get('id')
            user = MyUser.objects.get(id=request.GET.get('id'))
            serialized_cofounder = UserSerializer(user)
            return Response({
                'sucess': True,
                'cofounder': serialized_cofounder.data,
                'status': status.HTTP_200_OK
                })

        except AssertionError:
            return Response({
                'success'       :   False ,
                'error'         :   'user_id not provided',
                'status_code'   :   status.HTTP_400_BAD_REQUEST,
            }, status.HTTP_400_BAD_REQUEST)

        except MyUser.DoesNotExist:
            return Response({
                'success'   : False ,
                'error'     : 'No such User Exists',
                'status'    : status.HTTP_404_NOT_FOUND
            }, status.HTTP_404_NOT_FOUND)

        except Exception as e:
            e = repr(e)
            return Response({
                'success'   : False ,
                'error'     : e,
                'status'    : status.HTTP_500_INTERNAL_SERVER_ERROR,
                }, status.HTTP_500_INTERNAL_SERVER_ERROR)

    # This method is to accept request for editing and changing the details of profile of founders.
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def post(self, request):

        file_path = user_images_file_path
        try:
            assert 'id' in request.data
            user = MyUser.objects.get(id=request.data['id'])
            if request.user in user.startup.cofounders.all():

                if request.FILES.get('image'):
                    image = request.FILES.get('image')
                    if image._size > 0:
                        file_name = str(image)
                        image_file = open(os.path.join(file_path, file_name), 'wb')
                        image_file.write(image.read())
                        image_file.close()
                        image_path = boto_helper.upload_image(file_path, str(image))
                        image_s3 = "https://" + CDN_DOMAIN + "/" + file_name
                        request.data['image'] = image_s3
                    else:
                        pass

                cofounder_edited = UserSerializer(user, request.data)
                if cofounder_edited.is_valid():
                    cofounder_edited.save()
                    return Response({
                        'success': True ,
                        'message': 'All the details have been updated',
                        'cofounder': cofounder_edited.data,
                        'status': status.HTTP_200_OK,
                    })
                else:
                    return Response({
                        'success' : False ,
                        'error' : 'Serializer data is invalid.',
                        'serializer_errors': cofounder_edited.errors,
                        'status' : status.HTTP_400_BAD_REQUEST,
                        }, status.HTTP_400_BAD_REQUEST)

            else:
                return Response({
                    'success': False,
                    'error': 'Not Authorised to edit the details',
                    'status': status.HTTP_403_FORBIDDEN
                    }, status.HTTP_403_FORBIDDEN)
        except AssertionError:
            return Response({
                'success':False,
                'error':' cofounderid not provided',
                'status_code':status.HTTP_400_BAD_REQUEST,
            }, status.HTTP_400_BAD_REQUEST)

        except MyUser.DoesNotExist:
            return Response({
                'success': False,
                'error': 'No such User Exists',
                'status': status.HTTP_404_NOT_FOUND
            }, status.HTTP_404_NOT_FOUND)

        except Exception as e:
            e = repr(e)
            return Response({
                'success'   : False ,
                'error'     : e,
                'status'    : status.HTTP_500_INTERNAL_SERVER_ERROR,
                }, status.HTTP_500_INTERNAL_SERVER_ERROR)


class MentorHandler(views.APIView):
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def get(self, request):

        if request.user.is_authenticated():

            try:
                assert request.GET.get('mentor_id')

                mentor_id = request.GET.get("mentor_id")
                mentor = Mentor.objects.get(id=mentor_id)
                serialized_mentor = MentorSerializer(mentor)
                return Response({
                    'success': True,
                    'mentor': serialized_mentor.data,
                    'status': status.HTTP_200_OK
                    }, status.HTTP_200_OK)

            except AssertionError:
                return Response({
                    'success':   False ,
                    'error':   'mentor_id not provided',
                    'status_code':   status.HTTP_400_BAD_REQUEST,
                }, status.HTTP_400_BAD_REQUEST)

            except Mentor.DoesNotExist:
                return Response({
                    'success'   : False ,
                    'error'     : 'No such Mentor Exists',
                    'status'    : status.HTTP_404_NOT_FOUND
                }, status.HTTP_404_NOT_FOUND)

            except Exception as e:
                e = repr(e)
                return Response({
                    'success'   : False ,
                    'error'     : e,
                    'status'    : status.HTTP_500_INTERNAL_SERVER_ERROR,
                    }, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                "success"       : False,
                "error"         : "Authentication Failed Please provide token",
                "status"        : status.HTTP_401_UNAUTHORIZED,
                }, status.HTTP_401_UNAUTHORIZED)

    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def post(self, request):

        file_path = user_images_file_path

        try:
            assert 'id' in request.data
            mentor = Mentor.objects.get(id=request.data['id'])
            if mentor.id == request.user.id:

                if request.FILES.get('image'):
                    image = request.FILES.get('image')
                    if image._size > 0:

                        file_name =  ('-').join(str(datetime.datetime.now()).split(' ')) + str(image)
                        image_file = open(os.path.join(file_path, file_name), 'wb')
                        image_file.write(image.read())
                        image_file.close()
                        image_path = boto_helper.upload_image(file_path, file_name)
                        image_s3 = "https://" + CDN_DOMAIN + "/" + file_name
                        request.data['image'] = image_s3
                    else:
                        pass
                edited_mentor = MentorSerializer(mentor, data = request.data)

                if edited_mentor.is_valid():
                    edited_mentor.save()

                    return Response({
                            "sucess"    : True,
                            "error"   : "Details successfully edited",
                            "mentor"    : edited_mentor.data,
                            "status"    : status.HTTP_200_OK
                        }, status.HTTP_200_OK)
                else:

                    return Response({
                        'success' : False ,
                        'error' : 'Serializer data is invalid.',
                        'serializer_errors' : edited_mentor.errors,
                        'status' : status.HTTP_400_BAD_REQUEST,
                        }, status.HTTP_400_BAD_REQUEST)
            else:

                return Response({
                        'success' : False ,
                        'error' : 'Not authorised to edit the details',
                        'status' : status.HTTP_403_FORBIDDEN,
                        }, status.HTTP_403_FORBIDDEN)

        except AssertionError:
            return Response({
                'success'       :   False ,
                'error'         :   'id not provided',
                'status_code'   :   status.HTTP_400_BAD_REQUEST
            }, status.HTTP_400_BAD_REQUEST)

        except Mentor.DoesNotExist:
            return Response({
                'success'   : False ,
                'error'     : 'No such Mentor Exists',
                'status'    : status.HTTP_404_NOT_FOUND,
            }, status.HTTP_404_NOT_FOUND)

        except Exception as e:
            traceback.print_exc()
            e = repr(e)
            return Response({
                'success'   : False ,
                'error'     : e,
                'status'    : status.HTTP_500_INTERNAL_SERVER_ERROR,
                }, status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
@api_view(['POST'])
def Logout_User(request):
    user = request.user
    # request.user.auth_token.delete()
    try:
        mentor = Mentor.objects.get(id=user.id)
        if mentor.identity_token:
            mentor.identity_token = None
            mentor.save()
    except Mentor.DoesNotExist:
        startup = user.startup        
        if startup.identity_token:
            startup.identity_token = None
            startup.save()
    
#     logout(user)
    return Response({
        'success': True,
        'message': 'Successfully logged out',
        'status': status.HTTP_200_OK
        }, status.HTTP_200_OK)


@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def MentorsList(request):

    mentors = Mentor.objects.all()
    mentor_serializers = MentorFieldsSerializer(mentors, many=True)
    return Response({
        'success': True,
        'mentors': mentor_serializers.data,
        'status':status.HTTP_200_OK
    },  status.HTTP_200_OK)


class MentorSearch(generics.ListAPIView):

    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def get(self, request):

        mentor_name = self.request.query_params.get('mentor_name', None)
        view_all = request.GET.get('view_all')
        view_all = int(view_all)
        if mentor_name is not None:
            if view_all:
                queryset = Mentor.objects.filter(first_name__icontains=mentor_name)
                serialized_mentors = MentorFieldsSerializer(queryset, many=True)
                return Response({
                'success': True,
                'mentors': serialized_mentors.data,
                'status': status.HTTP_200_OK,
                })
            else:
                queryset = Mentor.objects.filter(first_name__icontains=mentor_name)[0:9]
                serialized_mentors = MentorFieldsSerializer(queryset, many=True)
                return Response({
                    'success': True,
                    'mentors': serialized_mentors.data,
                    'status': status.HTTP_200_OK,
                })
        else:
            return Response({
                'sucess': False,
                'error' : 'No name specified',
                'status': status.HTTP_400_BAD_REQUEST,
                }, status.HTTP_400_BAD_REQUEST)


def AddFounderfromForm(request):

    file_path = user_images_file_path
    if request.method == 'POST':
        form = AddUserForm(request.POST , request.FILES)

        if form.is_valid():
            add_another_founder = form.cleaned_data['add_another_founder']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            startup = form.cleaned_data['startup']
            linkedin_url = form.cleaned_data['linkedin_url']
            facebook_url = form.cleaned_data['facebook_url']
            twitter_handle = form.cleaned_data['twitter_handle']
            about = form.cleaned_data['about']

            if request.FILES['image']:
                image = request.FILES['image']
                file_name = str(image)
                image_file = open(os.path.join(file_path, file_name), 'wb')
                image_file.write(image.read())
                image_file.close()
                image_path = boto_helper.upload_image(file_path, str(image))
                image_s3 = "https://" + CDN_DOMAIN + "/" + file_name
            else:
                image_s3 = ''

            startup = startUp.objects.get(name_of_startup=startup)

            created_user = MyUser.objects.create(username=email, email=email, first_name=first_name,
                                                 last_name=last_name, facebook_url=facebook_url,
                                                 linkedin_url=linkedin_url, twitter_handle=twitter_handle,
                                                 image=image_s3, startup=startup, about=about)

            created_user.save()

            if add_another_founder:
                return redirect('/user/addfounder')
            else:
                return redirect('/approvalrequest/')

        else:
            return render(request, 'users/addfounders.html', {'form': form, 'errors': form.errors})
    else:
        form = AddUserForm()
        return render(request, 'users/addfounders.html', {'form': form})


def InApproval(request):

    return render(request, 'users/inapproval.html')



