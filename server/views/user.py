from django.contrib.auth import authenticate, logout
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from server import ErrorCode
from server.models import User
from server.serializers import FullAccountSerializer, BasicAccountSerializer


class UserAuthentication():
    def __init__(self):
        pass

    class UserLogin(APIView):
        @staticmethod
        def post(request):
            try:
                user = authenticate(fb_id=request.data.get('fb_id', None))
                if user is None:
                    serializer = FullAccountSerializer(data=request.data)
                    if serializer.is_valid():
                        user = serializer.save()
                    else:
                        return Response({'success': False,
                                         'error': {
                                             'code': ErrorCode.INPUT_DATA_INVALID,
                                             'message': 'Input data invalid.'
                                         }}, status=status.HTTP_406_NOT_ACCEPTABLE)
                return Response({'success': True,
                                 'payload': {
                                     'token': Token.objects.get(user=user).key,
                                     'user_data': FullAccountSerializer(user).data
                                 }}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({'success': False,
                                 'error': {
                                     'code': 500,
                                     'message': 'Internal Server Error: ' + str(ex)
                                 }}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    class UserLogout(APIView):
        @staticmethod
        def get(request, format=None):
            logout(request)
            return Response({'success': True})

    class IsAuthenticate(APIView):
        @staticmethod
        def get(request, format=None):
            return Response({'success': True,
                             'payload': {
                                 'status': request.user.is_authenticated()
                             }})


class UserData():
    def __init__(self):
        pass

    class SelfInfo(APIView):
        permission_classes = (IsAuthenticatedOrReadOnly,)

        @staticmethod
        def get(request):
            serializer = FullAccountSerializer(request.user)
            return Response({'success': True,
                             'payload': {
                                 'user_data': serializer.data
                             }})

        @staticmethod
        def put(request):
            try:
                serializer = FullAccountSerializer(request.user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'success': True})
                return Response({'success': False,
                                 'error': {
                                     'code': ErrorCode.INPUT_DATA_INVALID,
                                     'message': 'Input data invalid.'
                                 }}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except Exception as ex:
                return Response({'success': False,
                                 'error': {
                                     'code': ErrorCode.INTERNAL_SERVER_ERROR,
                                     'message': 'Internal Server Error: ' + str(ex)
                                 }}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        @staticmethod
        def delete(request):
            request.user.set_inactive()
            return Response({'success': True})

    class GetUser(APIView):
        permission_classes = (IsAuthenticatedOrReadOnly,)

        def get(self, request):
            user = BasicAccountSerializer(User.objects.get(pk=request.query_params.get('id', 0)))
            if user:
                return Response({'success': True,
                                 'payload': {
                                     'user_data': user.data
                                 }})
            return Response({'success': False,
                             'error': {
                                 'code': ErrorCode.DATA_NOT_FOUND,
                                 'message': 'Data not found.'
                             }}, status=status.HTTP_404_NOT_FOUND)
