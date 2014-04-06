from django.contrib import admin

# Register your models here.
from projects.models import Project, Team, Release, Response

admin.site.register(Project)
admin.site.register(Team)
admin.site.register(Release)
admin.site.register(Response)