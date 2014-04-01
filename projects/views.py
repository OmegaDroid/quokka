from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render_to_response

# Create your views here.
from django.template import RequestContext
from django.utils.timezone import now
from accounts import emails
from projects.models import ProjectForm, Project, ReleaseForm, Release, Response, AcceptResponseForm, RejectResponseForm, \
    ResponseCodes


@login_required
def projects(request):
    return render_to_response("projects.html", RequestContext(request, {
        "title": "Projects",
        "form": ProjectForm(),
        "projects": Project.objects.all(),
        "formAction": "/create_project/"
    }))


@login_required
def create_project(request):
    if request.POST:
        form = ProjectForm(request.POST)
        if form.is_valid():
            elem = form.save()
            return HttpResponseRedirect("/project/"+str(elem.id)+"/")
        else:
            return HttpResponseBadRequest()

    return  HttpResponseNotAllowed(['POST'])


@login_required
def project(request, id):
    p = Project.objects.get(id=id)
    form = ReleaseForm(initial={'project':p})
    return render_to_response("project.html", RequestContext(request, {
        "title": p.name,
        "project": p,
        "form": form,
        "formAction": "/create_release/"
    }))


def create_response(hostname, release, auth):
    response = Response(release=release, user=auth)
    response.save()
    emails.new_release_auth(hostname, response)


def create_responses(hostname, elem):
    for auth in elem.project.authorisers.all():
        create_response(hostname, elem, auth)


@login_required
def create_release(request):
    if request.POST:
        form = ReleaseForm(request.POST)
        if form.is_valid():
            release = form.save(commit=False)
            release.dateTime = now()
            release.save()
            create_responses(request.META["HTTP_HOST"], release)
            emails.new_release_team(request.META["HTTP_HOST"], release)
            return HttpResponseRedirect("/release/"+str(release.id)+"/")
        else:
            return HttpResponseBadRequest()

    return HttpResponseNotAllowed(["POST"])


@login_required
def release(request, id):
    r = Release.objects.get(id=id)
    userResponse = r.active_user_response_object(request.user)
    return render_to_response("release.html",  RequestContext(request, {
        "title": r.project.name+", "+r.number,
        "release": r,
        "userResponse": userResponse,
        "acceptForm": AcceptResponseForm(instance=userResponse),
        "rejectForm": RejectResponseForm(instance=userResponse)
    }))


def accept_release(request, id):
    if request.POST:
        response = Release.objects.get(id=id).active_user_response_object(request.user)

        form = AcceptResponseForm(request.POST, instance=response)
        if form.is_valid():
            response = form.save(commit=False)
            response.response = ResponseCodes.Accept
            response.save()
            return HttpResponseRedirect("/release/"+str(response.release.id)+"/")
        else:
            return HttpResponseBadRequest()

    return HttpResponseNotAllowed(["POST"])


def reject_release(request, id):
    if request.POST:
        response = Release.objects.get(id=id).active_user_response_object(request.user)

        form = RejectResponseForm(request.POST, instance=response)
        if form.is_valid():
            response = form.save(commit=False)
            response.response = ResponseCodes.Reject
            response.save()
            return HttpResponseRedirect("/release/"+str(response.release.id)+"/")
        else:
            return HttpResponseBadRequest()

    return HttpResponseNotAllowed(["POST"])


def team(request, p1):
    return render_to_response("team.html")