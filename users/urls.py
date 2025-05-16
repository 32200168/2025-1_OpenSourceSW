from django.urls import path, include
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("taste/", views.taste_view, name="taste"),
    path("playlist/", views.playlist_view, name="playlist"),
]
