from django.contrib.auth import login
from django.http import HttpResponseNotAllowed

# Create your views here.
from django.shortcuts import render_to_response
from accounts.models import UserForm


def user(request, id):
    return render_to_response('user.html')


def create(request, id):
    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid:
            user = form.save()
            return login(request, user)
    return  HttpResponseNotAllowed(['POST'])