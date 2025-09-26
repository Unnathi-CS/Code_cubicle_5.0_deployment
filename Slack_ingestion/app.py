import os
from urllib.parse import urlparse

from flask import Flask, redirect, render_template, session, url_for, request
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

    app.config.update(
        GOOGLE_CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID"),
        GOOGLE_CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET"),
        SERVER_NAME=os.getenv("SERVER_NAME"),  # optional for url_for external urls
        PREFERRED_URL_SCHEME=os.getenv("PREFERRED_URL_SCHEME", "https"),
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=False,  # set True if serving over HTTPS in production
    )

    oauth = OAuth(app)
    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={
            "scope": "openid email profile",
        },
    )

    @app.route("/")
    def login_page():
        if session.get("user"):
            return redirect(url_for("dashboard"))
        return render_template("login.html")

    @app.route("/login")
    def login():
        redirect_uri = url_for("auth_callback", _external=True)
        # Force Google account chooser every time
        return oauth.google.authorize_redirect(redirect_uri, prompt="select_account")

    @app.route("/callback")
    def auth_callback():
        token = oauth.google.authorize_access_token()
        userinfo = None
        # Newer Authlib requires a nonce for parse_id_token; prefer userinfo endpoint
        try:
            userinfo = oauth.google.parse_id_token(token)
        except Exception:
            userinfo = None
        if not userinfo:
            resp = oauth.google.get("https://openidconnect.googleapis.com/v1/userinfo")
            userinfo = resp.json() if resp else None

        if not userinfo:
            return redirect(url_for("login_page"))

        session["user"] = {
            "name": userinfo.get("name"),
            "email": userinfo.get("email"),
            "picture": userinfo.get("picture"),
        }
        return redirect(url_for("dashboard"))

    @app.route("/dashboard")
    def dashboard():
        user = session.get("user")
        if not user:
            return redirect(url_for("login_page"))
        return render_template("dashboard.html", user=user)

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login_page"))

    @app.context_processor
    def inject_user():
        return {"session_user": session.get("user")}

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
