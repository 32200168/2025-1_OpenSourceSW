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

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from playlist.models import Playlist, Hashtag, PlaylistSong, PlaylistTaste
from music.models import Artist, Song
from users.models import UserHashtagScore, UserTaste
from django.views.decorators.csrf import csrf_exempt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

from playlist.models import PlaylistHashtagScore, Hashtag


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




@login_required
def recommendation_view(request):
    try:
        user_taste = UserTaste.objects.get(user=request.user)
    except UserTaste.DoesNotExist:
        return render(request, 'main/recommendation.html', {'playlist': None})

    # 사용자 해시태그 점수 가져오기
    user_scores = UserHashtagScore.objects.filter(user_taste=user_taste)
    if not user_scores.exists():
        return render(request, 'main/recommendation.html', {'playlist': None})

    all_hashtags = Hashtag.objects.all()
    hashtag_index = {tag.id: idx for idx, tag in enumerate(all_hashtags)}

    # 사용자 벡터 생성
    user_vector = np.zeros(len(all_hashtags))
    for score in user_scores:
        idx = hashtag_index[score.hashtag.id]
        user_vector[idx] = score.score

    best_score = -1
    best_playlist = None

    for playlist in Playlist.objects.exclude(owner=request.user):
        try:
            playlist_taste = PlaylistTaste.objects.get(playlist=playlist)
        except PlaylistTaste.DoesNotExist:
            continue

        pl_scores = PlaylistHashtagScore.objects.filter(playlist_taste=playlist_taste)
        if not pl_scores.exists():
            continue

        pl_vector = np.zeros(len(all_hashtags))
        for score in pl_scores:
            idx = hashtag_index[score.hashtag.id]
            pl_vector[idx] = score.score

        # 코사인 유사도 계산
        sim = cosine_similarity([user_vector], [pl_vector])[0][0]

        print(f"\n=== {playlist.title} ===")
        print("user_vector:", user_vector)
        print("pl_vector:  ", pl_vector)
        print("유사도:     ", cosine_similarity([user_vector], [pl_vector])[0][0])

        if sim > best_score:
            best_score = sim
            best_playlist = playlist

        if best_playlist:
            return redirect('playlist_detail', playlist_id=best_playlist.id)
        else:
            return render(request, 'main/recommendation.html', {
                'playlist': None
            })


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

        if not title:
            count = Playlist.objects.count() + 1
            title = f"Playlist#{count}"

        try:
            song_data = json.loads(song_data_json)
        except json.JSONDecodeError:
            return render(request, 'main/main.html', {
                'error': '곡 정보가 잘못되었습니다.'
            })

        playlist = Playlist.objects.create(owner=request.user, title=title)

        for order, song_obj in enumerate(song_data):
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

        # === [유저 취향 점수 저장] ===
        user_taste, _ = UserTaste.objects.get_or_create(user=request.user)

        for tag_name in hashtag_list:
            tag, _ = Hashtag.objects.get_or_create(name=tag_name)

            # 사용자 점수 저장 (가중치 누적)
            score_obj, created = UserHashtagScore.objects.get_or_create(
                user_taste=user_taste,
                hashtag=tag
            )
            if not created:
                score_obj.score += 1
            score_obj.save()

            # 플레이리스트 점수 저장 (무조건 score = 1 고정)
            playlist_taste, _ = PlaylistTaste.objects.get_or_create(playlist=playlist)
            PlaylistHashtagScore.objects.update_or_create(
                playlist_taste=playlist_taste,
                hashtag=tag,
                defaults={'score': 1}  # 항상 1로 설정
            )

            # 태그 연결
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


@login_required
def delete_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)

    if playlist.owner != request.user:
        raise Http404("삭제 권한이 없습니다.")

    # === 해시태그 점수 감소 ===
    hashtag_list = playlist.hashtags.all()

    try:
        user_taste = UserTaste.objects.get(user=request.user)
    except UserTaste.DoesNotExist:
        user_taste = None

    for tag in hashtag_list:
        # 유저 점수 줄이기
        if user_taste:
            try:
                user_score = UserHashtagScore.objects.get(user_taste=user_taste, hashtag=tag)
                user_score.score -= 1
                if user_score.score <= 0:
                    user_score.delete()
                else:
                    user_score.save()
            except UserHashtagScore.DoesNotExist:
                pass

        # 플레이리스트 점수 삭제
        PlaylistHashtagScore.objects.filter(playlist=playlist, hashtag=tag).delete()

    # === 플레이리스트 삭제 ===
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

def save_playlist_hashtag_scores(playlist, hashtag_names):
    for tag_name in hashtag_names:
        tag, _ = Hashtag.objects.get_or_create(name=tag_name)
        score_obj, created = PlaylistHashtagScore.objects.get_or_create(
            playlist=playlist,
            hashtag=tag
        )
        if not created:
            score_obj.score += 1
        score_obj.save()