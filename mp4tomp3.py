"""  
This script when executed in a directory containing MP4 files, will automatically convert all the MP4 files to MP3 files.   
Files will be saved with the same filename but with the .mp3 extension.
"""

import os
import subprocess

def convert_to_mp3(video_path, audio_path):
    # Command to extract audio and save as MP3
    cmd = ["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path]
    subprocess.call(cmd)

# Get the current directory where the script is located
folder_path = os.getcwd()

for video_file in os.listdir(folder_path):
    if video_file.endswith(".mp4"):
        video_path = os.path.join(folder_path, video_file)
        audio_path = os.path.join(folder_path, video_file.replace(".mp4", ".mp3"))
        
        convert_to_mp3(video_path, audio_path)

print("Conversion completed!")
