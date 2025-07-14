from flask import Flask, request, jsonify
import gdown
from moviepy.editor import VideoFileClip
from transformers import pipeline
import os

app = Flask(__name__)

# Load Hugging Face pipelines once at startup
asr_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-base")
gen_pipeline = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.1", device=0)

def download_video_from_gdrive(gdrive_url, output_path="video.mp4"):
    file_id = gdrive_url.split("/")[-2]
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output_path, quiet=False)
    return output_path

def extract_audio(video_path, audio_path="audio.wav"):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, verbose=False, logger=None)
    return audio_path

def transcribe_audio(audio_path):
    result = asr_pipeline(audio_path)
    return result['text']

def generate_response(transcript):
    prompt = f"Summarize or respond to this video transcript: {transcript}"
    response = gen_pipeline(prompt, max_new_tokens=200)
    return response[0]['generated_text']

@app.route("/process", methods=["POST"])
def process_video():
    data = request.json
    if "video_url" not in data:
        return jsonify({"error": "Missing 'video_url' in request."}), 400

    try:
        video_path = download_video_from_gdrive(data["video_url"])
        audio_path = extract_audio(video_path)
        transcript = transcribe_audio(audio_path)
        response = generate_response(transcript)

        os.remove(video_path)
        os.remove(audio_path)

        return jsonify({
            "transcript": transcript,
            "response": response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
