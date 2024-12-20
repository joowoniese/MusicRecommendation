import json
import numpy as np
import os

json_file_path = "/home/joowoniese/musiclabeling/music_metadata/music_jsonfiles/merged_music.json"

with open(json_file_path, "r") as file:
    data = json.load(file)

tempo = []
danceability = []
valence = []
titles = []

for song in data:
    tempo.append(song.get("tempo"))
    danceability.append(song.get("danceability"))
    valence.append(song.get("loudness"))
    titles.append(song.get("title"))

tempo = np.array(tempo)
danceability = np.array(danceability)
valence = np.array(valence)

tempo = (tempo - tempo.min()) / (tempo.max() - tempo.min())
danceability = (danceability - danceability.min()) / (danceability.max() - danceability.min())
valence = (valence - valence.min()) / (valence.max() - valence.min())

def get_track_info_from_json(track_name):
    for song in data:
        if song.get("title") and song["title"].lower() == track_name.lower():
            track_info = {
                "name": song.get("title"),
                "tempo": song.get("tempo"),
                "danceability": song.get("danceability"),
                "valence": song.get("loudness"),
            }
            return track_info
    print(f"No track found for {track_name} in the JSON file.")
    return None

if __name__ == "__main__":
    track_name = input("Track name: ")
    track_info = get_track_info_from_json(track_name)

    if track_info is None:
        print("No track information found. Exiting.")
        exit(1)

    input_title = track_info['name']
    input_tempo = track_info['tempo']
    input_danceability = track_info['danceability']
    input_valence = track_info['valence']

    print(f"Track Name: {track_info['name']}")
    print(f"Tempo: {track_info['tempo']}")
    print(f"Danceability: {track_info['danceability']}")
    print(f"Valence: {track_info['valence']}")

    input_song_features = np.array([input_tempo, input_danceability, input_valence])

    distances = []
    for i in range(len(titles)):
        current_song = np.array([tempo[i], danceability[i], valence[i]])
        distance = np.linalg.norm(input_song_features - current_song)
        distances.append((distance, titles[i], i))

    distances.sort(key=lambda x: x[0])
    recommended_songs = distances[1:4]
    farthest_songs = distances[-3:]

    print(f"\nSelected Song: {input_title}")
    print("\nRecommended Songs (Closest):")
    for distance, title, idx in recommended_songs:
        print(f"  - {title} (Distance: {distance:.4f})")

    print("\nFarthest Songs:")
    for distance, title, idx in farthest_songs:
        print(f"  - {title} (Distance: {distance:.4f})")
