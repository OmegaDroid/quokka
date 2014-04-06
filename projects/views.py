from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render_to_response

# Create your views here.
from django.template import RequestContext, Context
from django.utils.timezone import now
from taggit.models import Tag
from accounts import emails
from projects.models import ProjectForm, Project, ReleaseForm, Release, Response, AcceptResponseForm, RejectResponseForm, \
    ResponseCodes, Team, TeamForm
from utils.templatetags.utils import object_link


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
            return HttpResponseRedirect(object_link(elem))
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
        "formAction": "/create_release/",
        "isTeam": request.user in p.team.members.all(),
        "isAuth": request.user in p.authorisers.all()
    }))

@login_required
def create_release(request):
    if request.POST:
        form = ReleaseForm(request.POST)
        if form.is_valid():
            release = form.save()
            return HttpResponseRedirect(object_link(release))
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
            return HttpResponseRedirect(object_link(response.release))
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


@login_required
def team(request, id):
    t = Team.objects.get(id=id)
    return render_to_response("team.html", RequestContext(request,{
        "title": t.name,
        "team": t,
        "formAction": "/edit_team/"+str(id)+"/",
        "form": TeamForm(instance=t),
        "isTeam": request.user in t.members.all()
    }))


@login_required
def teams(request):
    return render_to_response('teams.html', RequestContext(request,{
        "title": "Teams",
        "teams": Team.objects.all(),
        "form": TeamForm(initial={"leader": request.user}),
        "formAction": "/create_team/"
    }))

def create_team(request):
    if request.POST:
        form = TeamForm(request.POST)
        if form.is_valid():
            elem = form.save()
            return HttpResponseRedirect(object_link(elem))
        else:
            return HttpResponseBadRequest()

    return  HttpResponseNotAllowed(['POST'])

def edit_team(request, id):
    if request.POST:
        t = Team.objects.get(id=id)
        form = TeamForm(request.POST, instance=t)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(object_link(t))
        else:
            return HttpResponseBadRequest()

    return  HttpResponseNotAllowed(['POST'])


def tag(request, id):
    t = Tag.objects.get(id=id)
    title = t.slug
    releases = []
    for p in Project.objects.all():
        release = p.release_with_tag(t)
        if release:
            releases.append({"project": p, "release": release})

    return render_to_response("tag.html", {
        "title": title,
        "releases": releases
    })