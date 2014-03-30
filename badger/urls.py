from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'badger.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^projects/$', 'projects.views.projects'),
    url(r'^create_project/$', 'projects.views.create_project'),
    url(r'^project/(\d+)/$', 'projects.views.project'),
    url(r'^create_release/$', 'projects.views.create_release'),
    url(r'^release/(\d+)/$', 'projects.views.release'),
)
