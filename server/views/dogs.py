from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from server import ErrorCode
from server import ResponseFormat
from server import models
from server.models import Dog, Image, Instance, User
from server.serializers import DogSerializer


class Individual(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @staticmethod
    def get(request):
        try:
            dog = Dog.objects.get(pk=request.query_params.get('id', 0))
            return Response(ResponseFormat.success({
                                 "dog": DogSerializer(dog).data
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
            return Response(ResponseFormat.success({'dog_id': dog.id}))
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

    @staticmethod
    def delete(request):
        try:
            dog = Dog.objects.get(pk=request.data.get('id', 0))
            if request.user.has_perm('manage_own_dog', dog):
                dog.delete()
                return Response(ResponseFormat.success())
        except Dog.DoesNotExist:
            return Response(
                ResponseFormat.error(ErrorCode.DATA_NOT_FOUND, "Data not found."),
                status=status.HTTP_404_NOT_FOUND)


class GetAllDog(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        serializer = DogSerializer(request.user.dog_set.all(), many=True)
        return Response(ResponseFormat.success({'dogs': serializer.data}))


class Instance(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    @staticmethod
    def post(request):
        dog = request.data.get('dog', None)
        if dog:
            try:
                dog = Dog.objects.get(pk=dog.get('id', 0))
                if request.user.has_perm('manage_own_dog', dog) is True:
                    image = Image.objects.get(pk=request.data.get('image_id', 0))
                    instance = dog.instance_set.create(image=image)
                    instance.save()
                    return Response(ResponseFormat.success())
                return Response(ResponseFormat.error(403, "Wrong permission."), status=status.HTTP_403_FORBIDDEN)
            except Dog.DoesNotExist | models.Instance.DoesNotExist:
                return Response(ResponseFormat.error(ErrorCode.DATA_NOT_FOUND, "Dog or image not found on server."),
                                status=status.HTTP_404_NOT_FOUND)
            except Exception as ex:
                return Response(ResponseFormat.error(ErrorCode.INTERNAL_SERVER_ERROR, str(ex)),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(ResponseFormat.error(ErrorCode.INPUT_DATA_INVALID, "Dog data is required."),
                        status=status.HTTP_406_NOT_ACCEPTABLE)