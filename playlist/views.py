from django.shortcuts import render, redirect
from users.models import Playlist, PlaylistSong
from music.models import Song
from django.contrib.auth.decorators import login_required

@login_required
def playlist_view(request):
    if request.method == "POST":
        title = request.POST.get("playlistName")
        song_ids = request.POST.getlist("song_ids")

        # 플레이리스트 생성
        playlist = Playlist.objects.create(
            title=title,
            owner=request.user
        )

        # 곡들 연결
        for order, song_id in enumerate(song_ids):
            try:
                song = Song.objects.get(id=song_id)
                PlaylistSong.objects.create(
                    playlist=playlist,
                    song=song,
                    order=order
                )
            except Song.DoesNotExist:
                continue

        return redirect("main")

    return render(request, "users/playlist.html")
