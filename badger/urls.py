from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'badger.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/projects/'}),

    url(r'^userprofile/(\d+)/', 'accounts.views.user'),

    url(r'^projects/$', 'projects.views.projects'),
    url(r'^create_project/$', 'projects.views.create_project'),
    url(r'^project/(\d+)/$', 'projects.views.project'),
    url(r'^create_release/$', 'projects.views.create_release'),
    url(r'^release/(\d+)/$', 'projects.views.release'),
    url(r'^accept_release/(\d+)/$', 'projects.views.accept_release'),
    url(r'^reject_release/(\d+)/$', 'projects.views.reject_release'),
    url(r'^team/(\d+)/$', 'projects.views.team'),
)
