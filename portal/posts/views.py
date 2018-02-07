# Django Related imports.

from django.db.models import Q

# Miscellaneous Impoert
import datetime
import traceback
import os
from portal import boto_helper
from portal.settings import  posts_images_file_path, CDN_DOMAIN
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request

# Rest Framework Imports.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, views
from rest_framework.decorators import api_view

# Model imports.
from startups.models import startUp
from posts.models import post, ConfessionPost, Comment
from users.models import Mentor, MyUser

# Serializer class imports.
from posts.serializers import *
from users.serializers import MyUserSerializerFields, MentorFieldsSerializer,\
        MentorPostCreatedSerializer
from startups.serializers import StartUpSerializerFields, StartupPostCreatedSerializer


class PostHandler(APIView):
    
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def post(self, request):
        
        file_path = posts_images_file_path
        if request.user.is_authenticated():
            try:
                user = request.user
                request.data['poster'] = user.id
                if user.startup is not None:
                    posting_startup = user.startup
                    request.data['posting_startup'] = posting_startup.id
                
                # uploading image to s3
                if 'post_image' in request.data:
                    try:
                        
                        post_image = request.FILES.get('post_image')
                        file_name = ('-').join(str(datetime.datetime.now()).split(' ')) + str(post_image) 
                        image_file = open(os.path.join(file_path, file_name), 'wb')
                        image_file.write(post_image.read())
                        image_file.close()
                        post_image_path = boto_helper.upload_image(file_path, file_name)

                        post_image_s3 = "https://" + CDN_DOMAIN + "/" + file_name
                        request.data['post_image'] = post_image_s3

                    except Exception as e:
                        err = repr(e)
                        return Response({
                            "success"   : False,
                            "error"     : err,
                            "status"    : status.HTTP_500_INTERNAL_SERVER_ERROR,
                            }, status.HTTP_500_INTERNAL_SERVER_ERROR)

                if 'post_url' in request.data and request.data['post_url']:

                    page = requests.get(request.data['post_url'])
                    if int(page.status_code) == 200 :
                        soup = BeautifulSoup(page.content)
                        if soup.find('meta', property='og:title'):
                            request.data['post_url_title'] = soup.find('meta', property='og:title')['content']
                        if soup.find('meta', property='og:description')['content']:
                            request.data['post_url_description'] = soup.find('meta', property='og:description')['content']
                        if soup.find('meta', property='og:image'):
                            request.data['post_url_image'] = soup.find('meta', property='og:image')['content']

                            post_favicon_url = create_fav_icon(request.data['post_url'])
                            request.data['post_url_favicon'] = post_favicon_url
                    else:
                        pass

                created_post = PostCreateSerializer(data=request.data)
                if created_post.is_valid():
                    created_post.save()
                    data = created_post.data
                    if user.startup:
                        data.pop('poster')
                        startup = startUp.objects.get(id=user.startup.id)
                        data.pop('posting_startup')
                        serialized_startup = StartupPostCreatedSerializer(startup)
                        startup_data = serialized_startup.data
                        data['posting_startup'] = startup_data
                        data['liked'] = False
                    else:
                        data.pop('posting_startup')
                        u = data.pop('poster')
                        mentor = Mentor.objects.get(id=user.id)
                        serialized_mentor = MentorPostCreatedSerializer(mentor)
                        data['posting_mentor'] = serialized_mentor.data
                        data['liked'] = False
                    return Response({
                        'success': True,
                        'data': data,
                        'status': status.HTTP_200_OK,
                        })
                else:
                    return Response({
                        'success': False,
                        'status': status.HTTP_400_BAD_REQUEST ,
                        'error': "Data is not valid. Please re-check data sent.",
                        'data-errors': created_post.errors,
                        }, status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                err = repr(e)
                return Response({
                    'success'   : False,
                    'error'     : "Some error occurred while saving your post. Please try to post again." ,
                    'msg'       :  err,
                    'status'    : status.HTTP_500_INTERNAL_SERVER_ERROR
                    }, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                "success"       : False,
                "error"         : "Authentication Failed Please provide token",
                "status"        : status.HTTP_401_UNAUTHORIZED,
                }, status.HTTP_401_UNAUTHORIZED)

    # Delete view. Accepts post_id as a requirement and deletes the post corresponding to that id
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def delete(self, request):
        
        if request.user.is_authenticated():
            try:
                assert 'post_id' in request.data
                delete_post = post.objects.get(id = request.data['post_id'])
                if delete_post.poster == request.user:
                    delete_post.delete()
                    return Response({
                        'success'   : True,
                        'status'    : status.HTTP_200_OK,
                        'message': "Post was Successfully deleted."
                        })
                else:
                    return Response({
                        'success'   : False,
                        'status'    : status.HTTP_403_FORBIDDEN,
                        'error' : "Not authorised to delete this post."
                        }, status.HTTP_403_FORBIDDEN)

            except AssertionError:
                return Response({
                    'success'   : False,
                    'status'    : status.HTTP_400_BAD_REQUEST,
                    'error'     : "Post_id parameter not passed in request."
                    }, status.HTTP_400_BAD_REQUEST)
            except post.DoesNotExist:
                return Response({
                    'success'   : False,
                    'status'    : status.HTTP_404_NOT_FOUND,
                    'error'     : "id does not match any existing post entry."
                    }, status.HTTP_404_NOT_FOUND)

        else:
            return Response({
                "success"       : False,
                "error"         : "Authentication Failed Please provide token",
                "status"        : status.HTTP_401_UNAUTHORIZED,
                }, status.HTTP_401_UNAUTHORIZED)


