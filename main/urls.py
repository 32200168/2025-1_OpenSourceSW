from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),

]
