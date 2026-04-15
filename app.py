from flask import Flask, render_template, jsonify
import sqlite3
from parse_logs import parse_logs   # Import parser

app = Flask(__name__)

DB_FILE = "cowrie_logs.db"


# ==========================
# Database connection import database 
# ==========================
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================
# Main Page of Dashboard
# ==========================
@app.route("/")
def index():
    return render_template("index.html")


# ==========================
# Logs api 
# ==========================
@app.route("/logs")
def logs_api():
    parse_logs()   # 🔥 Automatically parse new logs

    conn = get_db_connection()

    rows = conn.execute("""
        SELECT timestamp, src_ip, username, password, command
        FROM attacks
        ORDER BY timestamp DESC
        LIMIT 15
    """).fetchall()

    conn.close()

    return jsonify([
        {
            "timestamp": r["timestamp"],
            "src_ip": r["src_ip"],
            "username": r["username"],
            "password": r["password"],
            "command": r["command"]
        } for r in rows
    ])


# ==========================
# Top stats function
# ==========================
def top_stats(field: str, limit: int = 5):
    allowed = {
        "username": "username",
        "ip": "src_ip",
        "password": "password",
        "command": "command"
    }

    if field not in allowed:
        return {"labels": [], "values": []}

    col = allowed[field]

    parse_logs()   # 🔥 Keep stats updated

    conn = get_db_connection()

    rows = conn.execute(f"""
        SELECT {col} AS item, COUNT(*) AS cnt
        FROM attacks
        WHERE {col} IS NOT NULL
          AND TRIM({col}) != ''
          AND {col} != 'None'
        GROUP BY {col}
        ORDER BY cnt DESC
        LIMIT ?
    """, (limit,)).fetchall()

    conn.close()

    labels = [r["item"] for r in rows]
    values = [r["cnt"] for r in rows]

    return {"labels": labels, "values": values}


# ==========================
# Stats route field 
# ==========================
@app.route("/stats/<field>")
def stats(field):
    return jsonify(top_stats(field))


# ==========================
# Timeline histogram code
# ==========================
@app.route("/stats/timeline")
def timeline():
    parse_logs()   # 🔥 Keep timeline updated

    conn = get_db_connection()

    rows = conn.execute("""
        SELECT strftime('%Y-%m-%d %H:00', timestamp) AS hour,
               COUNT(*) AS cnt
        FROM attacks
        GROUP BY hour
        ORDER BY hour ASC
    """).fetchall()

    conn.close()

    labels = [r["hour"] for r in rows]
    values = [r["cnt"] for r in rows]

    return jsonify({
        "labels": labels,
        "values": values
    })


# ==========================
# App run code
# ==========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
