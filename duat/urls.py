from django.conf.urls import patterns, include, url
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from django.contrib import admin

from duat.views import post,view,generate_js

admin.autodiscover()
admin.site.unregister(Site)
admin.site.unregister(Group)

urlpatterns = patterns('',
    # home page
    url(r'^$',TemplateView.as_view(template_name='home.html')),

	# generated javascript
    url(r'^project/(?P<project_name>\w+)/feedback\.js$', 
        cache_page(60*24)(generate_js), 
        name='js', 
        kwargs={'filename':'feedback.js'}),

    url(r'^js/admin\.js$', 
        cache_page(60*24)(generate_js),
        name='admin',
        kwargs={'filename':'admin.js',
                'project_name':None}),

    url(r'^project/(?P<project_name>\w+)/submit$', post, name='post'),
    
    url(r'^view/(?P<project_name>\w+)/(?P<id>\d+)/$', cache_page(60*24)(view), name='view'),

    url(r'^admin/', include(admin.site.urls)),
)
