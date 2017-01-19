from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from server import ErrorCode
from server import ResponseFormat
from server.models import Dog, Image, Instance
from server.serializers import DogSerializer


class IndividualDog(APIView):
    @staticmethod
    def get(request):
        try:
            dog = Dog.objects.get(pk=request.query_params.get('id', 0))
            dog_instances = dog.instance_set.all()
            return Response(ResponseFormat.success({
                                 "dog_data": DogSerializer(dog).data
                             }))
        except Dog.DoesNotExist:
            return Response(
                ResponseFormat.error(ErrorCode.DATA_NOT_FOUND, "Data not found."),
                status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return Response(
                ResponseFormat.error(ErrorCode.AUTHENTICATION_IS_REQUIRED, "This operation needs authentication."),
                status=status.HTTP_401_UNAUTHORIZED)
        serializer = DogSerializer(data=request.data)
        if serializer.is_valid():
            dog = serializer.create()
            dog.user = request.user
            dog.save()
            return Response(ResponseFormat.success())
        return Response(ResponseFormat.error(ErrorCode.INPUT_DATA_INVALID, "Input data invalid."),
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    @staticmethod
    def put(request):
        try:
            dog = Dog.objects.get(pk=request.data.get('id', 0))
            if request.user.has_perm('manage_own_dog', dog):
                serializer = DogSerializer(dog, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(ResponseFormat.success())
                return Response(ResponseFormat.error(ErrorCode.INPUT_DATA_INVALID, "Input data invalid."), status=status.HTTP_406_NOT_ACCEPTABLE)
        except Dog.DoesNotExist:
            return Response(
                ResponseFormat.error(ErrorCode.DATA_NOT_FOUND, "Data not found."),
                status=status.HTTP_404_NOT_FOUND)


class Image(APIView):

    @staticmethod
    def post(request):
        dog = request.data.get('dog', None)
        if dog:
            try:
                dog = Dog.objects.get(pk=dog.get('id', 0))
                image = Image.objects.get(pk=request.data.get('image_id', 0))
                instance = Instance.objects.create(dog=dog, image=image)
                instance.save()
                return Response()
            except Dog.DoesNotExist | Image.DoesNotExist:
                return Response(ResponseFormat.error(ErrorCode.DATA_NOT_FOUND, "Dog or image not found on server."),
                                status=status.HTTP_404_NOT_FOUND)
            except Exception as ex:
                return Response(ResponseFormat.error(ErrorCode.INTERNAL_SERVER_ERROR, str(ex)),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(ResponseFormat.error(ErrorCode.INPUT_DATA_INVALID, "Dog data is required."),
                        status=status.HTTP_406_NOT_ACCEPTABLE)