import json
import sqlite3

LOG_FILE = "/home/cowrie/cowrie/var/log/cowrie/cowrie.json"
DB_FILE = "cowrie_logs.db"


def parse_logs():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    session_auth = {}

    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                event = json.loads(line)

                eventid = event.get("eventid")
                session = event.get("session")

                # -----------------------------
                # SUCCESSFUL LOGIN
                # -----------------------------
                if eventid == "cowrie.login.success":
                    session_auth[session] = {
                        "username": event.get("username"),
                        "password": event.get("password")
                    }

                # -----------------------------
                # FAILED LOGIN ATTEMPT
                # -----------------------------
                elif eventid == "cowrie.login.failed":
                    cursor.execute("""
                        INSERT OR IGNORE INTO attacks
                        (timestamp, src_ip, username, password, command, session)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        event.get("timestamp"),
                        event.get("src_ip"),
                        event.get("username"),
                        event.get("password"),
                        "FAILED LOGIN ATTEMPT",
                        session
                    ))

                # -----------------------------
                # COMMAND EXECUTION
                # -----------------------------
                elif eventid == "cowrie.command.input":

                    auth = session_auth.get(session, {})

                    cursor.execute("""
                        INSERT OR IGNORE INTO attacks
                        (timestamp, src_ip, username, password, command, session)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        event.get("timestamp"),
                        event.get("src_ip"),
                        auth.get("username"),
                        auth.get("password"),
                        event.get("input"),
                        session
                    ))

            except json.JSONDecodeError:
                continue
            except Exception as e:
                print("Error parsing line:", e)

    conn.commit()
    conn.close()
