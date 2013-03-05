from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from musiclib.models import Song, Playlist, Artist
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
    latest_songs_list = Song.objects.all().order_by('created', 'name')[:5]
    return render_to_response('musiclib/index.html', {
        'latest_songs_list': latest_songs_list,
        }, RequestContext(request))


def profile(request):
    if not request.user.is_authenticated():
	return (index(request))
    return render_to_response('musiclib/profile/index.html', {
	'user': request.user,
	}, RequestContext(request))


def artistIndex(request):
    if not request.user.is_authenticated():
	return (index(request))
    artists = Artist.objects.all().order_by('name')
    return render_to_response('musiclib/artist/index.html', {
	'artists': artists,
	'user': request.user,
	}, RequestContext(request))


def profileSave(request):
    loginName = request.POST['loginName']
    email = request.POST['email']
    firstName = request.POST['firstName']
    lastName = request.POST['lastName']
    user = User.objects.get(pk=request.user.id)
    if (loginName):
	user.username = loginName
    if (email):
	user.email = email
    if (firstName):
	user.first_name = firstName
    if (lastName):
	user.last_name = lastName
    user.save()
    return (profile(request))


def playlistIndex(request):
    if not request.user.is_authenticated():
	return (index(request))
    playlists = Playlist.objects.all().filter(owner=request.user).order_by('-name')
    return render_to_response('musiclib/playlist/index.html', {
        'playlists': playlists,
	'user': request.user,
        }, RequestContext(request))


def playlistAdd(request):
    if not request.user.is_authenticated():
	return (index(request))
    ctx = RequestContext(request)
    return render_to_response('musiclib/playlist/addPlaylist.html', ctx)


def playlistSave(request):
    buttonType = request.POST['plButton']
    playListName = request.POST['playlistName']
    user = request.user
    playList = Playlist(name=playListName, owner=user)
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
	'user': request.user,
	}, RequestContext(request))


def playlistSaveSongs(request):
    playlist_id = request.POST['playlistID']
    try:
	playlist = Playlist.objects.get(pk=playlist_id)
    except Playlist.DoesNotExist:
	raise Http404
    songIDs = request.POST.getlist('playListSongs')
    logger.debug('newSongs=%r' % songIDs)
    for songID in songIDs:
	song = Song.objects.get(pk=songID)
	playlist.songs.add(song)
    playlist.lastPlayedIX = 0
    return (playlistIndex(request))


def playlistDelete(request, playlist_id):
    if not request.user.is_authenticated():
	return (index(request))
    try:
        playList = Playlist.objects.get(pk=playlist_id)
    except Playlist.DoesNotExist:
        raise Http404
    playList.delete()
    return (playlistIndex(request))


def playlistPlay(request, playlist_id):
    if not request.user.is_authenticated():
	return (index(request))
    try:
        playlist = Playlist.objects.get(pk=playlist_id)
    except Playlist.DoesNotExist:
        raise Http404
    songs = playlist.songs.all()
    return render_to_response('musiclib/playlist/playlist.html', {
        'playlist': playlist,
        'songs': songs,
	'songCnt': playlist.songs.count(),
	'user': request.user,
        }, RequestContext(request))


def songsByArtist(request, artist_id):
    if not request.user.is_authenticated():
	return (index(request))
    try:
	art = Artist.objects.get(pk=artist_id)
    except Artist.DoesNotExist:
	raise Http404
    try:
	songs = list(Song.objects.filter(artist=art).order_by('name'))
    except Song.DoesNotExist:
	raise Http404
    playlists = Playlist.objects.all().filter(owner=request.user).order_by('name')
    return render_to_response('musiclib/artist/songs.html', {
        'songs': songs,
        'artist': art,
	'playlists': playlists,
	'user': request.user,
        }, RequestContext(request))

