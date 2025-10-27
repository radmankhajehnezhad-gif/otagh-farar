# main.py
from flask import Flask, render_template, request, jsonify
import os
import openai

app = Flask(__name__, static_folder="static", template_folder="static")

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("لطفاً متغیر محیطی OPENAI_API_KEY را تنظیم کن.")
openai.api_key = OPENAI_KEY

PUBLIC_PASSWORD = os.getenv("PUBLIC_PASSWORD")  # optional

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    password = data.get("password", None)

    if not message:
        return jsonify({"error": "پیام خالی است"}), 400

    if PUBLIC_PASSWORD:
        if not password or password != PUBLIC_PASSWORD:
            return jsonify({"error": "رمز نامعتبر"}), 401

    system_prompt = ("You are a helpful assistant. Reply in Persian (Farsi). "
                     "Do NOT repeat the user's exact question back. Be concise and clear.")

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=400,
            temperature=0.6,
        )
        answer = resp.choices[0].message.content.strip()
        return jsonify({"response": answer})
    except Exception as e:
        print("OpenAI error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
