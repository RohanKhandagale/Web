import os
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DATABASE = Path(os.environ.get("DATABASE_PATH", BASE_DIR / "instance" / "enquiries.db"))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "local-development-key-change-before-deploy")
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024


def get_db():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS enquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                service TEXT,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/contact")
def contact():
    # Simple honeypot to discard basic automated spam.
    if request.form.get("website", "").strip():
        return redirect(url_for("home") + "#contact")

    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    service = request.form.get("service", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not phone or not message:
        flash("Please fill in your name, phone number, and project message.", "error")
        return redirect(url_for("home") + "#contact")

    if len(name) > 100 or len(phone) > 20 or len(email) > 120 or len(service) > 80 or len(message) > 2000:
        flash("One or more fields are too long. Please shorten your message and try again.", "error")
        return redirect(url_for("home") + "#contact")

    if not re.fullmatch(r"[0-9+() .-]{7,20}", phone):
        flash("Please enter a valid phone number.", "error")
        return redirect(url_for("home") + "#contact")

    if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        flash("Please enter a valid email address.", "error")
        return redirect(url_for("home") + "#contact")

    with get_db() as db:
        db.execute(
            """INSERT INTO enquiries (name, phone, email, service, message, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (name, phone, email, service, message, datetime.now(timezone.utc).isoformat()),
        )

    flash("Thank you! Your enquiry has been received. The Shravani Construction team will contact you.", "success")
    return redirect(url_for("home") + "#contact")


@app.errorhandler(413)
def request_too_large(_error):
    flash("Your submission is too large. Please keep the message under 2,000 characters.", "error")
    return redirect(url_for("home") + "#contact")


init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=False)
