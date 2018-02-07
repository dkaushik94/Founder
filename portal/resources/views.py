'''------------------------------------------------------------------------------------'''

#Django related imports.

'''------------------------------------------------------------------------------------'''

#RestFramework Imports.
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework import status
from rest_framework.decorators import api_view

'''------------------------------------------------------------------------------------'''

#Model imports.
from .models import Resource

'''------------------------------------------------------------------------------------'''


'''FBV for Resources. Download.'''
@authentication_classes((TokenAuthentication,))
@api_view(['GET'])
def GetResources(request):
    """
        Function based View to return resources available in database.   
    """
    request.META['HTTP_HOST'] = '54.201.230.174'

    try:
        mark = request.GET.get("mark")
        resources = Resource.objects.all()[int(mark):int(mark)+10]
        assert resources.exists()
        serialized_resources = ResourceSerializer(resources , many = True)
        if Resource.objects.all()[int(mark)+10:].exists():
            return Response({
                "success"           :   True ,
                "resources_left"    :   True ,
                "data"              :   serialized_resources.data ,
                "status"            :   status.HTTP_200_OK ,
                })
        else:
            return Response({
                "success"           :   True ,
                "resources_left"    :   False ,
                "data"              :   serialized_resources.data ,
                "status"            :   status.HTTP_200_OK ,
                })
    except Exception:
        return Response({
            "success"           :   False ,
            "message"           :   "Server error occurred. Please Report this." ,
            "status"            :   status.HTTP_500_INTERNAL_SERVER_ERROR ,
            })