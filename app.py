from flask import Flask, request, jsonify
import requests
import re
import os

app = Flask(__name__)

# API Key Railway se lega
API_KEY = os.getenv("sk-fe7e909d5484410992a8b2d0aac1b84a")

def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

def ask_ai(prompt):
    url = "https://api.deepseek.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are Vasudev, a wise and helpful AI assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        return clean_text(reply)

    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/')
def home():
    return "Vasudev AI Server Running 🚀"

@app.route('/ask', methods=['GET'])
def ask():
    user_msg = request.args.get('msg')

    if not user_msg:
        return jsonify({"error": "No message"}), 400

    reply = ask_ai(user_msg)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
