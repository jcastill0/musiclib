from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from musiclib.models import Song, Playlist
from django.template import Context, loader, RequestContext
from django.http import Http404
import logging

logger = logging.getLogger(__name__)


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
	    return (playlistIndex(request))
        else:
            logger.debug('User not active =%r' % user)
	    return (index(request))
    else:
	logger.debug('User not found =%r' % user)
	return (index(request))


def logout_view(request):
    logout(request)
    return (index(request))


def index(request):
    ctx = RequestContext(request);
    latest_songs_list = Song.objects.all().order_by('-created')[:5]
    return render_to_response('musiclib/index.html', {
        'latest_songs_list': latest_songs_list,
        }, RequestContext(request))


def playlistIndex(request):
    playlists = Playlist.objects.all().order_by('-name')[:5]
    return render_to_response('musiclib/playlist/index.html', {
        'playlists': playlists,
        }, RequestContext(request))


def playlistAdd(request):
    ctx = RequestContext(request)
    return render_to_response('musiclib/playlist/addPlaylist.html', ctx)


def playlistSave(request):
    buttonType = request.POST['plButton']
    playListName = request.POST['playlistName']
    user = request.user
    logger.debug('User=%r' % user)
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
    playListMap = {}
    for song in playListSongs:
	playListMap[song.id] = True
    allSongsList = list(allSongs)
    for song in allSongsList:
	found = playListMap.get(song.id)
	if (found):
	    allSongsList.remove(song)
    return render_to_response('musiclib/playlist/editPlaylist.html', {
        'playlist': playlist,
        'playListSongs': playListSongs,
        'allSongs': allSongsList,
	}, RequestContext(request))


def playlistSaveSongs(request):
    playlist_id = request.POST['playlistID']
    try:
	playlist = Playlist.objects.get(pk=playlist_id)
    except Playlist.DoesNotExist:
	raise Http404
    newSongs = request.POST.getlist('playListSongs')
    playlist.songs.clear()
    for song in newSongs:
	playlist.songs.add(song)
    playlist.lastPlayedIX = 0
    playlist.save(force_update=True)
    return (playlistIndex(request))


def playlistDelete(request, playlist_id):
    try:
        playList = Playlist.objects.get(pk=playlist_id)
    except Playlist.DoesNotExist:
        raise Http404
    playList.delete()
    return (playlistIndex(request))


def playlistPlay(request, playlist_id):
    try:
        playlist = Playlist.objects.get(pk=playlist_id)
    except Playlist.DoesNotExist:
        raise Http404
    songs = playlist.songs.all()
    if (songs):
	oneSong = songs[0]
    return render_to_response('musiclib/playlist/playlist.html', {
        'playlist': playlist,
        'songs': songs,
        'fixedSong': oneSong,
        }, RequestContext(request))

