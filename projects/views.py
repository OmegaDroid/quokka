from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render_to_response

# Create your views here.
from django.template import RequestContext
from django.utils.timezone import now
from accounts import emails
from projects.models import ProjectForm, Project, ReleaseForm, Release, Response, AcceptResponseForm, RejectResponseForm


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

    return  HttpResponseNotAllowed(["POST"])


@login_required
def release(request, id):
    r = Release.objects.get(id=id)
    return render_to_response("release.html", {
        "title": r.project.name+", "+r.number,
        "release": r,
    })

@login_required
def respond(request, id):
    r = Response.objects.get(id=id)
    # if response.user is not request.user:
    #     return render_to_response("bad_login.html")
    return render_to_response('respond.html', RequestContext(request, {
        "title": "Response for "+r.release.project.name+" release v"+r.release.number,
        "response": r,
        "acceptForm": AcceptResponseForm(instance=r),
        "rejectForm": RejectResponseForm(instance=r)
    }))