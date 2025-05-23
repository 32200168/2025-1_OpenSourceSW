from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseNotFound
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
import json


@login_required
def main_view(request):
    return render(request, 'main/main.html', {
        'tab': request.GET.get('tab', 'feed')  # 기본값은 feed 탭
    })

def profile_edit(request):
    return render(request, 'main/profile_edit.html')

def playlist_detail(request, playlist_id):
    mock_playlists = {
        1: {
            'title': 'My Playlist 1',
            'creator': '내 아이디',
            'songs': [
                { 'title': '노래 A', 'artist': '아티스트 A', 'album_art_url': 'https://cdn.startupful.io/img/app_logo/no_img.png' },
                { 'title': '노래 B', 'artist': '아티스트 B', 'album_art_url': 'https://cdn.startupful.io/img/app_logo/no_img.png' }
            ]
        },
        2: {
            'title': 'My Playlist 2',
            'creator': '내 아이디',
            'songs': [
                { 'title': '노래 C', 'artist': '아티스트 C', 'album_art_url': 'https://cdn.startupful.io/img/app_logo/no_img.png' },
                { 'title': '노래 D', 'artist': '아티스트 D', 'album_art_url': 'https://cdn.startupful.io/img/app_logo/no_img.png' }
            ]
        },
        3: {
            'title': 'Liked Playlist A',
            'creator': 'user_2',
            'songs': [
                { 'title': '노래 E', 'artist': '아티스트 E', 'album_art_url': 'https://cdn.startupful.io/img/app_logo/no_img.png' },
                { 'title': '노래 F', 'artist': '아티스트 F', 'album_art_url': 'https://cdn.startupful.io/img/app_logo/no_img.png' }
            ]
        },
        4: {
            'title': 'Liked Playlist B',
            'creator': 'user_3',
            'songs': [
                { 'title': '노래 G', 'artist': '아티스트 G', 'album_art_url': 'https://cdn.startupful.io/img/app_logo/no_img.png' },
                { 'title': '노래 H', 'artist': '아티스트 H', 'album_art_url': 'https://cdn.startupful.io/img/app_logo/no_img.png' }
            ]
        },
    }

    playlist = mock_playlists.get(playlist_id)
    if not playlist:
        raise Http404("플레이리스트 없음")
    return render(request, 'main/playlist_detail.html', {'playlist': playlist})


def profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    is_own_profile = (user_profile == request.user)
    return render(request, 'main/profile.html', {
        'profile_user': user_profile,
        'is_own_profile': is_own_profile
    })