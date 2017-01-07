from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from server.serializers import CoordinateSerializer
from .models import Coordinate
from .forms import CustomUserCreationForm


def add_user(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CustomUserCreationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            user = form.save()
            return HttpResponse('success')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CustomUserCreationForm()

    return render(request, 'server/name.html', {'form': form})


def user_login(request):
    if request.POST.get('fb_id', False) is False:
        return render(request, 'server/login.html')

    user = authenticate(fb_id=request.POST.get('fb_id'))
    if user is not None:
        login(request, user)
        return HttpResponse('login success')
    else:
        return HttpResponse('login failed')


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