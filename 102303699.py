import sys
import os

# -------- FORCE FFMPEG PATH -------- #
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin"

import yt_dlp
from pydub import AudioSegment

# ---------------- INPUT VALIDATION ---------------- #

if len(sys.argv) != 5:
    print("Usage: python RollNumber.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
    sys.exit(1)

singer = sys.argv[1]
num_videos = int(sys.argv[2])
duration = int(sys.argv[3])
output_file = sys.argv[4]

if num_videos <= 10:
    print("Error: Number of videos must be greater than 10")
    sys.exit(1)

if duration <= 20:
    print("Error: Audio duration must be greater than 20 seconds")
    sys.exit(1)

if not output_file.endswith(".mp3"):
    print("Error: Output file must be .mp3")
    sys.exit(1)

print("Inputs accepted ")
print("Singer:", singer)
print("Videos:", num_videos)
print("Duration:", duration)
print("Output:", output_file)

# ---------------- CREATE AUDIO FOLDER ---------------- #

audio_folder = "audios"
os.makedirs(audio_folder, exist_ok=True)

# ---------------- READ VIDEO LINKS ---------------- #

with open("videos.txt", "r") as file:
    video_links = file.readlines()



ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': f'{audio_folder}/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'ffmpeg_location': r"C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin"
}

count = 0

for link in video_links:
    if count >= num_videos:
        break

    link = link.strip()

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        count += 1
    except:
        print("Error downloading:", link)

print("Audio download & conversion completed ")

# ---------------- TRIM + MERGE ---------------- #

audio_files = []

for file in os.listdir(audio_folder):
    if file.endswith(".mp3"):
        path = os.path.join(audio_folder, file)
        audio_files.append(path)

trimmed_songs = []

for file in audio_files:
    song = AudioSegment.from_mp3(file)
    start_time = (len(song) // 2) - (duration * 1000 // 2)
    end_time = start_time + (duration * 1000)
    trimmed = song[start_time:end_time]  
    trimmed = trimmed.fade_in(1000).fade_out(1000)
    trimmed_songs.append(trimmed)

if not trimmed_songs:
    print("No audio files found!")
    sys.exit(1)

mashup = AudioSegment.empty()

for song in trimmed_songs:
    mashup += song

mashup.export(output_file, format="mp3")

print("Mashup created successfully ")