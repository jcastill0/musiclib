from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from musiclib.models import Song, Playlist
from django.template import Context, loader, RequestContext
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
    # tmplt = loader.get_template('musiclib/playlist/addPlaylist.html')
    ctx = RequestContext(request)
    return render_to_response('musiclib/playlist/addPlaylist.html', ctx)


def playlistSave(request):
    buttonType = request.POST['plButton']
    playListName = request.POST['playlistName']
    playList = Playlist(name=playListName, owner=User.objects.get(pk=1))
    playList.save()
    if (buttonType == 'saveNameOnly'):
	return (playlistIndex(request))
    else:
	return (playlistEdit(request, playList.id))


def playlistEdit(request, playlist_id):
    try:
	playlist = Playlist.objects.get(pk=playlist_id)
    except Playlist.DoesNotExist:
	raise Http404
    playListSongs = playlist.songs.all()
    allSongs = Song.objects.all().order_by('-name')
    # tmplt = loader.get_template('musiclib/playlist/editPlaylist.html')
    #ctx = Context ({'playlist': playlist,'playListSongs': playListSongs,
#	'allSongs': allSongs,	})
    # return HttpResponse(tmplt.render(ctx))
    return render_to_response('musiclib/playlist/editPlaylist.html', {
        'playlist': playlist,
        'playListSongs': playListSongs,
        'allSongs': allSongs,
	}, RequestContext(request))


def playlistSaveSongs(request):
    playlist_id = request.POST['playlistID']
    try:
	playlist = Playlist.objects.get(pk=playlist_id)
    except Playlist.DoesNotExist:
	raise Http404
    return (playlistIndex(request))


def playlistDelete(request, playlist_id):
    try:
        playList = Playlist.objects.get(pk=playlist_id)
    except Playlist.DoesNotExist:
        raise Http404
    playList.delete()
    return (playlistIndex(request))
