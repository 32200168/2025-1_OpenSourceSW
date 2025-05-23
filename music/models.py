from django.db import models

# music/models.py

from django.db import models

#장르: 장르명
class Genre(models.Model): 
    name = models.CharField(max_length=50)

#가수: 가수명, 소개
class Artist(models.Model):
    name = models.CharField(max_length=100)
    detail = models.TextField(blank=True)

#앨범: 앨범명, 발매일, 가수
class Album(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title} ({self.artist.name})"

#곡: 곡명, 재생시간, 가수, 앨범, 장르, 발매일
class Song(models.Model):
    title = models.CharField(max_length=100)
    duration = models.DurationField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
