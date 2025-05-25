from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseNotFound
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
import json



@login_required
def main_view(request):
    return render(request, 'main/main.html', {
        'tab': request.GET.get('tab', 'home'),
        'playlists': [],
        'query': '', 
    })


def playlist_detail(request, playlist_id):
    playlist = mock_playlists.get(playlist_id)
    if not playlist:
        raise Http404("플레이리스트 없음")
    return render(request, 'main/playlist_detail.html', {'playlist': playlist})


mock_playlists = {
    1: {
        'title': 'My Playlist 1',
        'creator': '내 아이디',
        'hashtags': ['K-POP', '랩/힙합', '발라드'],
        'songs': [
            { 'title': '노래 A', 'artist': '아티스트 A', 'album_art_url': 'https://cdn.startupful.io/img/app_logo/no_img.png' },
            { 'title': '노래 B', 'artist': '아티스트 B', 'album_art_url': 'https://cdn.startupful.io/img/app_logo/no_img.png' }
        ]
    },
    2: {
        'title': 'My Playlist 2',
        'creator': '내 아이디',
        'hashtags': ['K-POP', '랩/힙합', '발라드'],
        'songs': [
            { 'title': '노래 C', 'artist': '아티스트 C', 'album_art_url': 'https://cdn.startupful.io/img/app_logo/no_img.png' },
            { 'title': '노래 D', 'artist': '아티스트 D', 'album_art_url': 'https://cdn.startupful.io/img/app_logo/no_img.png' }
        ]
    },
    3: {
        'title': 'Liked Playlist A',
        'creator': 'user_2',
        'hashtags': ['인디', '차분한', '잔잔한'],
        'songs': [
            { 'title': '노래 E', 'artist': '아티스트 E', 'album_art_url': 'https://cdn.startupful.io/img/app_logo/no_img.png' },
            { 'title': '노래 F', 'artist': '아티스트 F', 'album_art_url': 'https://cdn.startupful.io/img/app_logo/no_img.png' }
        ]
    },
    4: {
        'title': 'Liked Playlist B',
        'creator': 'user_3',
        'hashtags': ['랩/힙합', '발라드'],
        'songs': [
            { 'title': '노래 G', 'artist': '아티스트 G', 'album_art_url': 'https://cdn.startupful.io/img/app_logo/no_img.png' },
            { 'title': '노래 H', 'artist': '아티스트 H', 'album_art_url': 'https://cdn.startupful.io/img/app_logo/no_img.png' }
        ]
    },
}


def playlist_view(request):
    if request.method == "POST":
        songs_json = request.POST.get("songs", "[]")
        hashtags = request.POST.getlist("hashtags")

        try:
            songs = json.loads(songs_json)
        except json.JSONDecodeError:
            songs = []

        if len(songs) < 3 or len(hashtags) < 3:
            error_msg = ""
            if len(songs) < 3:
                error_msg += "노래는 최소 3곡 이상 선택해야 합니다. "
            if len(hashtags) < 3:
                error_msg += "해시태그는 최소 3개 이상 선택해야 합니다."

            return render(request, "main/main.html", {
                "tab": "add",
                "error": error_msg,
                "playlists": [],
                "query": ""
            })

        messages.success(request, "플레이리스트가 저장되었습니다.")

        return redirect("/?tab=add")

    return render(request, "main/main.html", {
        "tab": "add",
        "playlists": [],
        "query": ""
    })