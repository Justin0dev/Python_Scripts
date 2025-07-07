import subprocess
import os
import threading
from datetime import datetime

def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_output_filename(output_filename_pattern):
    cwd = os.getcwd()
    return os.path.join(cwd, output_filename_pattern)

def record_video(rtsp_url, output_filename_pattern):
    output_filepath = get_output_filename(output_filename_pattern)

    command = [
        'ffmpeg',
        '-i', rtsp_url,
        '-c:v', 'copy',
        '-c:a', 'copy',
        '-segment_time', '600',
        '-f', 'segment',
        output_filepath
    ]

    try:
        print("Recording MP4...")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print("Error during MP4 recording.")
    except KeyboardInterrupt:
        print("MP4 recording interrupted.")

def record_audio(rtsp_url, output_filename_pattern):
    output_filepath = get_output_filename(output_filename_pattern)

    command = [
        'ffmpeg',
        '-i', rtsp_url,
        '-vn',
        '-ac', '2',
        '-ar', '44100',
        '-ab', '320k',
        '-segment_time', '600',
        '-f', 'segment',
        output_filepath
    ]

    try:
        print("Recording MP3...")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print("Error during MP3 recording.")
    except KeyboardInterrupt:
        print("MP3 recording interrupted.")

def record_rtsp(rtsp_url, output_filename_pattern_mp4, output_filename_pattern_mp3):
    # Starting video recording in a new thread
    video_thread = threading.Thread(target=record_video, args=(rtsp_url, output_filename_pattern_mp4))
    video_thread.start()

    # Starting audio recording in a new thread
    audio_thread = threading.Thread(target=record_audio, args=(rtsp_url, output_filename_pattern_mp3))
    audio_thread.start()

    # Wait for both threads to complete
    video_thread.join()
    audio_thread.join()

rtsp_stream_url = "rtsp://USER:PASSWORD@IP_ADDRESS/cam/realmonitor?channel=1&subtype=1"
record_rtsp(rtsp_stream_url, 'output_video_%s.mp4', 'output_audio_%s.mp3')

input("Press Enter to exit...")
