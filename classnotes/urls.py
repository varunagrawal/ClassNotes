from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'classnotes.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^connect.json', 'classnotes.views.connect_json', name='connect_json'),
    url(r'^notes/', include('notes.urls')),
)
