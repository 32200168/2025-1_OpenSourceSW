from django.contrib import admin
from .models import Playlist, Like, PlaylistTaste, PlaylistHashtagScore

admin.site.register(PlaylistTaste)
admin.site.register(PlaylistHashtagScore)
admin.site.register(Like)
admin.site.register(Playlist)