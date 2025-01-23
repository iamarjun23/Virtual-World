import os
import re
import threading
from flask import Flask, send_from_directory, jsonify, request
from gtts import gTTS
import time
import hashlib

app = Flask(__name__)
directory_path = os.path.dirname(os.path.abspath(__file__))
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
 # Add this to the imports if not already present

@app.route("/generate_audio", methods=["POST"])
def generate_audio():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        text = data.get("text", "").strip()
        decibel_value = data.get("decibelValue", None)

        # Log the input text and decibel value for debugging
        print(f"Received text for TTS: {text}")
        print(f"Received decibel value: {decibel_value}")

        # Clean the object name (remove underscores and numbers)
        cleaned_text = clean_object_name(text)

        # If no text is provided, return an error
        if not cleaned_text:
            print("Error: Text input is empty")
            return jsonify({"error": "Text input is empty"}), 400

        # Ensure the directory exists
        if not os.path.exists(AUDIO_FOLDER):
            os.makedirs(AUDIO_FOLDER)

        # Generate a short, safe filename
        hash_value = hashlib.md5((cleaned_text + str(decibel_value)).encode()).hexdigest()[:8]  # Create a hash for uniqueness
        audio_filename = f"audio_{hash_value}.mp3"
        audio_path = os.path.join(AUDIO_FOLDER, audio_filename)

        # Log the audio path for debugging
        print(f"Saving TTS audio to: {audio_path}")

        # Use decibel value to control TTS settings
        # For simplicity, map decibelValue to speed
        if decibel_value:
            try:
                decibel_value = float(decibel_value)
                if decibel_value < 50:
                    slow = True  # Lower decibels -> slower speech
                else:
                    slow = False  # Higher decibels -> faster speech
            except ValueError:
                print("Invalid decibel value. Using default speed.")
                slow = False
        else:
            slow = False  # Default speed if decibelValue is not provided

        # Convert text to speech and save the file
        tts = gTTS(text=cleaned_text, lang="en", slow=slow)
        tts.save(audio_path)

        # Start a background thread to delete the audio file after 2 minutes
        threading.Thread(target=delete_audio_file_after_delay, args=(audio_path, 120)).start()

        # Log the success and file URL
        audio_url = f"/audio/{audio_filename}"  # Assuming the audio folder is served publicly
        print(f"Audio file successfully created: {audio_url}")
        return jsonify({"audio_url": audio_url}), 200

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500



# Serve audio files from the audio directory
@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename)

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

# Cleanup endpoint to delete all audio files
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

# Endpoint to serve object_descriptions.json
@app.route('/model-1/object_descriptions.json')
def serve_descriptions():
    # Send the file from the directory where app.py is located
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'object_descriptions.json')

if __name__ == "__main__":
    app.run(debug=True)
