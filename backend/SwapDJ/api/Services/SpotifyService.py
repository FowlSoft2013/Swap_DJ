import requests
from base64 import b64encode
from spotipy import Spotify, util
from spotipy.oauth2 import SpotifyClientCredentials
from SwapDJ.settings import SPOTIFY_CLIENT_ID, SPOTIFY_SECRET_KEY, SPOTIFY_REDIRECT_URL

def InitalizeClientCredentials():
    clientCredientialManager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_SECRET_KEY)
    sp = Spotify(client_credentials_manager=clientCredientialManager)

    return sp

def SearchArtist(artistName):
    spotify = InitalizeClientCredentials()
    results =  spotify.search(q='artist:' + artistName, type='artist')

    return results

def LoginUser(username, scope):
    spotifyUserToken = util.prompt_for_user_token(username, 
                scope=scope, 
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_SECRET_KEY,
                redirect_uri= SPOTIFY_REDIRECT_URL)

    return spotifyUserToken

def ManualLogin():
    scope = ''

    response_type = 'code'
    redirect_uri = 'http://localhost:8000'
    state = ''
    scope = 'playlist-read-private playlist-read-public playlist-modify-private playlist-modify-public'
    show_dialog = ''

    authorize_url = 'https://accounts.spotify.com/authorize?'
    authorize_url += 'clientID=' +SPOTIFY_CLIENT_ID + '&'
    authorize_url += 'reponse_type=' + response_type + '&'
    authorize_url +=  'redirect_uri=' + redirect_uri
    authorize_url +=  'scope=' + scope

    response = requests.get(url=authorize_url)

    return response.json()

def RequestUserToken(authorization_code):
    spotify_token_url = 'https://accounts.spotify.com/api/token'
    key = SPOTIFY_CLIENT_ID + ":" + SPOTIFY_SECRET_KEY

    b64_encoded_key = b64encode(key.encode())
    
    request_header = {
        'Authorization': 'Basic ' + b64_encoded_key.decode('utf-8')
    }

    post_data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': SPOTIFY_REDIRECT_URL
    }

    tokenRequest = requests.post(url=spotify_token_url, data=post_data, headers=request_header)

    return tokenRequest.json()

def GetUserPlaylists(token):
    sp = Spotify(auth=token['access_token'])
    user_playlists = sp.current_user_playlists()

    return user_playlists

def GetPlaylistByURL(userToken, playlistURL):
    header = {
        'Authorization': 'Bearer ' + userToken
    }
    
    fields = 'description,id,images(url),name,owner,tracks.items(track(name, album(name), artists, href))'

    playlistURL += '?fields=' + fields

    playlistRequest = requests.get(url=playlistURL, headers=header)

    return playlistRequest.json()

def SearchTrack(userToken, track):
    searchURL = 'https://api.spotify.com/v1/search'
    attributes = track['attributes']
    trackName = attributes['name']

    header = {
        'Authorization': 'Bearer ' + userToken
    }

    queryParams = '?q="{0}"&type=track&fields={1}&limit=1'.format(trackName, '')
    searchURL += queryParams

    searchedSong = requests.get(searchURL, headers=header)

    return searchedSong.json()

def PopulatePlaylistTrackIDs(userToken, playlist):
    relationships = playlist['relationships']
    tracks = relationships['tracks']['data']
    trackIDs = []

    for track in tracks:
        spotifyTrack = SearchTrack(userToken, track)
        if('tracks' in spotifyTrack):
            spotifyTrack = spotifyTrack['tracks']
            if('items' in spotifyTrack and len(spotifyTrack['items']) > 0):
                trackData = spotifyTrack['items'][0]
                spotifyTrackURI = trackData['uri']
                trackIDs.append(spotifyTrackURI)

    return trackIDs

def AddTracksToPlaylist(userToken, playlistID, trackIDs):
    addTracksURL = 'https://api.spotify.com/v1/playlists/{0}/tracks'.format(playlistID)

    header = {
        'Authorization': 'Bearer ' + userToken
    }

    postData = {
        'uris': trackIDs,
        'position': 0
    }

    addTracksToPlaylistRequest = requests.post(url=addTracksURL, json=postData, headers=header)


    return addTracksToPlaylistRequest.json()

def CreatePlaylist(userToken, playlist):
    user_id = IsAuthorized(userToken)['display_name']
    createPlaylistURL = 'https://api.spotify.com/v1/users/{0}/playlists'.format(user_id)
    attributes = playlist['attributes']
    description = attributes['description']

    postData = {
        'name': attributes['name'],
        'public': False,
        'collaborative': False,
        'description': description['standard']
    }

    header = {
        'Authorization': 'Bearer ' + userToken,
        'Content-Type': 'application/json'
    }

    createPlaylistResponse = requests.post(url=createPlaylistURL, json=postData, headers=header)

    return createPlaylistResponse.json()

def ImportPlaylist(userToken, playlist):
    createdPlaylist = CreatePlaylist(userToken, playlist)
    newPlaylistID = createdPlaylist['id']
    populatedPlaylistTrackIDs = PopulatePlaylistTrackIDs(userToken, playlist)
    newPlaylist = AddTracksToPlaylist(userToken, newPlaylistID, populatedPlaylistTrackIDs)

    return newPlaylist

def IsAuthorized(userToken):
    spotifyAuthURL = 'https://api.spotify.com/v1/me'

    header = {
        'Authorization': 'Bearer ' + userToken
    }

    spotifyAuth = requests.get(url=spotifyAuthURL, headers=header)

    return spotifyAuth.json()
