import os
import subprocess

def convert_mov_to_mp4():
    mov_path = input("Enter the full path to the .mov file: ").strip()

    if not os.path.isfile(mov_path):
        print("❌ File does not exist.")
        return

    if not mov_path.lower().endswith(".mov"):
        print("❌ File is not a .mov video.")
        return

    # Construct output .mp4 path
    base, _ = os.path.splitext(mov_path)
    mp4_path = base + ".mp4"

    print(f"Converting '{mov_path}' to '{mp4_path}'...")

    try:
        subprocess.run([
            "ffmpeg",
            "-i", mov_path,
            "-vcodec", "libx264",
            "-acodec", "aac",
            mp4_path
        ], check=True)
        print("✅ Conversion complete.")
    except subprocess.CalledProcessError:
        print("❌ Conversion failed. Make sure ffmpeg is installed and working.")

if __name__ == "__main__":
    convert_mov_to_mp4()
