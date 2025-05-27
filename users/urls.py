from django.urls import path, include
from . import views
from .views import playlist_view

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("taste/", views.taste_view, name="taste"),
    path("playlist/", playlist_view, name="playlist"),
]
