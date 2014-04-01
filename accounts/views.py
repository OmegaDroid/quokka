from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response


def user(request, p1):
    return render_to_response('user.html')