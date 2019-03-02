from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from SwapDJ.api.Services import AppleService, SpotifyService

@api_view(['POST'])
def ImportPlaylist(request):
    SPOTIFY = 0
    APPLE_MUSIC = 1

    spotifyUserToken = request.session['spotifyToken']['access_token']
    appleUserToken = request.session['appleToken']
    appleDevToken = request.session['appleDevToken']

    if(request.data['service']['serviceFromValue'] == SPOTIFY):
        spotifyPlaylistJSON = request.data['playlist']
        spotifyPlaylistURL = spotifyPlaylistJSON['href']
        

        playlist = SpotifyService.GetPlaylistByURL(userToken=spotifyUserToken, playlistURL=spotifyPlaylistURL)
        


        appleServiceResponse = AppleService.ImportPlaylist(appleDevToken, appleUserToken, playlist)

        return Response(appleServiceResponse)

    elif(request.data['service']['serviceFromValue'] == APPLE_MUSIC):

        appleMusicPlaylistJSON = request.data['playlist']
        applePlaylistURL = appleMusicPlaylistJSON['href']

        playlist = AppleService.GetPlaylistByURL(appToken=appleDevToken, userToken=appleUserToken, playlistURL=applePlaylistURL)
        spotifyServiceResponse = SpotifyService.ImportPlaylist(spotifyUserToken, playlist['data'][0])

    return Response(status=200, data=spotifyServiceResponse)
