from django.db import models
from django.forms import ModelForm
from parsley.decorators import parsleyfy
from taggit.managers import TaggableManager
from taggit.models import Tag

from accounts.models import User

class Team(models.Model):
    leader = models.ForeignKey(User, related_name='+')
    name = models.CharField(max_length=20, unique=True)
    members = models.ManyToManyField(User)
    description = models.TextField(blank=True, null=True)
    img = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def projects(self):
        return Project.objects.filter(team=self)


class TeamForm(ModelForm):
    class Meta:
        model = Team
        exclude = []


class Project(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    team = models.ForeignKey(Team, null=True, blank=True)
    authorisers = models.ManyToManyField(User)
    subscribers = models.ManyToManyField(User, related_name='+')
    img = models.ImageField(null=True, blank=True)

    @property
    def tags(self):
        projectTags = []
        for ts in Release.objects.values_list("tags").filter(project=self):
            for t in ts:
                if t not in projectTags:
                    projectTags.append(t)

        return projectTags

    @property
    def latest(self):
        tagged = []
        if self.accepted_releases:
            tagged.append({"tag": None, "release": self.accepted_releases[0]})
        for tag in Tag.objects.all():

            forTag = [r for r in Release.objects.filter(project=self, tags__slug=tag).order_by("-dateTime") if r.accepted]
            if forTag:
                tagged.append({"tag": tag, "release": forTag[0]})

        return tagged

    @property
    def releases(self):
        return Release.objects.filter(project=self).order_by("-dateTime")

    @property
    def accepted_releases(self):
        return [r for r in Release.objects.filter(project=self).order_by("-dateTime") if r.accepted]

    def __str__(self):
        return self.name


@parsleyfy
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = []


class Release(models.Model):
    number = models.CharField(max_length=20, unique=True)
    project = models.ForeignKey(Project)
    notes = models.TextField()
    dateTime = models.DateTimeField()
    url = models.URLField()
    tags = TaggableManager()

    def __str__(self):
        return self.number

    def create_responses(self):
        for auth in self.project.authorisers.all():
            Response(release=self, user=auth).save()

    def active_user_response_object(self, user):
        responses = Response.objects.filter(release=self, response=ResponseCodes.Pending)
        if responses:
            return responses.get(user=user)
        return None

    @property
    def responses(self):
        return Response.objects.filter(release=self)

    @property
    def pending_responses(self):
        return Response.objects.filter(release=self, response=ResponseCodes.Pending)

    @property
    def accepted_responses(self):
        return Response.objects.filter(release=self, response=ResponseCodes.Accept)

    @property
    def rejected_responses(self):
        return Response.objects.filter(release=self, response=ResponseCodes.Reject)

    @property
    def pending(self):
        return self.pending_responses and not self.rejected

    @property
    def accepted(self):
        return len(self.accepted_responses) == len(self.responses)

    @property
    def rejected(self):
        return len(self.rejected_responses) > 0

    @property
    def since_last_accepted(self):
        releases = [self]
        for release in Release.objects.filter(id__lt=self.id).order_by("-id"):
            if release.accepted:
                return releases
            else:
                releases.append(release)


@parsleyfy
class ReleaseForm(ModelForm):
    class Meta:
        model = Release
        exclude = ['dateTime']


class ResponseCodes():
    Pending = 0
    Accept = 1
    Reject = 2


class Response(models.Model):
    response = models.IntegerField(choices=(
        (ResponseCodes.Pending, "Pending"),
        (ResponseCodes.Accept, "Accept"),
        (ResponseCodes.Reject, "Reject"),
    ), default=ResponseCodes.Pending)

    release = models.ForeignKey(Release)
    reason = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User)

    class Meta:
        unique_together = (("release", "user"),)


@parsleyfy
class AcceptResponseForm(ModelForm):
    message = "Accept the release?"

    class Meta:
        model = Response
        exclude = ['reason', 'response', 'release', 'user']


@parsleyfy
class RejectResponseForm(ModelForm):
    class Meta:
        model = Response
        exclude = ['response', 'release', 'user']

        parsley_extras = {
            "reason": {
                "required": True
            }
        }