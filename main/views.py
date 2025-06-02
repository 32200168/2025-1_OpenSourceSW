from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseNotFound
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
import json
from users.models import Profile

from playlist.models import Playlist, Hashtag, PlaylistSong
from music.models import Artist, Song
from users.models import UserTaste
from django.views.decorators.csrf import csrf_exempt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv



@login_required
def main_view(request):
    playlist_count = Playlist.objects.filter(owner=request.user).count()
    my_playlists = Playlist.objects.filter(owner=request.user)

    # 유저 취향 가져오기
    try:
        user_taste = UserTaste.objects.get(user=request.user)
        hashtags = user_taste.hashtags.all()
    except UserTaste.DoesNotExist:
        hashtags = []

    return render(request, 'main/main.html', {
        'tab': request.GET.get('tab', 'home'),
        'playlists': [],
        'query': '', 
        'playlist_count': playlist_count,
        'my_playlists': my_playlists,
        'hashtags': hashtags,  # ✅ 추가
}
)



def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)

    # PlaylistSong을 order 순서대로 가져오기
    songs = PlaylistSong.objects.filter(playlist=playlist).select_related('song').order_by('order')

    hashtags = playlist.hashtags.all()

    return render(request, 'main/playlist_detail.html', {
        'playlist': playlist,
        'songs': songs,
        'hashtags': hashtags
    })


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



def recommendation_view(request):
    dummy_playlist = {
        'title': '감성적인 밤에 듣는 플레이리스트',
        'creator': 'test_user',
        'hashtags': ['잔잔한', '감성', '밤'],
        'songs': [
            {'title': '밤편지', 'artist': '아이유', 'album_art_url': ''},
            {'title': '너를 그린다', 'artist': '정키', 'album_art_url': ''},
            {'title': '이 밤', 'artist': '양다일', 'album_art_url': ''},
        ]
    }
    return render(request, 'main/recommendation.html', {'playlist': dummy_playlist})


def hashtag_search_view(request):
    selected_tags = request.GET.getlist('hashtags')
    tags = Hashtag.objects.all().distinct()
    if selected_tags:
        results = Playlist.objects.all()
        for tag in selected_tags:
            results = results.filter(hashtags__name=tag)
    else:
        results = None
    return render(request, 'main/main.html', {
        'tags': tags,
        'selected_tags': selected_tags,
        'results': results,
    })

def hashtag_search_ajax(request):
    selected_tags = request.GET.getlist('hashtags')
    results = []
    if selected_tags:
        playlists = Playlist.objects.all()
        for tag in selected_tags:
            playlists = playlists.filter(hashtags__name=tag)
        for playlist in playlists:
            results.append({
                'id': playlist.id,
                'title': playlist.title,
                'owner': playlist.owner.username,
                'hashtags': [tag.name for tag in playlist.hashtags.all()],
            })
    return JsonResponse({'results': results})


@login_required
def create_playlist(request):
    if request.method == 'POST':
        title = request.POST.get("playlistName")
        song_data_json = request.POST.get("playlistData")
        hashtag_list = request.POST.getlist("hashtags")

        if not title or not song_data_json:
            return render(request, 'main/main.html', {
                'error': '제목과 곡을 입력하세요.'
            })

        try:
            song_data = json.loads(song_data_json)
        except json.JSONDecodeError:
            return render(request, 'main/main.html', {
                'error': '곡 정보가 잘못되었습니다.'
            })

        playlist = Playlist.objects.create(owner=request.user, title=title)

        for order, song_obj in enumerate(song_data):
            # 아티스트 처리
            artist_name = song_obj['artist']
            artist, _ = Artist.objects.get_or_create(name=artist_name, defaults={'detail': ''})

            song, _ = Song.objects.get_or_create(
                id=song_obj['id'],
                defaults={
                    'title': song_obj['title'],
                    'artist': artist,
                    'image': song_obj.get('image', ''),
                    'url': song_obj.get('url', ''),
                    'embed': song_obj.get('embed', ''),
                }
            )
            PlaylistSong.objects.create(playlist=playlist, song=song, order=order)

        for tag_name in hashtag_list:
            tag, _ = Hashtag.objects.get_or_create(name=tag_name)
            playlist.hashtags.add(tag)

        return redirect('main')

    return render(request, 'main/main.html')



load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET')
))
# Spotify 검색 API
@csrf_exempt
def spotify_search(request):
    query = request.GET.get("q", "")
    if not query:
        return JsonResponse({"results": []})

    results = sp.search(q=query, type='track', limit=10)
    tracks = []
    for item in results['tracks']['items']:
        tracks.append({
            'title': item['name'],
            'artist': item['artists'][0]['name'],
            'image': item['album']['images'][0]['url'],
            'url': item['external_urls']['spotify'],
            'id': item['id'],
            'embed': f"https://open.spotify.com/embed/track/{item['id']}"
        })
    return JsonResponse({'results': tracks})

def delete_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)

    if playlist.owner != request.user:
        raise Http404("삭제 권한이 없습니다.")

    playlist.delete()
    return redirect('main')

@login_required
def user_profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=profile_user)  # Profile 인스턴스 가져오기

    playlists = Playlist.objects.filter(owner=profile_user)
    playlist_count = playlists.count()

    follower_count = profile.followers.count()
    following_count = profile.following.count()

    return render(request, 'main/profile_page.html', {
        'profile_user': profile_user,
        'is_own_profile': request.user == profile_user,
        'playlists': playlists,
        'playlist_count': playlist_count,
        'follower_count': follower_count,
        'following_count': following_count,
    })