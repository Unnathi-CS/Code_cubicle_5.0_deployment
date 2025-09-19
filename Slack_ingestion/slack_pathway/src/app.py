from flask import Flask, request
import os
from dotenv import load_dotenv
from stream import push_message
from utils import is_valid_message

load_dotenv()

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
@app.route("/slack/events/", methods=["POST"])
def slack_events():
    # Ensure JSON payload
    if not request.is_json:
        return {"error": "Unsupported Media Type"}, 415

    data = request.get_json()
    print("Incoming payload:", data)

    # Slack URL verification
    if data.get("type") == "url_verification":
        # Must return the raw challenge string
        return data["challenge"], 200, {"Content-Type": "text/plain"}

    # Handle new message events
    if "event" in data and data["event"].get("type") == "message":
        msg = {
            "user": data["event"].get("user"),
            "text": data["event"].get("text"),
            "ts": data["event"].get("ts")
        }

        # Filter invalid messages
        if is_valid_message(msg):
            push_message(msg)
            print("Message pushed:", msg)
        else:
            print("Filtered invalid message:", msg)

    return {"ok": True}

if __name__ == "__main__":
    # Listen on all interfaces so ngrok can reach it
    app.run(host="0.0.0.0", port=5000)
