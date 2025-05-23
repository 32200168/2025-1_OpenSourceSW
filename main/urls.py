from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('profile/<str:username>/', views.profile_view, name='profile'),

]
