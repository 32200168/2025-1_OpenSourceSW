from django.db import models
from django.contrib.auth.models import User
from music.models import Song


class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    users = models.ManyToManyField(User, related_name='hashtag_set')

    def __str__(self):
        return f"{self.name}"
    
class Playlist(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    hashtags = models.ManyToManyField(Hashtag,related_name = "playlists", blank=True)
    songs = models.ManyToManyField(Song, through='PlaylistSong', related_name='playlists')

    def __str__(self):
        return f"{self.title}"

class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.playlist.title}의 곡"
    
    class Meta:
        ordering = ['order']

    class Meta:
        unique_together = ('playlist', 'song')


class Like(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('playlist', 'user')

class PlaylistHashtagScore(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)
    score = models.IntegerField(default=1)