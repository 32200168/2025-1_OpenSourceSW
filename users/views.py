from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User

from playlist.models import Playlist
from music.models import Song
from .models import Hashtag, UserTaste
from playlist.models import PlaylistSong  # 필요 시 추가

from django.views.decorators.csrf import csrf_exempt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API 인증 정보
client_id = 'ea1b7382a37d4a0abaa168c46cb9b2bb'
client_secret = 'e66c7a40d63c4e26bed390a6e48f16ce'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))


# 로그인
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("main")
        else:
            messages.error(request, "등록된 사용자가 없거나 비밀번호가 틀렸습니다.")

    return render(request, "users/login.html")


# 회원가입
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'users/signup.html', {'error': '이미 존재하는 사용자명입니다.'})

        User.objects.create_user(username=username, password=password)
        return redirect('/users/taste/')

    return render(request, 'users/signup.html')


# 취향 선택
def taste_view(request):
    if request.method == "POST":
        tags = request.POST.getlist("hashtags")
        print("선택된 태그:", tags)
        return redirect("/users/playlist/")
    return render(request, "users/taste.html")


# 취향 저장
@login_required
def save_user_taste(request):
    if request.method == 'POST':
        tag_names = request.POST.getlist('hashtags')

        user_taste, _ = UserTaste.objects.get_or_create(user=request.user)
        user_taste.hashtags.clear()

        for name in tag_names:
            tag, _ = Hashtag.objects.get_or_create(name=name)
            user_taste.hashtags.add(tag)

        return redirect('main')

    hashtags = Hashtag.objects.all()
    return render(request, 'main/select_taste.html', {'hashtags': hashtags})


# 플레이리스트 작성
def playlist_view(request):
    if request.method == "POST":
        title = request.POST.get("playlistName")
        song_ids = request.POST.getlist("song_ids")
        hashtags = request.POST.getlist("hashtags")

        if not title or not song_ids:
            return render(request, "users/playlist.html", {"error": "제목 또는 곡이 비어있습니다."})

        playlist = Playlist.objects.create(
            title=title,
            user=request.user
        )

        print("저장된 해시태그:", hashtags)

        return redirect("main")

    return render(request, "users/playlist.html")


# 플레이리스트 + 곡 저장
def save_playlist(request):
    if request.method == 'POST':
        title = request.POST.get('playlistName')
        hashtags = request.POST.getlist('hashtags')
        song_ids = request.POST.getlist('song_ids')

        playlist = Playlist.objects.create(
            title=title,
            user=request.user
        )

        for idx, sid in enumerate(song_ids):
            song = Song.objects.get(id=sid)
            PlaylistSong.objects.create(
                playlist=playlist,
                song=song,
                order=idx
            )

        return redirect('playlist_detail', pk=playlist.id)


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
