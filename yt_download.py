import os
from pytube import YouTube

# Create a directory for videos if it doesn't exist
video_dir = "videos"
os.makedirs(video_dir, exist_ok=True)

# YouTube video URL (change this to the video you want)
video_url = "https://www.youtube.com/watch?v=6XDGBBPuef4&t=328s"  # Example URL

# Download the highest resolution video
try:
    yt = YouTube(video_url)
    video_stream = yt.streams
    
    print(f"Downloading: {yt.title}")
    video_stream.download(output_path=video_dir)
    
    print(f"Download complete! Video saved in '{video_dir}' directory.")
except Exception as e:
    print(f"Error: {e}")
