import whisper
import os
import yt_dlp

# List of YouTube video and playlist URLs
urls = [
    "https://www.youtube.com/watch?v=G0f_vdRmFk4",
    "https://www.youtube.com/watch?v=85TF87ItZJc",
    "https://www.youtube.com/watch?v=qCqO2smoRic",
    "https://www.youtube.com/watch?v=tbizTKb6uzs",
    "https://www.youtube.com/watch?v=RU9Mvf8fMBU",
    "https://www.youtube.com/watch?v=5gzlfjvE6Rg&list=PLbhO4L_ozdfQKJWWk3WsRXHuSNyXLZgND&index=2",
    "https://www.youtube.com/watch?v=3K7CDGkmoAo&list=PLbhO4L_ozdfQKJWWk3WsRXHuSNyXLZgND&index=3",
    "https://www.youtube.com/watch?v=6HtZbUkgDpk&list=PLbhO4L_ozdfQKJWWk3WsRXHuSNyXLZgND&index=4",
    "https://www.youtube.com/watch?v=nYGSs4Xu4I0&list=PLbhO4L_ozdfQKJWWk3WsRXHuSNyXLZgND&index=5",
    "https://www.youtube.com/watch?v=yzoKNxqFuuU&list=PLbhO4L_ozdfQKJWWk3WsRXHuSNyXLZgND&index=6",
    "https://www.youtube.com/watch?v=VT1KORkNZm0&list=PLbhO4L_ozdfQKJWWk3WsRXHuSNyXLZgND&index=8",
    "https://www.youtube.com/watch?v=rH4nQdr7n4E&list=PLbhO4L_ozdfQKJWWk3WsRXHuSNyXLZgND&index=11",
    "https://www.youtube.com/watch?v=0R32VohvgkI&list=PLbhO4L_ozdfQKJWWk3WsRXHuSNyXLZgND&index=12",
    "https://www.youtube.com/watch?v=8qQwadwh4ZE&list=PLbhO4L_ozdfQKJWWk3WsRXHuSNyXLZgND&index=13",
    "https://www.youtube.com/watch?v=qwW2eXCJabM&list=PLbhO4L_ozdfQKJWWk3WsRXHuSNyXLZgND&index=14",
    "https://www.youtube.com/watch?v=lPVcWyDVxpk",
    "https://www.youtube.com/playlist?list=PLbdTJRfShNLs_vhwSJBvU1sbt2griw5Xs",
    "https://www.youtube.com/playlist?list=PLbdTJRfShNLtRjQTxs7_aT3zc09a3vQqG"
]

# Create folders for audio and transcripts
os.makedirs("audios", exist_ok=True)
os.makedirs("transcripts", exist_ok=True)

# yt-dlp options
ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "audios/%(title)s.%(ext)s",
    "quiet": True,
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}

# Download audio files
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(urls)

# Load Whisper model
model = whisper.load_model("base")  # You can also try "small", "medium", or "large"

# Transcribe all MP3 files
for filename in os.listdir("audios"):
    if filename.endswith(".mp3"):
        path = os.path.join("audios", filename)
        print(f"Transcribing: {filename}")
        result = model.transcribe(path, language="pt")
        # Save transcription to text file
        txt_file = os.path.join("transcripts", filename.replace(".mp3", ".txt"))
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(result["text"])
