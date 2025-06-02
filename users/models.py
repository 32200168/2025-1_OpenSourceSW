from django.db import models
from django.contrib.auth.models import User
from playlist.models import Hashtag, Playlist


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # 좋아요 누른 플레이리스트
    liked_playlists = models.ManyToManyField(Playlist, blank=True, related_name='liked_by')
    
    # 팔로잉 / 팔로워
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def __str__(self):
        return f"{self.user.username}의 프로필"
    
class UserTaste(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hashtags = models.ManyToManyField(Hashtag)

    def __str__(self):
        return f"{self.user.username}의 취향"
    
class UserHashtagScore(models.Model):
    user_taste = models.ForeignKey(UserTaste, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)
    score = models.IntegerField(default=1)

    class Meta:
        unique_together = ('user_taste', 'hashtag')  # 하나의 조합만 존재

    def __str__(self):
        return f"{self.user_taste.user.username} - {self.hashtag.name} ({self.score}점)"