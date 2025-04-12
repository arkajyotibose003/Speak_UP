from flask import Flask, request, jsonify, send_file, render_template
import pyttsx3
import tempfile
import os

app = Flask(__name__)
spdval = 120  # Default speed

@app.route('/')
def index():
    return render_template('new_index.html', spdval=spdval)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get("Text", "")
    speed = data.get("newval", 120)

    if not text.strip():
        return jsonify({"error": "Text is empty"}), 400

    # Set up TTS engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')#New add
    engine.setProperty('voice', voices[1].id)#New add
    engine.setProperty('rate', speed)

    # Generate temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        filename = tmpfile.name

    # Save to WAV file
    engine.save_to_file(text, filename)
    engine.runAndWait()

    # Return WAV as file response
    return send_file(
        filename,
        mimetype='audio/wav',
        as_attachment=False
    )
#New addition 
@app.route("/output")
def output():
    return render_template("output.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)