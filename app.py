import os
import tempfile

from flask import Flask, jsonify, render_template, request, send_file
from gtts import gTTS
from pydub import AudioSegment

app = Flask(__name__)

# Home route
@app.route("/")
def index():
    return render_template("index.html")

# New route for the text-to-speech page
@app.route("/speech")
def speech():
    return render_template("speech.html")

# API for text-to-speech conversion
@app.route("/convert", methods=["POST"])
def convert():
    try:
        # Parse JSON data
        data = request.get_json()
        text = data.get("text", "").strip()
        volume = int(data.get("volume", 0))

        if not text:
            return jsonify({"error": "Text input is empty"}), 400

        # Create temporary directory for file processing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = os.path.join(temp_dir, "output.mp3")

            # Convert text to speech and save to a file
            tts = gTTS(text=text, lang="en", slow=False)
            tts.save(temp_file)

            # Adjust volume
            audio = AudioSegment.from_mp3(temp_file)
            adjusted_audio = audio + volume
            adjusted_audio.export(temp_file, format="mp3")

            # Send the adjusted audio file to the client
            return send_file(temp_file, mimetype="audio/mpeg", as_attachment=False)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
