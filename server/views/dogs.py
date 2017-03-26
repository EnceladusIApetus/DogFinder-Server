import random

import numpy
from django.conf import settings
from django.core.files import File
from django.shortcuts import render
from fcm_django.models import FCMDevice
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from modules import cluster
from modules import feature_extractor, feature_selector, data_manager, nearest_neighbors
from modules import sentence_generator
from server import CloudMessenger
from server import ErrorCode
from server import ResponseFormat
from server import models
from server.forms import UploadImageForm
from server.models import Dog, Image, User, LostAndFound
from server.serializers import DogSerializer, LostAndFoundSerializer, BasicAccountSerializer, ImageSerializer
from django.core.cache import caches

import threading, names, requests


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
                return Response(ResponseFormat.error(ErrorCode.INPUT_DATA_INVALID, "Input data invalid."),
                                status=status.HTTP_406_NOT_ACCEPTABLE)
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
        try:
            limit = int(request.query_params['limit'])
            end = limit * int(request.query_params['page'])
            dogs = request.user.dog_set.all()[end - limit:end]
            serializer = DogSerializer(dogs, many=True)
            return Response(ResponseFormat.success({'dogs': serializer.data}))
        except:
            return Response(
                ResponseFormat.error(ErrorCode.INPUT_DATA_INVALID, "Required parameters are not fulfilled."),
                status=status.HTTP_406_NOT_ACCEPTABLE)


