import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import time

# Configura las credenciales de la aplicación
clientId = "6bc23490ba8b4cad9b28ab746e6cd127"
clientSecret = "3868dd6c926141f8aa81c97c6a0fe126"
redirectUri = 'http://localhost:8888/callback'
scope = 'user-library-read user-modify-playback-state playlist-modify-public playlist-modify-private user-read-playback-state  user-read-currently-playing user-library-modify playlist-read-private playlist-read-collaborative'
username = "12186342048"
scope1 = "user-modify-playback-state  user-library-read"
token1 = util.prompt_for_user_token(username, scope, clientId, clientSecret, redirectUri)
token = util.prompt_for_user_token(username, scope1, clientId, clientSecret, redirectUri)
sp = spotipy.Spotify(auth=token1)
sp1 = spotipy.Spotify(auth=token)

def createPlaylist(songs):
    '''CREACION DE LA PLAYLIST'''
    playlistName = 'Playlist Prueba3'
    playlist = sp.user_playlist_create(user=username, name=playlistName, public=True)

    for song in songs:
        results = sp.search(q=f'track:{song}', type='track')
        if results['tracks']['items']:
            trackId = results['tracks']['items'][0]['id']
            sp.playlist_add_items(playlist['id'], [trackId])

            '''trackUri = results['tracks']['items'][0]['uri']
            sp.start_playback(uris=trackUri)'''

    print(f'se han agregado las canciones a: {playlistName}')
    return [playlist,songs]
# GENERAR EL LOOP
'''currentTrack = sp.current_playback()
if currentTrack:
    currentTrackUri = currentTrack['item']['uri']

    while True:
        time.sleep(1)

        if currentTrack['progress_ms'] >= currentTrack['item']['duration_ms']:
            sp.start_playback(uris=currentTrackUri)'''

def playSong(playlist,songs,number):
    results = sp.search(q=songs[number], type='track', limit=1)
    if results['tracks']['items']:
        trackUri = results['tracks']['items'][0]['uri']
    else:
        print("fuck it")
        exit()
    sp.start_playback(uris=[trackUri])
    '''ACCEDER A LAS AUDIO FEATURES'''
    playlistID = playlist['id']
    playlistSongs = sp.playlist_items(playlistID)

    for item in playlistSongs['items']:
        track = item['track']
        trackName = track['name']
        print(trackName)
    item =playlistSongs['items'][number]
    track = item['track']
    trackName = track['name']
    trackId = track['id']

    audioFeatures = sp.audio_features([trackId])[0]
    # Imprime las audio features de la canción
    print(f'Audio Features de "{trackName}":')
    print(f'Tiempo: {audioFeatures["duration_ms"]}')
    print(f'Tempo: {audioFeatures["tempo"]}')
    print(f'Energía: {audioFeatures["energy"]}')
    print(f'Danza: {audioFeatures["danceability"]}')

    return[audioFeatures["duration_ms"],audioFeatures["tempo"]]

def pauseSong():
    sp.pause_playback()

def searchSong(songName):
    results = []
    search_results = sp.search(q=f'track:{songName}', type='track')

    for track in search_results['tracks']['items'][:3]:
        track_name = track['name']
        track_artist = track['artists'][0]['name']  # Supongo que tomas al primer artista de la lista si hay varios
        results.append(track_name+" "+track_artist)
    print(results)
    return results

#play=createPlaylist()
#playSong(play[0],play[1])