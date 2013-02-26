from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

MEDIA_TYPES = ( ('MP3', 'MP3'), ('MP4', 'MP4'))

class Artist(models.Model):
    name = models.CharField(max_length=128)
    def __unicode__(self):
	return self.name

class Video(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    video = models.URLField()
    embedCode = models.TextField(max_length=512, null=True, blank=True)
    #viewedCnt = models.IntegerField(null=True, blank=True)
    def __unicode__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=256, error_messages = {'required': 'Please enter the Song Title'})
    type = models.CharField(max_length=4, choices=MEDIA_TYPES, help_text='Pick a format type if you know it', null=True, blank=True)
    created = models.DateTimeField(default=datetime.now)
    file = models.FileField(upload_to='media')
    video = models.ForeignKey(Video, null=True, blank=True)
    artist = models.ForeignKey(Artist)
    #playedCnt = models.IntegerField(null=True, blank=True)
    def __unicode__(self):
	return self.name

class Playlist(models.Model):
    name = models.CharField(max_length=32)
    songs = models.ManyToManyField(Song, null=True, blank=True)
    owner = models.ForeignKey(User)
    lastPlayedIX = models.IntegerField(null=True, blank=True)
    def __unicode__(self):
	return self.name


