from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect

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


# @login_required()
def hello(request):
    return HttpResponse('hiiiiii')