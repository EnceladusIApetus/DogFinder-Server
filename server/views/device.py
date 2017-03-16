from fcm_django.models import FCMDevice
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from server import ErrorCode
from server import ResponseFormat


class UpdateFCMToken(APIView):

    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        try:
            device = FCMDevice.objects.filter(user_id=request.user.id).first()
            if device is None:
                FCMDevice.objects.create(registration_id=request.data['registration_id'], type='android',
                                         user=request.user)
            else:
                device.registration_id = request.data['registration_id']
                device.save()
            return Response(ResponseFormat.success())
        except:
            return Response(ResponseFormat.error(ErrorCode.INTERNAL_SERVER_ERROR, 'Could not create or update the token.'), status=status.HTTP_500_INTERNAL_SERVER_ERROR)