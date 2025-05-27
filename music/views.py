from django.shortcuts import render

import playlist
from playlist.models import PlaylistSong

songs = PlaylistSong.objects.filter(playlist=playlist).select_related("song", "song__artist", "song__album", "song__genre")
