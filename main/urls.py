from django.urls import path
from .views import create_playlist, hashtag_search_view, playlist_detail,liked_playlists_view, profile_view
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('recommend/', views.recommendation_view, name='recommendation'),
    path('search/', views.hashtag_search_view, name='search'),
    path('playlist/', create_playlist, name='create_playlist'),
    path('playlist/<int:playlist_id>/', playlist_detail, name='playlist_detail'),
    path("api/search/", views.spotify_search, name="spotify_search"),
    path('api/search_hashtag/', views.hashtag_search_ajax, name='hashtag_search_ajax'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('playlist/<int:playlist_id>/delete/', views.delete_playlist, name='delete_playlist'),
    path('profile/<str:username>/', views.user_profile_view, name='user_profile'),
    path('playlist/<int:playlist_id>/like/', views.toggle_like, name='toggle_like'),
    path('liked/', liked_playlists_view, name='liked_playlists'),
    path('profile/', profile_view, name='profile_view'),
    


]

