from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from SwapDJ.api.Services import SpotifyService
from SwapDJ.api.Serializers.serializers import SpotifyTokenSerializer

@api_view(['GET'])
def SearchArtist(request):
    searchText = request.query_params['searchText']
    result = SpotifyService.SearchArtist(searchText)
    response = Response(result)
    
    return response

@api_view(['POST'])
def Login(request):
    username = request.data['username']
    scope = ''

    sp_token = SpotifyService.LoginUser(username, scope)

    if sp_token:
        response = Response(sp_token)
        response.status_code = 200

        print(response)

        return response
    else:
        return Response(status=401)

@api_view(['GET'])
def ManualLogin(request):
    response = SpotifyService.ManualLogin()
    response = Response(response)

    print(response)

    return response


@api_view(['GET'])
def Callback(request):
    authorization_code = request.query_params['code']
    
    sp_token = SpotifyService.RequestUserToken(authorization_code)
    tokenSerializer = SpotifyTokenSerializer(data=sp_token, many=False)

    tokenSerializer.is_valid(raise_exception=True)
    request.session['spotifyToken'] = tokenSerializer.data
    print(request.session.keys())
    print(tokenSerializer)

    response = Response(status=200)

    return response

@api_view(['GET'])
def GetUserPlaylists(request):
    response = Response()
    if('spotifyToken' in request.session):
        user_token = SpotifyTokenSerializer(data=request.session['spotifyToken'])
        user_token.is_valid()
        
        user_playlists = SpotifyService.GetUserPlaylists(user_token.data)
        response.status_code = 200
        response.data = user_playlists
    else:
        response.status_code = 401
    

    return response

@api_view(['GET'])
def Authorized(request):
    if 'spotifyToken' in request.session:
        spotifyUserToken = request.session['spotifyToken']['access_token']

        isSpotifyAuthorized = SpotifyService.IsAuthorized(spotifyUserToken)
        if('display_name' in isSpotifyAuthorized):
            return Response(status=200)


    return Response(status=401)
