from django.contrib.auth import login, authenticate
from django.http import HttpResponseNotAllowed
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from accounts.models import NewUserForm


def user(request, id):
    return render_to_response('user.html')


def create_user(request):
    if request.method == "GET":
        return render_to_response("create_user.html", RequestContext(request, {
            "title": "Create User",
            "form": NewUserForm(),
            "formAction": "/accounts/create"
        }))
    elif request.POST:
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            u = authenticate(
                username=request.POST["username"],
                password=request.POST["password1"]
            )
            login(request, u)
            return HttpResponseRedirect("/")
        else:
            return render_to_response("create_user.html", RequestContext(request, {
                "title": "Create User",
                "form": form,
                "formAction": "/accounts/create"
            }))
    return HttpResponseNotAllowed(['POST', 'GET'])
