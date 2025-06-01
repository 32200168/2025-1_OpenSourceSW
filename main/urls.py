from django.urls import path
from .views import (
    main_view,
    create_playlist,
    playlist_detail,
    recommendation_view,
    hashtag_search_view,
    playlist_from_main
)

urlpatterns = [
    path('', main_view, name='main'),
    path('playlist/', create_playlist, name='create_playlist'),
    path('playlist/<int:playlist_id>/', playlist_detail, name='playlist_detail'),
    path('recommend/', recommendation_view, name='recommendation'),
    path('search/', hashtag_search_view, name='search'),
    path('', playlist_from_main, name='main_playlist'),  # http://127.0.0.1:8000/main/
]
