import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import os
import re

client_id = '552b384c961f4b5cb54a473b25a1621c'
client_secret = '3b7601af339746719cd2a4c3167f301a'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_link = input('Enter the playlist link: ')

playlist_id = playlist_link.split('/')[-1].split('?')[0]
playlist_id = f"spotify:playlist:{playlist_id}"
print(f"PID {playlist_id}")

def sanitize_filename(filename):
    return re.sub(r'[\\/:*?"<>|]', '_', filename)

# Get the playlist tracks
try:
    results = sp.playlist_tracks(playlist_id)
except Exception as e:
    print('Error:', e)
    exit()

playlist_genre = input('Enter the genre of the playlist: ')

with open ('classes.txt', 'r+') as file:
    try:
        last_line = file.readlines()[-1]
        last_line = int(last_line.split("-")[0])
    except:
        file.write(f'{0} - {playlist_genre}')
    else:
        file.write(f'\n{last_line + 1} - {playlist_genre}')

counter = 0  # Initialize counter variable

for item in results['items']:
    if counter >= 50:
        break  # Break out of the loop after 50 iterations

    track = item['track']
    song_title = track['name']
    artist_name = track['artists'][0]['name']

    song_title = sanitize_filename(track['name'])
    artist_name = sanitize_filename(track['artists'][0]['name'])


    search_results = sp.search(q='track:' + song_title + ' artist:' + artist_name, type='track')
    if len(search_results['tracks']['items']) > 0:
        search_track = search_results['tracks']['items'][0]

        # Check if preview_url is available
        if 'preview_url' in search_track and search_track['preview_url']:
            preview_url = search_track['preview_url']
            mp3_dir = f'SpotifySongs/mp3_files/{playlist_genre}'  # Specify the directory for MP3 files
            os.makedirs(mp3_dir, exist_ok=True)
            mp3_file_path = os.path.join(mp3_dir, song_title + ' - ' + artist_name + '.mp3')

            with open(mp3_file_path, 'wb') as f:
                r = requests.get(preview_url)
                f.write(r.content)
            print(f"Downloaded {song_title} by {artist_name}")
            counter += 1  # Increment counter
        else:
            print(f"No preview available for {song_title} by {artist_name}")
    else:
        print('No results found for', song_title, 'by', artist_name)

print('Finished')

