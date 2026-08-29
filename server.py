import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from google import genai

app = Flask(__name__, static_folder='.')
CORS(app)

# Securely fetch API Key from Environment Variables
API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/chat", methods=["POST"])
def handle_chat():
    try:
        if not API_KEY:
            return jsonify({"error": "GEMINI_API_KEY is not set in Environment Variables."}), 500

        client = genai.Client(api_key=API_KEY)
        data = request.json
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        chat = client.chats.create(
            model="gemini-3.6-flash",
            config={
                "system_instruction": "Your name is Aranta. You are a professional, friendly, and helpful AI assistant."
            }
        )

        response = chat.send_message(user_message)
        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
