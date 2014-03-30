from django.db import models
from django.forms import ModelForm
from parsley.decorators import parsleyfy

from accounts.models import UserProfile


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    leader = models.ForeignKey(UserProfile, related_name='+')
    name = models.CharField(max_length=20, unique=True)
    members = models.ManyToManyField(UserProfile)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    team = models.ForeignKey(Team, null=True, blank=True)
    authorisers = models.ManyToManyField(UserProfile)
    subscribers = models.ManyToManyField(UserProfile, related_name='+')
    img = models.ImageField(null=True, blank=True)

    @property
    def latest(self):
        tagged = []
        if self.releases:
            tagged.append({"tag": None, "release": self.releases[0]})
        for tag in Tag.objects.all().order_by("name"):
            forTag = Release.objects.filter(project=self, tag=tag).order_by("-dateTime")
            if forTag:
                tagged.append({"tag": tag, "release": forTag[0]})

        return tagged
    @property
    def releases(self):
        return Release.objects.filter(project=self).order_by("-dateTime")

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
    tag = models.ManyToManyField(Tag, null=True, blank=True)

    def __str__(self):
        return self.number

@parsleyfy
class ReleaseForm(ModelForm):
    class Meta:
        model = Release
        exclude = ['dateTime']

class Response(models.Model):
    response = models.IntegerField(choices=(
        (0, "Pending"),
        (1, "Accept"),
        (2, "Reject"),
    ), default=0)

    release = models.ForeignKey(Release)
    reason = models.TextField(null=True)
    user = models.ForeignKey(UserProfile)