from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages

from django.contrib.auth.models import User
from playlist.models import Playlist
from music.models import Song
from .models import Hashtag, UserTaste




def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("main")
        else:
            # 로그인 실패 시 오류 메시지 전달
            return render(request, "users/login.html", {
                'error': "등록된 사용자가 없거나 비밀번호가 틀렸습니다."
            })

    return render(request, "users/login.html")


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'users/signup.html', {'error': '이미 존재하는 사용자명입니다.'})

        User.objects.create_user(username=username, password=password)
        return redirect('/users/taste/')

    return render(request, 'users/signup.html')



def taste_view(request):
    if request.method == "POST":
        tags = request.POST.getlist("hashtags")
        print("선택된 태그:", tags)  # 로그 확인용
        return redirect("/users/playlist/")
    return render(request, "users/taste.html")

def playlist_view(request):
    if request.method == "POST":
        title = request.POST.get("playlistName")
        song_ids = request.POST.getlist("song_ids")
        hashtags = request.POST.getlist("hashtags")

        if not title or not song_ids:
            return render(request, "users/playlist.html", {"error": "제목 또는 곡이 비어있습니다."})

        # Playlist 생성
        playlist = Playlist.objects.create(
            title=title,
            user=request.user
        )

        print("저장된 해시태그:", hashtags)  # 해시태그 출력만 (저장 X)

        return redirect("main")  # 저장 후 메인 페이지 이동

    return render(request, "users/playlist.html")

def save_playlist(request):
    if request.method == 'POST':
        title = request.POST.get('playlistName')  # 제목
        hashtags = request.POST.getlist('hashtags')  # ['K-POP', '몽환적인']
        song_ids = request.POST.getlist('song_ids')  # ['3', '5', '8']

        # 플레이리스트 저장
        playlist = Playlist.objects.create(
            title=title,
            user=request.user
        )

        # 곡 연결
        for idx, sid in enumerate(song_ids):
            song = Song.objects.get(id=sid)
            PlaylistSong.objects.create(
                playlist=playlist,
                song=song,
                order=idx
            )

        return redirect('playlist_detail', pk=playlist.id)
    
@login_required
def save_user_taste(request):
    if request.method == 'POST':
        tag_names = request.POST.getlist('hashtags')

        user_taste, _ = UserTaste.objects.get_or_create(user=request.user)
        user_taste.hashtags.clear()  # 기존 취향 초기화

        for name in tag_names:
            tag, _ = Hashtag.objects.get_or_create(name=name)
            user_taste.hashtags.add(tag)

        return redirect('main')  # 저장 후 리디렉션

    hashtags = Hashtag.objects.all()
    return render(request, 'main/select_taste.html', {'hashtags': hashtags})