# FBV for Editing a post.
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
@api_view(['POST'])
def EditPost(request):

    file_path = posts_images_file_path
    if request.user.is_authenticated():
        
        try:
            # Check if post_id present in request or not.
            p_id = request.data["post_id"]
            assert p_id != ""

            p_id = request.data['post_id']
            edited_post = post.objects.get(id = p_id)
            if edited_post.poster == request.user:
                request.data['poster'] = request.user.id

                # uploading image to s3
                if 'post_image' in request.data:
                    try:
                        
                        post_image = request.FILES.get('post_image')
                        file_name = str(post_image)
                        image_file = open(os.path.join(file_path, file_name), 'wb')
                        image_file.write(post_image.read())
                        image_file.close()
                        post_image_path = boto_helper.upload_image(file_path, str(post_image))
                        post_image_s3 = "https://" + CDN_DOMAIN + "/" + file_name
                        request.data['post_image'] = post_image_s3

                    except Exception as e:

                        err = repr(e)
                        return Response({
                            "success"   : False,
                            "error"     : err,
                            "status"    : status.HTTP_500_INTERNAL_SERVER_ERROR,
                            }, status.HTTP_500_INTERNAL_SERVER_ERROR)

                serialized_data = PostSerializerFields(edited_post, data=request.data)

                if serialized_data.is_valid():
                    serialized_data.save()
                    return Response({
                        'success'   : True , 
                        'data'      : serialized_data.data ,
                        'status'    : status.HTTP_200_OK,
                        })
                else:
                    return Response({
                        'success'       : False , 
                        'status'        : status.HTTP_400_BAD_REQUEST , 
                        'error'         : "Data is not valid. Please re-check data sent.",
                        'data-errors'   : serialized_data.errors,
                        }, status.HTTP_400_BAD_REQUEST)

            else:
                 return Response({
                    'success'   : False,
                    'status'    : status.HTTP_403_FORBIDDEN,
                    'confirmation-message' : "Not authorised to edit this post."
                    } ,status.HTTP_403_FORBIDDEN)

        except AssertionError:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST ,
                'error': "Please re-check your data. 'post_id' is missing." ,
                'success': False,
                }, status.HTTP_400_BAD_REQUEST )
        except post.DoesNotExist:
            return Response({
                'status'    : status.HTTP_404_NOT_FOUND ,
                'error'     : "Please re-check your data. The given id doesn't return a post instance." ,
                'success'   : False,
                }, status.HTTP_404_NOT_FOUND)
    else:
        # User is not authentication and need to login.
        return Response({
            'success'   : False,
            'status'    : status.HTTP_401_UNAUTHORIZED , 
            'error'     : "User not Authenticated. You are required to authenticate to acces this endpoint."
            }, status.HTTP_401_UNAUTHORIZED)


