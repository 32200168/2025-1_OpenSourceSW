from django.urls import path
from .views import create_playlist, playlist_detail
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('recommend/', views.recommendation_view, name='recommendation'),
    path('search/', views.hashtag_view, name='search'),
    path('playlist/', create_playlist, name='create_playlist'),
    path('playlist/<int:playlist_id>/', playlist_detail, name='playlist_detail'),

]

