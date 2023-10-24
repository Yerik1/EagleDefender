import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# Configura las credenciales de la aplicación
clientId = "6bc23490ba8b4cad9b28ab746e6cd127"
clientSecret = "3868dd6c926141f8aa81c97c6a0fe126"
redirectUri = 'http://localhost:8888/callback'
scope = 'user-library-read user-modify-playback-state playlist-modify-public playlist-modify-private user-read-playback-state  user-read-currently-playing user-library-modify playlist-read-private playlist-read-collaborative'
username = "josegd1605"
scope1 = "user-modify-playback-state user-library-read"
token1 = util.prompt_for_user_token(username, scope, clientId, clientSecret, redirectUri)
token = util.prompt_for_user_token(username, scope1, clientId, clientSecret, redirectUri)
sp = spotipy.Spotify(auth=token1)
sp1 = spotipy.Spotify(auth=token)
songs = []
for i in range(3):
    song = input(f'Ingrese el nombre de la cancion {i+1}:')
    songs.append(song)

'''songName = "la santa"
results = sp.search(q=songName, type='track', limit=1)'''

playlistName = 'Playlist Prueba1'
playlist = sp.user_playlist_create(user=username, name=playlistName, public=True)

for song in songs:
    results = sp.search(q=f'track:{song}', type='track')
    if results['tracks']['items']:
        trackId = results['tracks']['items'][0]['id']
        sp.playlist_add_items(playlist['id'], [trackId])

print(f'se han agregado las canciones a: {playlistName}')

'''if results['tracks']['items']:
    trackUri = results['tracks']['items'][0]['uri']
else:
    print("fuck it")
    exit()'''

playlistID = playlist['id']
playlistSongs = sp.playlist_items(playlistID)


for item in playlistSongs['items']:
    track = item['track']
    trackName = track['name']
    trackId = track['id']

    audioFeatures = sp.audio_features([trackId])[0]

    # Imprime las audio features de la canción
    print(f'Audio Features de "{trackName}":')
    print(f'Tempo: {audioFeatures["tempo"]}')
    print(f'Energía: {audioFeatures["energy"]}')
    print(f'Danza: {audioFeatures["danceability"]}')

#sp.start_playback(uris=[trackUri])
