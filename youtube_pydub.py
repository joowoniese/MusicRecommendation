import yt_dlp
from pydub import AudioSegment
import os
import re

def sanitize_title(title):
    title = re.sub(r'\[Official Video\]|\[Official Music Video\]|\(Official Music Video\)|\(Official Video\)|\(Official Lyric Video\)|\(Lyric Video\)|\(Official Audio\)|\(Audio\)|\(Lyrics\)|\(Official Visualizer\)|\(MUSIC VIDEO\)|\(Official Visualizer\)', '', title, flags=re.IGNORECASE)
    title = re.sub(r'[\\/*?:"<>|]', "", title)
    return title.strip()

def download_playlist_as_wav(playlist_url):
    playlist_id = playlist_url.split("list=")[-1]
    output_folder = f"./music_wavefiles/playlist_{playlist_id}"
    os.makedirs(output_folder, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': False,
        'extract_flat': True,
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)

        for entry in playlist_info['entries']:
            video_id = entry['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            title = entry.get('title', f"video_{video_id}")

            sanitized_title = sanitize_title(title)
            output_path = os.path.join(output_folder, f"{sanitized_title}.wav")

            if os.path.exists(output_path):
                print(f"이미 존재하는 파일 : {output_path}")
                continue

            try:
                ydl_opts_audio = {
                    'format': 'bestaudio/best',
                    'outtmpl': f'temp_audio_{video_id}.%(ext)s',
                    'quiet': True
                }
                with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl_audio:
                    ydl_audio.download([video_url])

                audio = AudioSegment.from_file(f"temp_audio_{video_id}.webm", format="webm")
                audio.export(output_path, format="wav")
                print(f"WAV 파일로 저장되었습니다: {output_path}")

                os.remove(f"temp_audio_{video_id}.webm")

            except Exception as e:
                print(f"오류 발생: {e}")

playlist_urls = [
    "https://www.youtube.com/playlist?list=PLNjVKDn-Jmf6Kf7GBrg_1JPcLbTfaKLXj",
    "https://www.youtube.com/playlist?list=PLEaPJ6oGci9euI_IBWr6-C5Ypy5vzXTAJ",
    "https://www.youtube.com/playlist?list=PLWbNJuZfRvW-5SWIsYWxKLIKVDLpfqz0t",
    "https://www.youtube.com/playlist?list=PLRZlMhcYkA2Hqh5QvkEagOJwSG21GNLN2",
    "https://www.youtube.com/playlist?list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj"
]

for i, playlist_url in enumerate(playlist_urls):
    print(f"\n재생목록 {i + 1} 처리...")
    download_playlist_as_wav(playlist_url)
