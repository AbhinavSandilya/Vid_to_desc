import os
import sys
import subprocess
import whisper
import gdown

def get_drive_direct_url(drive_url):
    if "file/d/" in drive_url:
        file_id = drive_url.split("file/d/")[1].split("/")[0]
    elif "id=" in drive_url:
        file_id = drive_url.split("id=")[1].split("&")[0]
    else:
        raise ValueError("Invalid Google Drive URL format.")
    return f"https://drive.google.com/uc?export=download&id={file_id}"



def download_video(url, output_path='video.mp4'):
    print("🔽 Downloading video from Google Drive...")
    try:
        gdown.download(url, output_path, quiet=False, fuzzy=True)
    except Exception as e:
        print(f"❌ Download failed: {e}")
        sys.exit(1)

    if not os.path.exists(output_path):
        print("❌ Download failed. File not found.")
        sys.exit(1)

    print("✅ Download complete.")
    return output_path


# def extract_audio_ffmpeg(video_path, audio_path='audio.wav'):
#     print("🎞️ Extracting audio with FFmpeg...")
#     cmd = [
#         'ffmpeg', '-y', '-i', video_path,
#         '-vn',            # no video
#         '-acodec', 'pcm_s16le',  # WAV format
#         '-ar', '16000',          # sample rate
#         '-ac', '1',              # mono audio
#         audio_path
#     ]
#     subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#     if not os.path.exists(audio_path):
#         print("❌ Audio extraction failed.")
#         sys.exit(1)
#     print("✅ Audio extracted.")
#     return audio_path

def extract_audio_ffmpeg(video_path, audio_path='audio.wav'):
    print("🎞️ Extracting audio with FFmpeg...")
    cmd = [
        'ffmpeg', '-y', '-i', video_path,
        '-vn',
        '-acodec', 'pcm_s16le',
        '-ar', '16000',
        '-ac', '1',
        audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ FFmpeg Error:\n", result.stderr)
        sys.exit(1)

    if not os.path.exists(audio_path):
        print("❌ Audio file not created.")
        sys.exit(1)

    print("✅ Audio extracted.")
    return audio_path

def transcribe_audio(audio_path):
    print("🧠 Transcribing audio using Whisper...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    print("✅ Transcription complete.")
    return result['text']

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python video_to_text.py <Google Drive URL>")
        sys.exit(1)

    drive_url = sys.argv[1]
    video_path = download_video(drive_url)
    audio_path = extract_audio_ffmpeg(video_path)
    text = transcribe_audio(audio_path)

    output_txt = "transcription.txt"
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"\n📄 Transcription saved to: {output_txt}")


    print("\n📝 Transcription Result:\n")
    # print(text)
