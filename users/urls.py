from django.urls import path
from . import views
from .views import playlist_view, save_user_taste

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("taste/", views.taste_view, name="taste"),
    path("select-taste/", save_user_taste, name="select_taste"),
    path("playlist/", playlist_view, name="playlist"),
    path("api/search/", views.spotify_search, name="spotify_search"),  # Spotify API 연동
]
