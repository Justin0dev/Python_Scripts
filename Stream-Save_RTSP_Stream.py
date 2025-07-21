import subprocess
import os
import threading

"""
This script records an RTSP stream using FFmpeg, saving them as segmented MP4 and MP3 files.
The `record_rtsp` function runs these recordings concurrently in separate threads,
allowing simultaneous video and audio capture. Each recording is segmented into 10-minute (600-second) chunks. 
The script handles errors and interruptions gracefully.  Requires FFmpeg to be
installed and in system PATH.  
RTSP stream URL needs to be set at the end of the script under the variable rtsp_stream_url =
"""

def record_video(rtsp_url, output_filename_pattern):
    cwd = os.getcwd()
    output_filepath = os.path.join(cwd, output_filename_pattern)

    command = [
        'ffmpeg',
        '-i', rtsp_url,
        '-c:v', 'copy',
        '-c:a', 'copy',
        '-f', 'segment',
        '-segment_time', '600',
        '-reset_timestamps', '1',
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
    cwd = os.getcwd()
    output_filepath = os.path.join(cwd, output_filename_pattern)

    command = [
        'ffmpeg',
        '-i', rtsp_url,
        '-vn',
        '-ac', '2',
        '-ar', '44100',
        '-ab', '320k',
        '-f', 'segment',
        '-segment_time', '600',
        '-reset_timestamps', '1',
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

rtsp_stream_url = "rtsp://admin:3debES00@192.168.0.201:554/cam/realmonitor?channel=1&subtype=1"
record_rtsp(rtsp_stream_url, 'output_video_%03d.mp4', 'output_audio_%03d.mp3')

input("Press Enter to exit...")
