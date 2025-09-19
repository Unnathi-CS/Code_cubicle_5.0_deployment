# Slack Ingestion Pathway Project

## Setup Instructions

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd code_cubicle_5.0
```

### 2. Install Python

Download and install Python 3.10+ from [python.org](https://www.python.org/downloads/).

### 3. Create and Activate a Virtual Environment (Recommended)

```sh
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 4. Install Dependencies

```sh
pip install flask python-dotenv pathway
```

### 5. Set Up Environment Variables

Create a `.env` file in the project root:
```
SLACK_BOT_TOKEN=your-slack-bot-token-here
```

### 6. Start the Flask Server

```sh
python slack_pathway/src/app.py
```

### 7. Expose Local Server to the Internet

Download and install [ngrok](https://ngrok.com/download).

```sh
ngrok http 5000
```
Copy the HTTPS forwarding URL.

### 8. Configure Slack App

- Go to [Slack API Apps](https://api.slack.com/apps).
- Set your event request URL to `https://<ngrok-url>/slack/events`.
- Add necessary scopes (e.g., `chat:write`, `channels:history`, etc.).
- Install the app to your workspace.

### 9. Test the Endpoint

Use curl or Postman to send test events. Slack will send a `url_verification` event when you set the endpoint.

### 10. Monitor Logs

Check your terminal for incoming events and messages.

---

You are now ready to develop and run the project!

