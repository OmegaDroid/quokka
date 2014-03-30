from django.contrib import admin

# Register your models here.
from projects.models import Project, Team, Tag, Release, Response

admin.site.register(Project)
admin.site.register(Tag)
admin.site.register(Team)
admin.site.register(Release)
admin.site.register(Response)