from django.urls import path
from . import views
from playlist.views import playlist_view_from_main

urlpatterns = [
    path('', views.main_view, name='main'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('recommend/', views.recommendation_view, name='recommendation'),
    path('search/', views.hashtag_view, name='search'),

]

