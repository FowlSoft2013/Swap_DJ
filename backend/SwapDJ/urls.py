"""SwapDJ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from SwapDJ.api.Views import SpotifyView, AppleMusicView, AppView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search_artist', SpotifyView.SearchArtist, name='search-artist'),
    path('login_user', SpotifyView.ManualLogin, name='spotify-login'),
    path('callback', SpotifyView.Callback, name='spotify-callback'),
    path('playlists', SpotifyView.GetUserPlaylists, name='spotify-user-playlists'),
    path('apple_music', AppleMusicView.CreateAppToken, name='initalize-apple-music'),
    path('apple_music_callback', AppleMusicView.Callback, name='apple-callback'),
    path('apple_playlists', AppleMusicView.GetUserPlaylists, name='apple-user-playlists'),
    path('import', AppView.ImportPlaylist, name='import-playlist'),
    path('spotify', SpotifyView.Authorized, name='sp-authorized'),
    path('apple', AppleMusicView.Authorized, name='apple-authorized'),
]
