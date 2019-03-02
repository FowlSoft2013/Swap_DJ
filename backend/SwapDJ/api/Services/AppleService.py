import json, jwt, requests, time, sys
from base64 import b64encode
from SwapDJ.settings import APPLE_MUSIC_TEAM_ID, APPLE_MUSIC_KID, APPLE_SECRET

def CreateAppToken():
    header = {
        'alg': 'ES256',
        'kid': APPLE_MUSIC_KID
    }

    payload = {
            'iss': APPLE_MUSIC_TEAM_ID,
            'iat': time.time(),
            'exp': time.time() + 15777000
    }
    
    encoded = jwt.encode(payload, APPLE_SECRET, algorithm='ES256', headers=header)

    return encoded

def GetUserPlaylists(appToken, userToken):
    getPlaylistURL = 'https://api.music.apple.com/v1/me/library/playlists'

    header = {
        'Authorization': 'Bearer ' + appToken,
        'Music-User-Token': userToken 
    }

    playlistRequest = requests.get(url=getPlaylistURL, headers=header)

    return playlistRequest.json()

def CreatePlaylist(appToken, userToken, playlist):
    createPlaylistURL = 'https://api.music.apple.com/v1/me/library/playlists'

    applePlaylist = {
        'attributes': {
            'name': playlist['name'],
            'description': playlist['description']
        }
    }

    header = {
        'Authorization': 'Bearer ' + appToken,
        'Music-User-Token': userToken 
    }

    createPlaylistRequest = requests.post(url=createPlaylistURL, json=applePlaylist, headers=header)
    return createPlaylistRequest.json()

def PopulatePlaylistSongIDs(appToken, userToken, playlistID, playlistTracks):
    songIDs = []
    for playlistTrack in playlistTracks['items']:
        track = playlistTrack['track']
        album = track['album']
        artists = track['artists']
        trackName = track['name']

        searchedSong = SearchSong(artistName=artists[0]['name'], songTitle=trackName, albumTitle=album['name'], userToken=userToken, appToken=appToken)
        
        if('results' in searchedSong):
            results = searchedSong['results']
            if('songs' in results):
                songs = results['songs']
                songData = songs['data'][0]
                songIDs.append(songData['id'])
            
    return songIDs

def SearchSong(artistName, songTitle, albumTitle, userToken, appToken):
    searchURL = 'https://api.music.apple.com/v1/catalog/us/search'

    songTitleFormatted = songTitle
    if ' (' in songTitleFormatted:
        removeFeatureStart = songTitleFormatted.index(' (')
        songTitleFormatted = songTitleFormatted[:removeFeatureStart]

    albumTitleFormatted = albumTitle
    if ' (' in albumTitleFormatted:
        removeParenthesisStart = albumTitleFormatted.index(' (')
        albumTitleFormatted = albumTitleFormatted[:removeParenthesisStart]

    query = '?term={0} {1} {2}'.format(songTitleFormatted, artistName, albumTitleFormatted)

    searchURL += query

    header = {
        'Authorization': 'Bearer ' + appToken,
        'Music-User-Token': userToken 
    }

    searchRequest = requests.get(url=searchURL, headers=header)
    return searchRequest.json()

def AddSongsToPlaylist(playlistID, songIDs, appToken, userToken):
    addTrackToPlaylistURL = 'https://api.music.apple.com/v1/me/library/playlists/{0}/tracks'.format(playlistID)
    header = {
        'Authorization': 'Bearer ' + appToken,
        'Music-User-Token': userToken 
    }

    songs = []

    for id in songIDs:
        song = {
            'id': id,
            'type': 'songs'
        }
        songs.append(song)

    jsonData = {
        'data': songs
    }

    addSongsToPlaylistRequest = requests.post(url=addTrackToPlaylistURL, json=jsonData, headers=header)

    return addSongsToPlaylistRequest

def ImportPlaylist(appToken, userToken, playlist):
    creationResponse = CreatePlaylist(appToken=appToken, userToken=userToken, playlist=playlist)
    creationResponseData = creationResponse['data']
    newPlaylistID = creationResponseData[0]['id']
 
    songIDs = PopulatePlaylistSongIDs(appToken=appToken, userToken=userToken, playlistID=newPlaylistID, playlistTracks=playlist['tracks'])

    addSongsResponse = AddSongsToPlaylist(playlistID=newPlaylistID, songIDs=songIDs, appToken=appToken, userToken=userToken)

    return addSongsResponse

def GetPlaylistByURL(appToken, userToken, playlistURL):
    httpsPlaylistURL = 'https://api.music.apple.com' + playlistURL
    queryParams = '?include=tracks'
    httpsPlaylistURL += queryParams
    
    header = {
        'Authorization': 'Bearer ' + appToken,
        'Music-User-Token': userToken 
    }
    getPlaylist = requests.get(url=httpsPlaylistURL, headers=header)

    return getPlaylist.json()

def IsAuthorized(appToken, userToken):
    appleAuthorizeURL = 'https://api.music.apple.com/v1/me/storefront'
    header = {
        'Authorization': 'Bearer ' + appToken,
        'Music-User-Token': userToken 
    }

    authorizedResponse = requests.get(url=appleAuthorizeURL, headers=header)

    return authorizedResponse.json()

