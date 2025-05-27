from django.contrib import admin
from .models import Playlist, PlaylistSong, Comment, Like, PlayHistory

admin.site.register(Playlist)
admin.site.register(PlaylistSong)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(PlayHistory)