from django.db import models
from django.contrib.auth.models import User

# Create your models here.

MEDIA_TYPES = ( ('MP3', 'MP3'), ('MP4', 'MP4'))

class Artist(models.Model):
    name = models.CharField(max_length=128)
    def __unicode__(self):
	return self.name

class Song(models.Model):
    name = models.CharField(max_length=256)
    type = models.CharField(max_length=4, choices=MEDIA_TYPES)
    last_mod = models.DateTimeField('last modified')
    file = models.FilePathField()
    video = models.URLField()
    artist = models.ForeignKey(Artist)
    def __unicode__(self):
	return self.name

class Playlist(models.Model):
    name = models.CharField(max_length=32)
    song = models.ManyToManyField(Song)
    owner = models.ForeignKey(User)
    def __unicode__(self):
	return self.name
