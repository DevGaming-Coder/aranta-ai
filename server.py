import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

API_KEY = "AQ.Ab8RN6IqJ_8Uica4Y2u1vd54kuSxkXRbfqNubAZ37cZw7YfTqw"
client = genai.Client(api_key=API_KEY)

chat = client.chats.create(
    model="gemini-3.6-flash",
    config={
        "system_instruction": "Your name is Aranta. You are a professional, friendly, and helpful AI assistant."
    }
)

@app.route("/chat", methods=["POST"])
def handle_chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        response = chat.send_message(user_message)
        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)