from . import views
from django.urls import path, include
urlpatterns = [
    path('', views.index, name='index'),
    path('register_user/', views.register_user, name='register_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('profile/', views.profile, name='profile'),
    path('settings/',views.settings_page,name='settings'),
    path('delete-account/',views.delete_account,name='delete_account'),
    path('profile/change-picture/',views.change_profile_picture,name='change_profile_picture'),
    path('profile/remove-picture/',views.remove_profile_picture,name='remove_profile_picture'),
    path('create_playlist/', views.create_playlist, name='create_playlist'),
    path('view_playlist/<int:pk>/', views.view_playlist, name='view_playlist'),
    path('all_playlists/', views.all_playlists, name='all_playlists'),
    path('like/<int:song_id>/', views.toggle_like, name='toggle_like'),
    path('liked_songs/', views.liked_songs, name='liked_songs'),
    path('delete_playlist/<int:pk>/',views.delete_playlist,name='delete_playlist'),
    
]