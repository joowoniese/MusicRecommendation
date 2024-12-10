import os
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import time

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(client_id="", client_secret=""))

def sanitize_title(title):
    title = re.sub(r'\(Official Music Video\)|\(Official Video\)', '', title, flags=re.IGNORECASE)
    title = re.sub(r'[\\/*?:"<>|]', "_", title) 
    title = re.sub(r"\s+", "_", title) 
    return title.strip()

def rename_file_if_exists(old_filepath, new_filepath):
    if os.path.exists(old_filepath): 
        new_dir = os.path.dirname(new_filepath)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)  

        os.rename(old_filepath, new_filepath) 
        print(f"File '{old_filepath}' renamed to '{new_filepath}'")
    else:
        print(f"File not found: {old_filepath}")

def get_song_features(song_title):
    try:
        results = sp.search(q=song_title, type='track', limit=1)
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_id = track['id']

            audio_features = sp.audio_features(track_id)[0]

            song_info = {
                'title': track['name'],
                'artist': [artist['name'] for artist in track['artists']],
                'loudness': audio_features['loudness'],
                'tempo': audio_features['tempo'],
                'mode': "Major" if audio_features['mode'] == 1 else "Minor",
                'danceability': audio_features['danceability'],
                'acousticness': audio_features['acousticness'],
                'valence': audio_features['valence']
            }
            print(song_info)
            return song_info
        else:
            print(f"노래 없음")
            return None

    except spotipy.exceptions.SpotifyException as e:
        if e.http_status == 429:
            retry_after = int(e.headers.get("Retry-After", 5))
            print(f"Rate limit")
            time.sleep(retry_after)
            return get_song_features(song_title)
        else:
            raise

def save_songs_from_wav_to_json(wav_directory, output_file):
    songs_data = []

    for filename in os.listdir(wav_directory):
        if filename.endswith(".wav"):
            song_title = sanitize_title(os.path.splitext(filename)[0])
            print(f"Spotify에서 '{song_title}' 정보 검색 중...")

            song_info = get_song_features(song_title)
            if song_info:
                songs_data.append(song_info)

                new_filename = f"{song_info['title']}.wav"
                old_filepath = os.path.join(wav_directory, filename)
                new_filepath = os.path.join(wav_directory, new_filename)

                if old_filepath != new_filepath:
                    rename_file_if_exists(old_filepath, new_filepath)

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(songs_data, f, ensure_ascii=False, indent=4)
            print(f"정보를 '{output_file}'에 저장")

            time.sleep(2)

wav_directory = f"/home/joowoniese/diffwave/src/audio_data/clean_audio/" 

save_songs_from_wav_to_json(wav_directory, f"/home/joowoniese/musiclabeling/music_metadata/music_jsonfiles/music_features_final.json")
