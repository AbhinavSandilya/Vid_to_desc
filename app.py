from send_to_model import call_vertex_model
from flask import Flask, request, jsonify, render_template
import os
import whisper
import subprocess
import uuid

app = Flask(__name__)
model = whisper.load_model("base")  # Load once at startup

def extract_audio_ffmpeg(video_path, audio_path):
    cmd = [
        'ffmpeg', '-y', '-i', video_path,
        '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception("FFmpeg Error:\n" + result.stderr)
    return audio_path

@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/transcribe", methods=["POST"])
# def transcribe():
#     if 'audio' not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     file = request.files['audio']
#     filename = f"uploads/{uuid.uuid4()}.webm"
#     audio_filename = filename.replace(".webm", ".wav")

#     os.makedirs("uploads", exist_ok=True)
#     file.save(filename)

#     try:
#         extract_audio_ffmpeg(filename, audio_filename)
#         result = model.transcribe(audio_filename)

#         with open("transcription.txt", "w", encoding="utf-8") as f:
#             f.write(result["text"])

#         return jsonify({"transcription": result["text"]})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         os.remove(filename)
#         if os.path.exists(audio_filename):
#             os.remove(audio_filename)


@app.route("/transcribe", methods=["POST"])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['audio']
    filename = f"uploads/{uuid.uuid4()}.webm"
    audio_filename = filename.replace(".webm", ".wav")

    os.makedirs("uploads", exist_ok=True)
    file.save(filename)

    try:
        extract_audio_ffmpeg(filename, audio_filename)
        result = model.transcribe(audio_filename)

        # Save transcription to file
        with open("transcription.txt", "w", encoding="utf-8") as f:
            f.write(result["text"])

        # 🔥 Call the fine-tuned model
        vertex_output = call_vertex_model()

        # Return both transcription and model output
        return jsonify({
            "transcription": result["text"],
            "vertex_output": vertex_output
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(filename)
        if os.path.exists(audio_filename):
            os.remove(audio_filename)

if __name__ == "__main__":
    app.run(debug=True)



# from flask import Flask, request, jsonify, render_template
# import os
# import whisper
# import subprocess
# import uuid

# app = Flask(__name__)
# model = whisper.load_model("base")  # Load once at startup

# def extract_audio_ffmpeg(video_path, audio_path):
#     cmd = [
#         'ffmpeg', '-y', '-i', video_path,
#         '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', audio_path
#     ]
#     result = subprocess.run(cmd, capture_output=True, text=True)
#     if result.returncode != 0:
#         raise Exception("FFmpeg Error:\n" + result.stderr)
#     return audio_path

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/transcribe", methods=["POST"])
# def transcribe():
#     if 'audio' not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     file = request.files['audio']
#     filename = f"uploads/{uuid.uuid4()}.webm"
#     audio_filename = filename.replace(".webm", ".wav")

#     os.makedirs("uploads", exist_ok=True)
#     file.save(filename)

#     try:
#         extract_audio_ffmpeg(filename, audio_filename)
#         result = model.transcribe(audio_filename)
#         return jsonify({"transcription": result["text"]})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         os.remove(filename)
#         if os.path.exists(audio_filename):
#             os.remove(audio_filename)

# if __name__ == "__main__":
#     app.run(debug=True)