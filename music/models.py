from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=100)
    detail = models.TextField(blank=True)

class Song(models.Model):
    # Spotify 트랙 ID (unique)
    id = models.CharField(max_length=40, primary_key=True)  # 스포티파이 트랙 id 직접 사용
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    image = models.URLField(max_length=300, blank=True, null=True)  # 앨범 아트
    url = models.URLField(max_length=300, blank=True, null=True)    # 스포티파이 곡 URL
    embed = models.URLField(max_length=300, blank=True, null=True)  # 임베드 URL
    # duration, genre, album 등 필요시 추가 가능

    def __str__(self):
        return f"{self.title} - {self.artist.name}"
