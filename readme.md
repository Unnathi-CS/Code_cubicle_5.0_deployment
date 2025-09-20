# RAG + Pathway Powered Chatbot

Hackathon Wall is an intelligent chatbot platform built using **Flask**, **RAG (Retrieval-Augmented Generation)**, and **Pathway**.  
It allows users to interact with an AI assistant that retrieves relevant information from Slack channels and generates context-aware responses in real time.

---

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/UnnathiCS/Code_Cubicle_5.0_RAG_pathway.git
cd Code_Cubicle_5.0_RAG_pathway
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

all the commands to be run on WSL terminal for pathway to work
<img width="1204" height="472" alt="image" src="https://github.com/user-attachments/assets/982bd999-6531-4ad0-8734-f13682d4487f" />

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

```
python slack_pathway/src/app.py
```

---

## Slack Integration Setup

### 1. Expose Local Server to the Internet

Download and install [ngrok](https://ngrok.com/download).
<img width="1064" height="648" alt="image" src="https://github.com/user-attachments/assets/9409479d-ce7a-4389-94df-7dd0935a59d6" />

```sh
ngrok http 5000
```

Copy the HTTPS forwarding URL.
<img width="1225" height="658" alt="image" src="https://github.com/user-attachments/assets/56b228dd-dbff-477b-8eac-bb9a642da050" />

### 2. Configure Slack App

- Go to [Slack API Apps](https://api.slack.com/apps).
- Set your event request URL to `https://<ngrok-url>/slack/events`.
- Add necessary scopes (e.g., `chat:write`, `channels:history`, etc.).
- <img width="1461" height="766" alt="image" src="https://github.com/user-attachments/assets/5bdd878d-c437-4352-86a8-d5be3efa7692" />

- Install the app to your workspace.

- <img width="1682" height="771" alt="image" src="https://github.com/user-attachments/assets/f99b8d3f-9635-4257-b537-aff3be578529" />
  <img width="1467" height="636" alt="image" src="https://github.com/user-attachments/assets/ad8c0bda-8cd0-4236-9797-de012031bd26" />

### 3. Test the Endpoint

Use curl or Postman to send test events. Slack will send a `url_verification` event when you set the endpoint.

```sh
curl -X POST http://127.0.0.1:5000/slack/events \
-H "Content-Type: application/json" \
-d '{
  "event": {
    "type": "message",
    "user": "U123456",
    "text": "Hello world!",
    "ts": "1695120000.000"
  }
}'

```

### 4. Monitor Logs

Check your terminal for incoming events and messages.

---

## Running the Application

Start the Flask Backend (API + Frontend)

```sh
python slack_pathway/src/app.py
```

By default, the server runs at : http://127.0.0.1:5000/

- Opening http://127.0.0.1:5000 will show the Landing Page.
- Clicking “Try Me” will open the Chatbot UI.
- Type your queries & the bot will answer, using the real time data.

---

## Demo

[![Watch the video](thumbnail)](video_link)

---

## 💖 Made with Love

Made with ❤️ by She-E-Os

---