class Instance(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @staticmethod
    def post(request):
        try:
            dog = Dog.objects.get(pk=request.data.get("dog")['id'])
            if request.user.has_perm('manage_own_dog', dog) is True:
                image = Image.objects.get(pk=request.data.get('image_id', 0))
                instance = dog.instance_set.create(image=image)
                ExtractFeature(instance, image.path.url).start()
                return Response(ResponseFormat.success())
        except Exception as ex:
            return Response(ResponseFormat.error(ErrorCode.INTERNAL_SERVER_ERROR, str(ex)),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(ResponseFormat.error(403, "Wrong permission."), status=status.HTTP_403_FORBIDDEN)
        except Dog.DoesNotExist | models.Instance.DoesNotExist:
            return Response(ResponseFormat.error(ErrorCode.DATA_NOT_FOUND, "Dog or image not found on server."),
                            status=status.HTTP_404_NOT_FOUND)


threadLimiter = threading.BoundedSemaphore(2)


class ExtractFeature(threading.Thread):
    def __init__(self, instance, path):
        super(ExtractFeature, self).__init__()
        self.instance = instance
        self.path = path

    def run(self):
        threadLimiter.acquire()
        try:
            self.execute()
        finally:
            threadLimiter.release()

    def execute(self):
        self.instance.raw_features = feature_extractor.extract(settings.BASE_DIR + self.path)
        feature_selector.load()
        self.instance.reduced_features = feature_selector.reduce_features([self.instance.raw_features])[0]
        self.instance.save()


class AddDogSamples(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        (instances, paths, file_names, original_labels) = data_manager.read_data(settings.BASE_DIR +
                                                                                 '/data/samples/output/dogsColor')

        rootDir = settings.BASE_DIR + '/data/samples/orderDogsIn/'

        feature_selector.load()
        reduced_features_instances = feature_selector.reduce_features(instances)
        cluster.load()
        labels = cluster.predict(reduced_features_instances)
        for index in range(0, len(instances)):
            dog = Dog(name=names.get_first_name(), breed='thousand way', age=random.randint(1, 20),
                      user=User.objects.get(pk=8))
            dog.save()
            image = Image()
            f = open(rootDir + str(original_labels[index]) + '/' + file_names[index], 'r')
            image.path.save(file_names[index], File(f))
            image.save()
            instance = models.Instance(dog=dog, image=image, label=labels[index],
                                       raw_features=", ".join(str(x) for x in instances[index]),
                                       reduced_features=", ".join(
                                           str(x) for x in reduced_features_instances[index]))
            instance.save()

        return Response(ResponseFormat.success())


class FindSimilarDogs(APIView):
    # @staticmethod
    # def get(request):
    #     return render(request, 'server/alike_faces.html')

    @staticmethod
    def get(request):
        try:
            cache = caches['default']
            dog = Dog.objects.get(pk=request.query_params['dog_id'])
            lost_and_founds = cache.get('lost_and_found_dog_id_' + str(dog.id))
            if lost_and_founds is None:
                reduced_features = feature_extractor.convert_to_float(dog.instance_set.first().reduced_features)
                lost_and_founds = LostAndFound.objects.filter(dog_id__in=find(reduced_features))
                cache.set('lost_and_found_dog_id_' + str(dog.id), lost_and_founds, 240)
            return Response(ResponseFormat.success({
                'lost_and_founds': LostAndFoundSerializer(lost_and_founds, many=True).data
            }))
        except Dog.DoesNotExist:
            return Response(ResponseFormat.error(500, 'error'))

    @staticmethod
    def post(request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.save()
            raw_features = feature_extractor.extract(settings.BASE_DIR + image.path.url)
            feature_selector.load()
            reduced_features = feature_selector.reduce_features([raw_features])[0]
            dog_id_list = find(reduced_features)
            lost_and_founds = LostAndFound.objects.filter(dog_id__in=dog_id_list)
            objects = dict([(obj.dog.id, obj) for obj in lost_and_founds])
            sorted_objects = [objects[id] for id in dog_id_list]
            lost_and_founds = LostAndFoundSerializer(sorted_objects, many=True).data
            return Response(ResponseFormat.success({
                'lost_and_founds': lost_and_founds
            }))
        return Response(ResponseFormat.error(500, 'error'))


def find(reduced_features):
    instances = models.Instance.objects.values_list('id', 'reduced_features', 'dog_id')
    id_arr = []
    reduced_features_arr = []
    dog_id_arr = []
    for tuple in instances:
        id_arr.append(tuple[0])
        reduced_features_arr.append(feature_extractor.convert_to_float(tuple[1]))
        dog_id_arr.append(tuple[2])
    nearest_neighbors.set(10, 100)
    nearest_neighbors.fit(reduced_features_arr)
    return [dog_id_arr[i] for i in nearest_neighbors.neighbors(reduced_features)]


class LostAndFoundAPI(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(requesr):
        lostandfounds = LostAndFound.objects.filter(id__lte=50)
        return Response(
            ResponseFormat.success({'lost_and_founds': LostAndFoundSerializer(lostandfounds, many=True).data}))

    @staticmethod
    def post(request):
        try:
            dog = Dog.objects.get(pk=request.data.get('dog')['id'])
            lostandfound = LostAndFound(user=request.user, dog=dog, note=request.data.get('note'),
                                        type=request.data.get('type', 0))
            lostandfound.save()
        except Dog.DoesNotExist:
            return Response(ResponseFormat.error(ErrorCode.DATA_NOT_FOUND, 'Dog does not exist.'))
        return Response(ResponseFormat.success())


class Coordinate(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        try:
            dog = Dog.objects.get(pk=request.data.get('dog')['id'])
            lostandfound = LostAndFound(user=request.user, dog=dog, note=request.data.get('note'),
                                        type=request.data.get('type', 0))
            lostandfound.save()
        except Dog.DoesNotExist:
            return Response(ResponseFormat.error(ErrorCode.DATA_NOT_FOUND, 'Dog does not exist.'))
        return Response(ResponseFormat.success())


class GenLostAndFound(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        users = User.objects.filter(id__gte=11).filter(id__lte=20)
        size = len(users)
        dogs = Dog.objects.all()
        for index, dog in enumerate(dogs, 0):
            user = users[index % size]
            dog.user = user
            dog.latitude = random.uniform(13.672826, 13.948263)
            dog.longitude = random.uniform(100.338139, 100.894664)
            dog.save()
            lost_and_found = LostAndFound.objects.create(type=LostAndFound.LOST, user=user, dog=dog)
            lost_and_found.save()
        return Response(ResponseFormat.success())


class LoopThroughAll(APIView):
    @staticmethod
    def get(request):
        for item in LostAndFound.objects.all():
            item.note = sentence_generator.sing_sen_maker()
            item.save()
        return Response(ResponseFormat.success())


class TestNoti(APIView):
    @staticmethod
    def get(request):
        CloudMessenger.send_notification(None, 'hiiiii', 'helloooo')
        CloudMessenger.send_data(None, {'hello': 'hiiii'})
        return Response(ResponseFormat.success())