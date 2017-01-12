from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from server import ErrorCode
from server.forms import UploadImageForm, UploadFileForm


class UploadPicture(APIView):

    @staticmethod
    def post(request):
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            return Response({'success': True,
                         'payload': {
                             'image_id': image.id
                         }})
        return Response({'success': False,
                         'error': {
                             'code': ErrorCode.INPUT_DATA_INVALID,
                             'message': 'Wrong format or invalid file.'
                         }}, status=status.HTTP_406_NOT_ACCEPTABLE)


class UploadFile(APIView):

    @staticmethod
    def post(request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save()
            return Response({'success': True,
                         'payload': {
                             'image_id': file.id
                         }})
        return Response({'success': False,
                         'error': {
                             'code': ErrorCode.INPUT_DATA_INVALID,
                             'message': 'Invalid file.'
                         }}, status=status.HTTP_406_NOT_ACCEPTABLE)