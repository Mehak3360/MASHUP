import sys
import os
import yt_dlp

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

print("Inputs accepted ✅")
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

# ---------------- DOWNLOAD + CONVERT TO MP3 ---------------- #

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': f'{audio_folder}/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
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

print("Audio download & conversion completed ✅")

from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import os
import yt_dlp

AudioSegment.converter = r"C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"

# Example: video aur audio folders
video_folder = "videos"
audio_folder = "audios"

os.makedirs(audio_folder, exist_ok=True)

# Video to audio conversion
for file in os.listdir(video_folder):
    if file.endswith((".mp4", ".webm", ".mkv")):
        video_path = os.path.join(video_folder, file)
        audio_path = os.path.join(audio_folder, file.rsplit(".", 1)[0] + ".mp3")

        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, ffmpeg_params=["-loglevel", "panic"], ffmpeg_exe=r"C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe")
        video.close()

print("Audio extraction completed ✅")

all_audios = []
for file in os.listdir(audio_folder):
    if file.endswith(".mp3"):
        audio = AudioSegment.from_file(os.path.join(audio_folder, file), format="mp3")
        all_audios.append(audio)

# Concatenate all audios
if all_audios:
    mashup = sum(all_audios)
    mashup.export("output.mp3", format="mp3", codec="mp3")
    print("Mashup exported ✅")