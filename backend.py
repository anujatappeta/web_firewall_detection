from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend server running"

@app.route("/login")
def login():
    user = request.args.get("user")

    # Vulnerable SQL query (for testing WAF)
    query = f"SELECT * FROM users WHERE id = {user}"

    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    try:
        result = cursor.execute(query).fetchall()
        return str(result)
    except:
        return "Database error"

app.run(port=5001)