# FBV for news feed of a user
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def NewsFeed(request):
    if request.user.is_authenticated():
        try:

            user = request.user
            assert request.GET.get('page_no')
            page_no = request.GET.get('page_no')
            queryset = []
            page_no = int(page_no)*10
            query = post.objects.filter(Q(reported=False), Q(confession=False)).order_by('-created_timestamp')[page_no-10: page_no]
           
            # for u in founders:
            #   # Now fetching and iterating over every StartUp that the founders have followed
            #   for s in u.following_startup.all():
            #       # Iterating over All post fetched and append it to a common query set.
            #       for p in s.posting_startup.all():
            #                   # If the post is already in the query set then pass
            #                   if p in queryset:
            #                       pass
            #                   else:
            #                       queryset.append(p)
            # query = query[int(start):int(start)+10]
            # for q in query:
            #   queryset.append(q)
            # queryset.sort(key = attrgetter('created_timestamp') , reverse = True)
            serialized_posts = PostSerializerFields(query, many = True)
            data = serialized_posts.data

            i = 0
            
            for current_post in serialized_posts.data:
                # Ordered dictionary returned. Hence need to update. Convert to dict for traversal
                post_id = dict(serialized_posts.data[i])['id']
                current_post = post.objects.get(id=post_id)
                
                if current_post.posting_startup:

                    startup = startUp.objects.get(id=current_post.posting_startup.id)
                    serialized_startup = StartUpSerializerFields(startup)
                    startup_data = serialized_startup.data
                    if user in startup.following_company.all():
                        startup_data['followed'] = True
                    else:
                        startup_data['followed'] = False
                    data[i]['posting_startup'] = startup_data

                    if user.startup:

                        if user.startup.id == current_post.posting_startup.id:   
                            data[i]['is_editable'] = True
                        else:
                            data[i]['is_editable'] = False
                else:

                    if current_post.poster.id == user.id:
                        mentor = Mentor.objects.get(id=current_post.poster.id)
                        serialized_mentor = MentorFieldsSerializer(mentor)
                        data[i]['posting_mentor'] = serialized_mentor.data
                        data[i]['is_editable'] = True

                    else:
                        mentor = Mentor.objects.get(id = current_post.poster.id)
                        serialized_mentor = MentorFieldsSerializer(mentor)
                        data[i]['posting_mentor'] = serialized_mentor.data
                        data[i]['is_editable'] = False

                if user.startup:
                    cofounders = user.startup.cofounders.all()
                    for founder in cofounders:
                        if founder in current_post.likers.all():
                            post_liked = True
                        else:
                            post_liked = False
                else:

                    if request.user in current_post.likers.all():
                        post_liked = True
                    else:
                        post_liked = False

                # Fetch all comments related and count likers and comments. Also Append post_liked flag.
                comm_count = current_post.comments.all().count()
                like_count = current_post.likers.all().count()
                data[i].update({'comment_count': comm_count, 'likers_count': like_count, 'liked': post_liked})
                i += 1

            return Response({
                    'success'   : True,
                    'status'    : status.HTTP_200_OK,
                    'data'      : data,
                    })

        except AssertionError as e:
            return Response({
                    'success'   : False,
                    'status'    : status.HTTP_400_BAD_REQUEST,
                    'error'     : "Please check integrity of parameters passed."
                },status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            e = repr(e)

            return Response({
                    'success'   : False,
                    'status'    : status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'error'     : e
                }, status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({
            "success"   :   False,
            "error"     :   "Please provide Authentication details.",
            "status"    :   status.HTTP_401_UNAUTHORIZED, 
            }, status.HTTP_401_UNAUTHORIZED)


# """Influencer News Feed."""
# @authentication_classes((TokenAuthentication,))
# @api_view(["GET"])
# def InfluencerNewsFeed(request):
#     """
#     FBV for Influencer News Feed. Returns relevent posts of the companies the user might have followed.
#     ---
#     parameters:
#     - name: start
#       description: Starting flag of the page requested.
#       type: query
#       paramType: query
#       required: true
#     """
    
#     try:
#         assert request.GET.get("start")
#         starting = request.GET.get("start")
        
#         current_queryset = []
        
#         """Fetch Posts and convert them into list objects before appending them WRT the user."""
#         if request.user.mentor and request.user.mentor in Mentor.objects.all():
#             for startup in request.user.mentor.following_startup.all():
#                 """Relation manager Returned. Converting into list of objects."""
#                 posts = list(startup.posting_startup.all())
#                 current_queryset.append(posts)
            
#             """Reduce List of list into a single list of post objects."""
#             queryset = []
#             for entry in current_queryset:
#                 if isinstance(entry,list):
#                     for p in entry:
#                         queryset.append(p)
#                 else:
#                     pass

#             queryset.sort(key = attrgetter("created_timestamp") , reverse = True)
#             queryset = queryset[int(starting):int(starting)+10]

#             i = 0
            

#             if queryset:
#                 serialized_posts = PostSerializerFields(queryset , many = True, context={'request': request})
#                 for current_post in serialized_posts.data:
#                     """Ordered dictionary returned. Hence need to update. Convert to dict for traversal"""
#                     post_id = dict(serialized_posts.data[i])['id']
#                     current_post = post.objects.get(id = post_id)
                    
#                     if request.user in current_post.likers.all():
#                         post_liked = True
#                     else:
#                         post_liked = False

#                     """Fetch all comments related and count likers and comments. Also Append post_liked flag."""
#                     comm_count = current_post.comments.all().count()
#                     like_count = current_post.likers.all().count()
#                     serialized_posts.data[i].update({'comment_count' : comm_count , 'likers_count' : like_count , 'liked' : post_liked})
                    
#                     i = i+1

#                 return Response({
#                     'success'   : True,
#                     'status'    : status.HTTP_200_OK,
#                     'data'      : serialized_posts.data,
#                 })
#             else:
#                 return Response({
#                     'success'   : True,
#                     'status'    : status.HTTP_200_OK,
#                     'message'   : "No posts to return."
#                 })
#     except MyUser.DoesNotExist:
#         try:
#             """Fetch Posts and convert them into list objects before appending them WRT the user."""
#             for startup in request.user.investor.following_startup.all():
                
#                 """Relation manager Returned. Converting into list of objects."""
#                 posts = list(startup.posting_startup.all())
#                 current_queryset.append(posts)

#             """Reduce a list of lists into a flat list."""
#             queryset = []
#             for entry in current_queryset:
#                 if isinstance(entry,list):
#                     for p in entry:
#                         queryset.append(p)
#                 else:
#                     pass
            
#             queryset.sort(key = attrgetter("created_timestamp") , reverse = True)
#             queryset = queryset[int(starting):int(starting)+10] 
            
#             i = 0

#             if queryset:
#                 serialized_posts = PostSerializerFields(queryset , many = True, context={'request': request})
#                 for current_post in serialized_posts.data:
#                     """Ordered dictionary returned. Hence need to update. Convert to dict for traversal"""
#                     post_id = dict(serialized_posts.data[i])['id']
#                     current_post = post.objects.get(id = post_id)
                    
#                     if request.user in current_post.likers.all():
#                         post_liked = True
#                     else:
#                         post_liked = False

#                     """Fetch all comments related and count likers and comments. Also Append post_liked flag."""
#                     comm_count = current_post.comments.all().count()
#                     like_count = current_post.likers.all().count()
#                     serialized_posts.data[i].update({'comment_count' : comm_count , 'likers_count' : like_count , 'liked' : post_liked})
                    
#                     i = i+1

#                 return Response({
#                     'success'   : True,
#                     'status'    : status.HTTP_200_OK,
#                     'data'      : serialized_posts.data,
#                 })
#             else:
#                 return Response({
#                     'success'   : True,
#                     'status'    : status.HTTP_200_OK,
#                     'message'   : "No posts to return."
#                 })
#         except MyUser.DoesNotExist:
#             return Response({
#                     'success'   : False,
#                     'status'    : status.HTTP_404_NOT_FOUND,
#                     'error'   : "No User found. Does not belong to influencers.",
#                 },status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({
#                 'success'   : True,
#                 'status'    : status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 'message'   : "We encountered and error. Please report this.",
#             },status.HTTP_500_INTERNAL_SERVER_ERROR)
            
#     except AssertionError:
#         return Response({
#             'success'   : True,
#             'status'    : status.HTTP_400_BAD_REQUEST,
#             'error'   : "Please Check parameters.",
#         },status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({
#             'success'   : True,
#             'status'    : status.HTTP_500_INTERNAL_SERVER_ERROR,
#             'error'     : "We encountered and error. Please report this.",
#         },status.HTTP_500_INTERNAL_SERVER_ERROR)


# Function Based View for getting list of Comments or details of likers.
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def liker_or_comments(request):

    try:
        data = {}
        likes_s = {}
        likes_m = {}
        like_startups = {}
        like_mentors = {}
        likes = []
        comments = []

        assert 'post_id' in request.GET
        user = request.user
        p_id = request.GET.get('post_id')
        current_post = post.objects.get(id = p_id)
        post_likers = current_post.likers.all()
        for liker in post_likers:
            if liker.startup:
                startup = liker.startup
                serialized_startup = StartUpSerializerFields(startup)
                startup_data = serialized_startup.data
                startup_data['image'] = startup_data.pop('startup_logo')
                likes_s['startup'] = startup_data
                like_startups['like'] = likes_s
                likes.append(like_startups)
            else:
                mentor = Mentor.objects.get(id = liker.id)
                serialized_mentor = MentorFieldsSerializer(mentor)
                mentor_data = serialized_mentor.data
                likes_m['mentor'] = mentor_data
                like_mentors['like'] =likes_m
                likes.append(like_mentors)
        
        post_comments = current_post.comments.all()
        for comment in post_comments:
            if comment.comment_poster.startup:
                comment_startups = {}
                
                comment_serializer = CommentSerializer(comment)
                startup = comment.comment_poster.startup
                serialized_startup = StartUpSerializerFields(startup)
                startup_data = serialized_startup.data
                startup_data['image'] = startup_data.pop('startup_logo')
                comment_data = comment_serializer.data
                comment_data['startup'] =startup_data
                
                if user.startup:
                    if user.startup == comment.comment_poster.startup:
                        is_editable = True
                    else:
                        is_editable = False
                else:
                    is_editable = False
               
                comment_data['is_editable'] = is_editable
                comment_startups['comment'] = comment_data
                comments.append(comment_startups)
                
            else:
                comment_mentors = {}
                comment_serializer = CommentSerializer(comment)
                mentor = Mentor.objects.get(id = comment.comment_poster.id)
                serialized_mentor = MentorFieldsSerializer(mentor)
                mentor_data = serialized_mentor.data
                comment_data = comment_serializer.data
                comment_data['mentor'] = mentor_data

                if user.startup:
                    is_editable = False

                else:
                    if user == comment.comment_poster:
                        is_editable = True
                    else:
                        is_editable = False  
                comment_data['is_editable'] = is_editable
                comment_mentors['comment'] = comment_data
                comments.append(comment_mentors)

        data['likes'] = likes
        data['comments'] = comments
        return Response({
                'status'    : status.HTTP_200_OK,
                'data'      : data ,
                'success'   : True,
                })
    except AssertionError:
        return Response({
            'success'   :   False,
            'error'     :   'Parameters missing or not sent properly. Please check data submission.',
            'status'    :   status.HTTP_400_BAD_REQUEST,
            },status.HTTP_400_BAD_REQUEST)

    except post.DoesNotExist:
        return Response({
                'success'   : False,
                'status'    : status.HTTP_404_NOT_FOUND,
                'error'     : "No such post exists."
                },status.HTTP_404_NOT_FOUND)
    except Exception as e:
        e = repr(e)

        return Response({
                    'success'   : False,
                    'status'    : status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'error'     : "Some error occurred "
                }, status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentHandler(APIView):

    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def get(self , request):
        try:
            
            assert request.GET.get("start")
            assert request.GET.get("post_id")
            starting = request.GET.get("start")
            p_id = request.GET.get("post_id")   

            comments = Comment.objects.filter(parent_post_id=p_id)[int(starting):int(starting)+10]
            
            if comments.exists():
                serialized_comments = CommentSerializerFields(comments , many = True)
                return Response({
                    'success'   :   True,
                    'data'      :   serialized_comments.data,
                    'status'    :   status.HTTP_200_OK              
                    })
            else:
                return Response({
                    'success'   :   True,
                    'data'      :   'No more Comments.',
                    'status'    :   status.HTTP_200_OK              
                    })
        except AssertionError:
            return Response({
                'success'   :   False,
                'error'     :   'Please check parameters.',
                'status'    :   status.HTTP_400_BAD_REQUEST
                }, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            err = repr(e)
            return Response({
                'success'   :   False,
                'error'     :   err,
                'status'    :   status.HTTP_500_INTERNAL_SERVER_ERROR
                }, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def post(self , request):
        try:
            assert 'comment_text' and 'parent_post' in request.data
            user = request.user
            request.data['comment_poster'] = user.id
            created_comment = CommentCreateSerializer(data=request.data)
            if created_comment.is_valid():
                created_comment.save()
                # created_comment = CommentSerializerFields(comment, context={'request': request})
                
                data = created_comment.data
               
                if user.startup:
                    startup = startUp.objects.get(id=user.startup.id)
                    serialized_startup = StartupPostCreatedSerializer(startup)
                    data['startup'] = serialized_startup.data
                    data.pop('comment_poster')
                else:
                    mentor  = Mentor.objects.get(id=user.id)
                    serialized_mentor = MentorPostCreatedSerializer(mentor)
                    data['mentor'] = serialized_mentor.data
                    data.pop('comment_poster')
                
                return Response({
                'status'    : status.HTTP_200_OK,
                'success'   : True, 
                'data'      : data,
                })
            else:
                return Response({
                'status'    : status.HTTP_400_BAD_REQUEST,
                'success'   : False , 
                'error'     : created_comment.errors
                },status.HTTP_400_BAD_REQUEST)    

        except AssertionError as e:
            err = repr(e)
            return Response({
                'status'    : status.HTTP_400_BAD_REQUEST,
                'success'   : False,
                'error'     :  err
                }, status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({
                'status'    : status.HTTP_400_BAD_REQUEST,
                'success'   : False , 
                'error'     : 'Please check parameters. Make sure you have provided the correct information.'
                }, status.HTTP_400_BAD_REQUEST)

    # Delete Function for comments
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def delete(self, request):
        try:
            assert 'comment_id' in request.data

            comment = Comment.objects.get(id=request.data['comment_id'])
            if comment.comment_poster == request.user:
                comment.delete()
                return Response({
                    'status'    : status.HTTP_200_OK,
                    'success'   : True,
                    'message'   : 'The comment has been successfully deleted.'
                    })
            else:
                return Response({
                'status': status.HTTP_403_FORBIDDEN,
                'success': False,
                'message': 'Forbidden'
                }, status.HTTP_403_FORBIDDEN)

        except AssertionError:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'success': False,
                'error': 'Please check parameters. Make sure you have provided sufficient information.'
                }, status.HTTP_400_BAD_REQUEST)

        except Comment.DoesNotExist:
            return Response({
                'status'    : status.HTTP_404_NOT_FOUND,
                'success'   : False , 
                'error'     : 'No such comment exists.'
                }, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status'    : status.HTTP_500_INTERNAL_SERVER_ERROR,
                'success'   : False , 
                'error'     : e,
                }, status.HTTP_500_INTERNAL_SERVER_ERROR)


# FBV to edit comments.Using Post method."""
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
@api_view(['POST'])
def EditComment(request):

    try:
        assert 'comment_text' and 'comment_id' in request.data
        comment = Comment.objects.get(id = request.data['comment_id'])
        request.data['comment_poster'] = request.user.id

        edited_comment = CommentSerializerFields(comment, data=request.data)
        if edited_comment.is_valid():
            comment = edited_comment.save()
            edited_comment = CommentSerializerFields(comment)
            return Response({
                'status'    : status.HTTP_200_OK,
                'success'   : True, 
                'data'      : edited_comment.data,
                })
        else:
            return Response({
                'status'    : status.HTTP_400_BAD_REQUEST,
                'success'   : False , 
                'error'     : edited_comment.errors
                }, status.HTTP_400_BAD_REQUEST)

    except AssertionError:
        return Response({
            'status'    : status.HTTP_400_BAD_REQUEST,
            'success'   : False,
            'error'     : 'Please check parameters. Make sure you have provided sufficient information.'
            }, status.HTTP_400_BAD_REQUEST)

    except ValueError:
        return Response({
            'status'    : status.HTTP_400_BAD_REQUEST,
            'success'   : False , 
            'error'     : 'Please check parameters. Make sure you have provided the correct information.'
            }, status.HTTP_400_BAD_REQUEST)

    except Exception:
        return Response({
            'status'    : status.HTTP_500_INTERNAL_SERVER_ERROR,
            'success'   : False , 
            'error'     : 'We are facing some problem. Please report this to the admin.'
            }, status.HTTP_500_INTERNAL_SERVER_ERROR)


class LikeorUnlike(views.APIView):

    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def post(self, request):
        try:
            assert 'like' in request.data
            if int(request.data['like']):
                try:
                    assert request.data['post_id']
                    p_id = request.data['post_id']
                    selected_post = post.objects.get(id = p_id)
                    user = request.user
                    if user in selected_post.likers.all():
                        return Response({
                            'success'   : True ,
                            'status'    : status.HTTP_200_OK ,
                            'message'   : "This post has been already liked.",
                        })
                    else:
                        selected_post.likers.add(user)
                        return Response({
                            'success'   : True ,
                            'status'    : status.HTTP_200_OK ,
                            'message'   : "This post has been liked.",
                            })
                except AssertionError:
                    return Response({
                        'success'   : False ,
                        'error'     : 'Check parameters, id of post not provided.',
                        'status'    : status.HTTP_400_BAD_REQUEST,
                    }, status.HTTP_400_BAD_REQUEST)
                except post.DoesNotExist:
                    return Response({
                        'success'   : False ,
                        'error'     : 'No such post exists.',
                        'status'    : status.HTTP_400_BAD_REQUEST,
                        }, status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response({
                        'success'   :   False,
                        'error'     :   "Some error occurred with us. Please report this.",
                        'status'    :   status.HTTP_500_INTERNAL_SERVER_ERROR,
                        }, status.HTTP_500_INTERNAL_SERVER_ERROR)          
            else:
                try:
                    assert request.data['post_id']
                    p_id = request.data['post_id']
                    selected_post = post.objects.get(id = p_id)
                    user = request.user
                    selected_post.likers.remove(user)
                    return Response({
                        'success'   : True ,
                        'status'    : status.HTTP_200_OK ,
                        'message'   : "This post has been unliked.",
                        })
                
                except AssertionError:
                    return Response({
                        'success'   : False ,
                        'error'     : 'Check parameters, id of post not provided.',
                        'status'    : status.HTTP_400_BAD_REQUEST,
                    }, status.HTTP_400_BAD_REQUEST)
                
                except post.DoesNotExist:
                    return Response({
                        'success'   : False ,
                        'error'     : 'No such post exists.',
                        'status'    : status.HTTP_400_BAD_REQUEST,
                        }, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                        'success'   : False ,
                        'error'     : 'Please check parameters. And report this.',
                        'status'    : status.HTTP_400_BAD_REQUEST,
                    }, status.HTTP_400_BAD_REQUEST)


@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def MyPosts(request):
    try:
        user = request.user
        assert request.GET.get('id')
        assert request.GET.get('category')
        id = request.GET.get('id')
        category = request.GET.get('category')

        if str(category) == 'startup':
            startup = startUp.objects.get(id = int(id))
            posts = post.objects.filter(posting_startup=startup)
            serialized_posts = Mypostserializer(posts, many=True)
            serialized_startup = StartupPostCreatedSerializer(startup)
            posts_data = serialized_posts.data
            i = 0
            for current_post in posts_data:
                posts_data[i].pop('poster')
                cofounders = startup.cofounders.all()
                c_post = post.objects.get(id=int(posts_data[i]['id']))
                likers_count = c_post.likers.all().count()
                
                if user in c_post.likers.all():
                    post_liked = True
                else:
                    post_liked = False
                posts_data[i]['posting_startup'] = serialized_startup.data
                posts_data[i]['liked'] = post_liked
                posts_data[i]['likers'] = likers_count
                i = i+1

            return Response({
                'success'   :True,
                'data'      : posts_data,
                'status'    : status.HTTP_200_OK ,
                })

        else:
            mentor = Mentor.objects.get(id=int(id))
            posts = post.objects.filter(poster=mentor.id)
            serialized_posts = Mypostserializer(posts, many=True)
            posts_data = serialized_posts.data
            i = 0
            for current_post in posts_data:
                posts_data[i].pop('posting_startup')
                posts_data[i].pop('poster')
                
                serialized_mentor = MentorPostCreatedSerializer(mentor)
                
                c_post = post.objects.get(id=int(posts_data[i]['id']))
                likers_count = c_post.likers.all().count()
                if user in c_post.likers.all():
                    post_liked = True
                else:
                    post_liked = False

                posts_data[i]['posting_mentor'] = serialized_mentor.data
                posts_data[i]['liked'] = post_liked
                posts_data[i]['likers'] = likers_count
                i = i+1

            return Response({
                'success'   :True,
                'data'      : posts_data,
                'status'    : status.HTTP_200_OK ,
                })

    except AssertionError:
        return Response({
            'success'   : False,
            'status'    : status.HTTP_400_BAD_REQUEST,
            'error'     : "parameters missing pls check the parameters",
            }, status.HTTP_400_BAD_REQUEST)

    except Exception as e:

        return Response({
            'success'   : False,
            'status'    : status.HTTP_400_BAD_REQUEST,
            'error'     : "error has occured",
            }, status.HTTP_400_BAD_REQUEST)


@authentication_classes((TokenAuthentication,))
@api_view(['POST'])
def ConfessionPostCreate(request):
    try:
        file_path = posts_images_file_path
        assert 'post_text' in request.data
        user = request.user
        request.data['poster'] = user.id
        if user.startup is not None:
            request.data['posting_startup'] = user.startup.id

        if 'post_image' in request.data:
            try:

                post_image = request.FILES.get('post_image')
                file_name = ('-').join(str(datetime.datetime.now()).split(' ')) + str(post_image)
                image_file = open(os.path.join(file_path, file_name), 'wb')
                image_file.write(post_image.read())
                image_file.close()
                post_image_path = boto_helper.upload_image(file_path, file_name)
                post_image_s3 = "https://" + CDN_DOMAIN + "/" + file_name
                request.data['post_image'] = post_image_s3

            except Exception as e:
                err = repr(e)
                return Response({
                    "success": False,
                    "error": err,
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }, status.HTTP_500_INTERNAL_SERVER_ERROR)

        request.data['confession'] = True
        created_post = ConfessionPostCreateSerializer(data=request.data)
        if created_post.is_valid():
            created_post.save()
            data = created_post.data
            data.pop('poster')
            data.pop('posting_startup')
            data['upvotes'] = 0
            data['upvote'] = False
            data['downvotes'] = 0
            data['downvote'] = False

            return Response({
                'status': status.HTTP_201_CREATED,
                'data': data,
                'success' : True
            }, status.HTTP_201_CREATED)

        else:

            return Response({
                'status' : status.HTTP_400_BAD_REQUEST,
                'success' : False,
                'errors' : created_post.errors,
            }, status.HTTP_400_BAD_REQUEST)
    except AssertionError:

        return Response({
            'status' : status.HTTP_400_BAD_REQUEST,
            'success' : False,
            'error' : 'Post Text missing '
        }, status.HTTP_400_BAD_REQUEST)

    except Exception as e:

        return  Response({
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'success': False,
            'error' : 'Exception occurred . Please Report this'
        }, status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes((TokenAuthentication,))
@api_view(['GET'])
def ConfessionNewsFeed(request):
    try:
        assert request.GET.get('page_no')
        page_no = request.GET.get('page_no')
        page_no = int(page_no) * 10
        user = request.user
        confessions = ConfessionPost.objects.all().order_by('-created_timestamp')[page_no-10: page_no]

        serialized_confessions = ConfessionPostSerializer(confessions, many=True)
        serialized_data = serialized_confessions.data

        i = 0
        for data in serialized_data:
            post_id = dict(serialized_data[i])['id']
            confession = ConfessionPost.objects.get(id=post_id)

            if user.startup:
                cofounders = user.startup.cofounders.all()
                for founder in cofounders:
                    if founder in confession.upvotes.all():
                        upvote, downvote = True, False

                    elif founder in confession.downvotes.all():
                        upvote, downvote = False, True
                    else:
                        upvote, downvote = False, False

            else:
                if user in confession.upvotes.all():
                    upvote, downvote = True, False

                elif user in confession.downvotes.all():
                    upvote, downvote = False, True
                else:
                    upvote, downvote = False, False

            upvotes = confession.upvotes.count()
            downvotes = confession.downvotes.count()
            serialized_data[i]['upvote'] = upvote
            serialized_data[i]['downvote'] = downvote
            serialized_data[i]['upvote_count'] = upvotes
            serialized_data[i]['downvote_count'] = downvotes

            i += 1

        return Response({
            'data':  serialized_data,
            'status': status.HTTP_200_OK,
            'sucess': True
        })

    except AssertionError:

        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'success': False,
            'error': 'Page no missing '
        }, status.HTTP_400_BAD_REQUEST)



    except Exception as e:
        return Response({
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'success': False,
            'error': 'Exception occurred . Please Report this'
        }, status.HTTP_500_INTERNAL_SERVER_ERROR)



@authentication_classes((TokenAuthentication,))
@api_view(['POST'])
def ConfessionUpvoteorDownvote(request):

    try:
        assert 'post_id' in request.data

        user = request.user
        p_id = request.data['post_id']
        selected_post = ConfessionPost.objects.get(id=p_id)

        if 'upvote' in request.data:
            if int(request.data['upvote']):
                try:
                    if user in selected_post.upvotes.all():
                        return Response({
                            'success': True,
                            'status': status.HTTP_200_OK,
                            'message': "This post has been already upvoted.",
                        })
                    else:
                        selected_post.upvotes.add(user)
                        serialized_confession = ConfessionPostSerializer(selected_post)
                        data = serialized_confession.data
                        data['upvote'] = True
                        data['upvotes'] = selected_post.likers.count()
                        return Response({
                            'success': True,
                            'status': status.HTTP_200_OK,
                            'message': "This post has been upvoted.",
                            'post': data
                        })

                except Exception as e:
                    return Response({
                        'success': False,
                        'error': "Some error occurred with us. Please report this.",
                        'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    }, status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:

                selected_post.upvotes.remove(user)
                serialized_confession = ConfessionPostSerializer(selected_post)
                data = serialized_confession.data
                data['upvote'] = False
                data['upvotes'] = selected_post.upvotes.count()
                return Response({
                    'success': True,
                    'status': status.HTTP_200_OK,
                    'message': "Upvote has been removed.",
                    'post': data
                })

        elif 'downvote' in request.data:
            if int(request.data['downvote']):
                try:
                    if user in selected_post.downvotes.all():
                        return Response({
                            'success': True,
                            'status': status.HTTP_200_OK,
                            'message': "This post has been already downvoted.",
                        })
                    else:
                        selected_post.downvotes.add(user)
                        serialized_confession = ConfessionPostSerializer(selected_post)
                        data = serialized_confession.data
                        data['downvote'] = True
                        data['downvotes'] = selected_post.likers.count()
                        return Response({
                            'success': True,
                            'status': status.HTTP_200_OK,
                            'message': "This post has been downvotes.",
                            'post': data
                        })

                except Exception as e:
                    return Response({
                        'success': False,
                        'error': "Some error occurred with us. Please report this.",
                        'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    }, status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:

                selected_post.downvotes.remove(user)
                serialized_confession = ConfessionPostSerializer(selected_post)
                data = serialized_confession.data
                data['downvote'] = False
                data['downvotes'] = selected_post.upvotes.count()
                return Response({
                    'success': True,
                    'status': status.HTTP_200_OK,
                    'message': "Downvote has been removed.",
                    'post': data
                })

    except post.DoesNotExist:
        return Response({
            'success': False,
            'error': 'No such post exists.',
            'status': status.HTTP_404_NOT_FOUND,
        }, status.HTTP_404_NOT_FOUND)

    except AssertionError:

        return Response({
            'success': False,
            'error': 'Check parameters, post_id or upvote value not  provided.',
            'status': status.HTTP_400_BAD_REQUEST,
        }, status.HTTP_400_BAD_REQUEST)

    except Exception as e:

        return Response({
            'success': False,
            'error': 'Please check parameters. And report this.',
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
        }, status.HTTP_400_BAD_REQUEST)


def create_fav_icon(url):
    page = requests.get(url)

    if 'yourstory' in url:
        post_url_favicon_s3 = 'https://d30kf02i9qby6l.cloudfront.net/2016-09-29-14%3A08%3A23.343184favicon.png'
    else:

        if page.status_code == 200:
            soup = BeautifulSoup(page.content)
            icon_link = soup.find("link", rel="icon")
            icon = icon_link['href']

            file_path = posts_images_file_path
            file_name = ('-').join(str(datetime.datetime.now()).split(' ')) + str('favicon.png')
            urllib.request.urlretrieve(icon, str(file_path) + file_name)
            post_url_favicon_path = boto_helper.upload_image(file_path, file_name)
            post_url_favicon_s3 = "https://" + CDN_DOMAIN + "/" + file_name

        else:
            post_url_favicon_s3 = None

    return post_url_favicon_s3


