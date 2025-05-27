from django.db import models
from .models import User
from music.models import Song

class Playlist(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

class Comment(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('playlist', 'user')

class PlayHistory(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey('music.Song', on_delete=models.CASCADE)
    played_at = models.DateTimeField(auto_now_add=True)