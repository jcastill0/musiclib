from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),
    url(r'^musiclib/playlist/play/(?P<playlist_id>\d+)/$', 'musiclib.views.playlistPlay'),
    url(r'^musiclib/playlist/saveSongs/$', 'musiclib.views.playlistSaveSongs'),
    url(r'^musiclib/playlist/save/$', 'musiclib.views.playlistSave'),
    url(r'^musiclib/playlist/delete/(?P<playlist_id>\d+)/$', 'musiclib.views.playlistDelete'),
    url(r'^musiclib/playlist/edit/(?P<playlist_id>\d+)/$', 'musiclib.views.playlistEdit'),
    url(r'^musiclib/playlist/add/$', 'musiclib.views.playlistAdd'),
    url(r'^musiclib/playlist/$', 'musiclib.views.playlistIndex'),
    url(r'^musiclib/artist/$', 'musiclib.views.artistIndex'),
    url(r'^musiclib/artist/songs/(?P<artist_id>\d+)$', 'musiclib.views.songsByArtist'),
    url(r'^musiclib/$', 'musiclib.views.index'),
    url(r'^musiclib/login/$', 'musiclib.views.login_view'),
    url(r'^musiclib/logout/$', 'musiclib.views.logout_view'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
