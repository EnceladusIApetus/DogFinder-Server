from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from server.models import Coordinate
from server.serializers import CoordinateSerializer


class hello(APIView):
    def get(self, request, format=None):
        snippets = Coordinate.objects.all()
        serializer = CoordinateSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CoordinateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class snippet_detail(APIView):
    def get_object(self, pk):
        try:
            return Coordinate.objects.get(pk=pk)
        except Coordinate.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer = CoordinateSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        serializer = CoordinateSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)