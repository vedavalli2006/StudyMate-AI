from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
import re

# App Configuration

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

print(BASE_DIR)
print(DB_PATH)

app = Flask(__name__)
app.secret_key = "studymate_secret"


# Database Initialization

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
     
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        note TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


# Home Page

@app.route("/")
def home():
    return render_template("index.html")

# About Page

@app.route("/about")
def about():
    return render_template("about.html")


# Login

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
    "SELECT * FROM users WHERE email=?",
    (email,)
     )

        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            session["user_email"] = user[2]

            flash("Login Successful!")
            return redirect(url_for("dashboard"))

        else:
            flash("Invalid Email or Password!")

    return render_template("login.html")


# Signup

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            flash("Email already registered! Please use another email.")
            conn.close()
            return redirect(url_for("signup"))

        # Insert new user
        cursor.execute(
            "INSERT INTO users(name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        

        conn.commit()
        conn.close()

        flash("Registration Successful!")
        return redirect(url_for("login"))

    return render_template("signup.html")


# Dashboard

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        flash("Please login first.")
        return redirect(url_for("login"))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    
    cursor.execute("SELECT COUNT(*) FROM notes")
    total_notes = cursor.fetchone()[0]

    conn.close()

    progress = min(total_notes * 10, 100)

    return render_template(
        "dashboard.html",
        username=session["user_name"],
        total_notes=total_notes,
        progress=progress
    )


# Notes

@app.route("/notes", methods=["GET", "POST"])
def notes():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if request.method == "POST":

        note = request.form["note"]

        cursor.execute(
            "INSERT INTO notes(note) VALUES(?)",
            (note,)
        )

        conn.commit()

    cursor.execute("SELECT * FROM notes")
    all_notes = cursor.fetchall()
    conn.close()

    return render_template("notes.html", notes=all_notes)


# Delete Note

@app.route("/delete_note/<int:id>")
def delete_note(id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("notes"))


# AI Tools

@app.route("/ai-tools")
def ai_tools():
    return render_template("ai-tools.html")


# Progress

@app.route("/progress")
def progress():

    if "user_id" not in session:
        flash("Please login first.")
        return redirect(url_for("login"))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM notes")
    total_notes = cursor.fetchone()[0]

    conn.close()

    
    progress = min(total_notes * 10, 100)

    return render_template(
        "progress.html",
        total_notes=total_notes,
        progress=progress
    )


# Contact

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO contacts(name, email, message) VALUES(?,?,?)",
            (name, email, message)
        )

        conn.commit()
        conn.close()

        flash("Message sent successfully!")
        return redirect(url_for("contact"))

    return render_template("contact.html")

# Logout

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully!")

    return redirect(url_for("login"))


# Initialize Database

init_db()


# Run App

if __name__ == "__main__":
    app.run(debug=True)