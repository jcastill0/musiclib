from django.http import HttpResponse
from musiclib.models import Song, Playlist
from django.template import Context, loader
from django.http import Http404

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


def playlistDetail(request, playlist_id):
    try:
	playlist = Playlist.objects.get(pk=playlist_id)
    except Playlist.DoesNotExist:
	raise Http404
    songs = playlist.songs.all()
    if {playlist.lastPlayedIX}:
	songIX = playlist.lastPlayedIX
    elif (songs.count() > 0):
	songIX = 1
    tmplt = loader.get_template('musiclib/playlist/playlist.html')
    ctx = Context ({
	'playlist': playlist,
	'songs': songs,
	'songIX': songIX,
	})
    return HttpResponse(tmplt.render(ctx))


def playlistAdd(request):
    tmplt = loader.get_template('musiclib/playlist/addPlaylist.html')
    ctx = Context ({ })
    return HttpResponse(tmplt.render(ctx))


def playlistEdit(request, playlist_id):
    try:
	playlist = Playlist.objects.get(pk=playlist_id)
    except Playlist.DoesNotExist:
	raise Http404
    songs = playlist.songs.all()
    tmplt = loader.get_template('musiclib/playlist/editPlaylist.html')
    ctx = Context ({
	'playlist': playlist,
	'songs': songs,
	})
    return HttpResponse(tmplt.render(ctx))


def playlistDelete(request, playlist_id):
    return HttpResponse("Delete")
