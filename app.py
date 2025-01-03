import os
import re
import threading
from flask import Flask, send_from_directory, jsonify, request, send_file
from gtts import gTTS
import time

app = Flask(__name__)

# Define the directory to save the audio files
AUDIO_FOLDER = os.path.join(os.getcwd(), 'audio')
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)

# Function to clean the object name (remove underscores and numbers)
def clean_object_name(object_name):
    cleaned_name = re.sub(r'[_\d]', '', object_name)
    return cleaned_name.strip()

# Function to delete the audio file after a delay
def delete_audio_file_after_delay(file_path, delay=120):
    time.sleep(delay)  # Wait for the specified delay (in seconds)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted audio file: {file_path}")

# Home route (serving index.html from the root directory)
@app.route("/")
def index():
    return send_from_directory(os.getcwd(), 'index.html')

# API for text-to-speech conversion
@app.route("/generate_audio", methods=["POST"])
def generate_audio():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        text = data.get("text", "").strip()

        # Clean the object name (remove underscores and numbers)
        cleaned_text = clean_object_name(text)

        # If no text is provided, return an error
        if not cleaned_text:
            return jsonify({"error": "Text input is empty"}), 400

        # Create a temporary file to save the audio
        audio_filename = f"{cleaned_text}.mp3"
        audio_path = os.path.join(AUDIO_FOLDER, audio_filename)

        # Convert text to speech and save the file
        tts = gTTS(text=cleaned_text, lang="en", slow=False)
        tts.save(audio_path)

        # Start a background thread to delete the audio file after 2 minutes
        threading.Thread(target=delete_audio_file_after_delay, args=(audio_path, 120)).start()

        # Send the audio file to the client
        return send_file(audio_path, mimetype="audio/mpeg", as_attachment=False)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Endpoint to receive the user data (condition, decibel, clicked object)
@app.route("/submit_data", methods=["POST"])
def submit_data():
    try:
        data = request.get_json()
        condition = data.get("condition", "Not Specified")
        decibel_value = data.get("decibelValue", "Not Provided")
        clicked_object = data.get("clickedObject", "None")

        # Log or save the data as needed
        print(f"Condition: {condition}, Decibel: {decibel_value}, Clicked Object: {clicked_object}")
        return jsonify({"status": "success", "data": data})

    except Exception as e:
        print(f"Error submitting data: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Serve CSS and other static files from the root directory
@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(os.getcwd(), filename)

# Clean up the audio files after they are played
@app.route('/cleanup', methods=["POST"])
def cleanup():
    try:
        for filename in os.listdir(AUDIO_FOLDER):
            file_path = os.path.join(AUDIO_FOLDER, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return jsonify({"status": "success", "message": "Audio files deleted"}), 200
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
