from flask import Flask, render_template, request, jsonify
from engine import Chatbot

app = Flask(__name__)
bot = Chatbot()

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    resp = bot.respond(message)
    return jsonify(resp)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
