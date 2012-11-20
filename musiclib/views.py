from django.http import HttpResponse
from musiclib.models import Song, Playlist
from django.template import Context, loader

def index(request):
    latest_songs_list = Song.objects.all().order_by('-created')[:5]
    tmplt = loader.get_template('musiclib/index.html')
    ctx = Context ({
	'latest_songs_list': latest_songs_list,
	})
    return HttpResponse(tmplt.render(ctx))

def playlistIndex(request):
    playlists = Playlist.objects.all().order_by('-name')[:5]
    tmplt = loader.get_template('musiclib/playlist/index.html')
    ctx = Context ({
        'playlists': playlists,
        })
    return HttpResponse(tmplt.render(ctx))
