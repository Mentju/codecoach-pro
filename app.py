from flask import Flask, jsonify, request, render_template, send_from_directory
import sqlite3
import os
from pathlib import Path
from datetime import datetime
import io
import contextlib

app = Flask(__name__)
DB_PATH = Path("codecoach_pro.db")

ROADMAP = [
    {"week": 1, "track": "Python", "topic": "Variables and conditionals", "goal": "Build calculator-style programs."},
    {"week": 2, "track": "JavaScript", "topic": "Variables and browser console", "goal": "Understand JS syntax and output."},
    {"week": 3, "track": "Both", "topic": "Loops and functions", "goal": "Solve repeated-task problems."},
    {"week": 4, "track": "Both", "topic": "Lists, arrays, dictionaries, objects", "goal": "Store and organize data."},
    {"week": 5, "track": "SQL", "topic": "SELECT, WHERE, ORDER BY", "goal": "Query database records."},
    {"week": 6, "track": "SQL", "topic": "GROUP BY, INSERT, UPDATE, DELETE", "goal": "Summarize and modify data."},
    {"week": 7, "track": "Web", "topic": "HTML and CSS", "goal": "Build clean pages and forms."},
    {"week": 8, "track": "JavaScript", "topic": "DOM and events", "goal": "Make interactive web apps."},
    {"week": 9, "track": "Python", "topic": "Flask routes", "goal": "Build backend routes and APIs."},
    {"week": 10, "track": "Full Stack", "topic": "SQLite + APIs", "goal": "Connect frontend, backend, and database."},
    {"week": 11, "track": "Projects", "topic": "Portfolio project 1", "goal": "Build a student success app."},
    {"week": 12, "track": "Projects", "topic": "Portfolio project 2", "goal": "Build a business dashboard."},
]

CHALLENGES = [
    ("Python", "Print your name", "Use print() to display your name.", "print("),
    ("Python", "Add two numbers", "Create two variables and print their sum.", "+"),
    ("Python", "Loop 1 to 10", "Use a loop to print numbers 1 through 10.", "for"),
    ("Python", "Function practice", "Write a function named add that returns a sum.", "def add"),
    ("JavaScript", "Console greeting", "Use console.log to print a greeting.", "console.log"),
    ("JavaScript", "Button logic", "Write JS that changes page text when a button is clicked.", "addEventListener"),
    ("JavaScript", "Array loop", "Create an array and loop through it.", "for"),
    ("SQL", "Select all students", "Write a query to select everything from students.", "SELECT * FROM students"),
    ("SQL", "Filter by grade", "Select students with grade >= 85.", "WHERE"),
    ("SQL", "Group spending", "Group expenses by category.", "GROUP BY"),
    ("Full Stack", "Create an API route", "Explain or build a route that returns JSON.", "json"),
    ("Full Stack", "Portfolio README", "Write a README explaining one project.", "README"),
]

PROJECTS = [
    {
        "title": "Student Success App",
        "skills": "Python, JavaScript, SQL, Flask",
        "description": "Track assignments, due dates, grades, and study sessions.",
        "features": ["Add assignments", "Track due dates", "Calculate grades", "Store data in SQLite"]
    },
    {
        "title": "Business Dashboard",
        "skills": "Python, SQL, JavaScript",
        "description": "Upload or enter sales data and display totals, averages, and trends.",
        "features": ["Enter sales", "Query totals", "Show summaries", "Export report"]
    },
    {
        "title": "Budget Tracker",
        "skills": "JavaScript, SQL, Flask",
        "description": "Track income, expenses, and spending categories.",
        "features": ["Add expenses", "Group by category", "View monthly totals", "Find money leaks"]
    },
    {
        "title": "Coding Habit Tracker",
        "skills": "Full Stack",
        "description": "A habit tracker specifically for learning to code.",
        "features": ["Daily sessions", "Streaks", "Language totals", "Challenge completion"]
    }
]

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        language TEXT NOT NULL,
        topic TEXT NOT NULL,
        minutes INTEGER NOT NULL,
        notes TEXT,
        created_at TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS challenges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        language TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        expected TEXT NOT NULL,
        completed INTEGER DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS portfolio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        status TEXT NOT NULL,
        notes TEXT,
        created_at TEXT NOT NULL
    )
    """)

    cur.execute("SELECT COUNT(*) AS count FROM challenges")
    if cur.fetchone()["count"] == 0:
        cur.executemany(
            "INSERT INTO challenges (language, title, description, expected) VALUES (?, ?, ?, ?)",
            CHALLENGES
        )

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        language TEXT NOT NULL,
        grade INTEGER NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        amount REAL NOT NULL
    )
    """)

    cur.execute("SELECT COUNT(*) AS count FROM students")
    if cur.fetchone()["count"] == 0:
        cur.executemany(
            "INSERT INTO students (name, language, grade) VALUES (?, ?, ?)",
            [
                ("Brandon", "Python", 95),
                ("Alex", "JavaScript", 88),
                ("Mia", "SQL", 91),
                ("Jordan", "Python", 78),
                ("Taylor", "JavaScript", 84)
            ]
        )

    cur.execute("SELECT COUNT(*) AS count FROM expenses")
    if cur.fetchone()["count"] == 0:
        cur.executemany(
            "INSERT INTO expenses (category, amount) VALUES (?, ?)",
            [
                ("Food", 45.25),
                ("Food", 18.10),
                ("Gas", 52.00),
                ("School", 80.00),
                ("Subscriptions", 15.99),
                ("Subscriptions", 12.99)
            ]
        )

    conn.commit()
    conn.close()


@app.route("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json")

@app.route("/service-worker.js")
def service_worker():
    return send_from_directory("static", "service-worker.js")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/roadmap")
def roadmap():
    return jsonify(ROADMAP)

@app.route("/api/projects")
def projects():
    return jsonify(PROJECTS)

@app.route("/api/challenges")
def challenges():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM challenges ORDER BY id").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/api/challenges/<int:challenge_id>/toggle", methods=["POST"])
def toggle_challenge(challenge_id):
    conn = get_connection()
    row = conn.execute("SELECT completed FROM challenges WHERE id=?", (challenge_id,)).fetchone()
    if row is None:
        conn.close()
        return jsonify({"error": "Challenge not found"}), 404

    new_value = 0 if row["completed"] else 1
    conn.execute("UPDATE challenges SET completed=? WHERE id=?", (new_value, challenge_id))
    conn.commit()
    conn.close()
    return jsonify({"id": challenge_id, "completed": new_value})

@app.route("/api/sessions", methods=["GET", "POST"])
def sessions():
    conn = get_connection()

    if request.method == "POST":
        data = request.get_json()
        language = data.get("language", "").strip()
        topic = data.get("topic", "").strip()
        notes = data.get("notes", "").strip()

        try:
            minutes = int(data.get("minutes", 0))
        except ValueError:
            conn.close()
            return jsonify({"error": "Minutes must be a number"}), 400

        if not language or not topic or minutes <= 0:
            conn.close()
            return jsonify({"error": "Language, topic, and positive minutes are required"}), 400

        conn.execute(
            "INSERT INTO sessions (language, topic, minutes, notes, created_at) VALUES (?, ?, ?, ?, ?)",
            (language, topic, minutes, notes, datetime.now().isoformat(timespec="seconds"))
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Session saved"}), 201

    rows = conn.execute("SELECT * FROM sessions ORDER BY created_at DESC").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/api/stats")
def stats():
    conn = get_connection()
    total_minutes = conn.execute("SELECT COALESCE(SUM(minutes), 0) AS total FROM sessions").fetchone()["total"]
    by_language = conn.execute("""
        SELECT language, SUM(minutes) AS total_minutes
        FROM sessions
        GROUP BY language
        ORDER BY total_minutes DESC
    """).fetchall()
    completed = conn.execute("SELECT COUNT(*) AS count FROM challenges WHERE completed=1").fetchone()["count"]
    total_challenges = conn.execute("SELECT COUNT(*) AS count FROM challenges").fetchone()["count"]
    portfolio_count = conn.execute("SELECT COUNT(*) AS count FROM portfolio").fetchone()["count"]
    conn.close()

    return jsonify({
        "total_minutes": total_minutes,
        "by_language": [dict(row) for row in by_language],
        "completed_challenges": completed,
        "total_challenges": total_challenges,
        "portfolio_count": portfolio_count
    })

@app.route("/api/run-python", methods=["POST"])
def run_python():
    data = request.get_json()
    code = data.get("code", "")

    blocked = ["import", "open(", "exec(", "eval(", "__", "os.", "subprocess", "socket", "shutil", "pathlib"]
    lowered = code.lower()

    for word in blocked:
        if word in lowered:
            return jsonify({
                "ok": False,
                "output": f"Blocked for safety: avoid using {word} in the learning sandbox."
            })

    output = io.StringIO()
    safe_globals = {
        "__builtins__": {
            "print": print,
            "range": range,
            "len": len,
            "sum": sum,
            "min": min,
            "max": max,
            "round": round,
            "str": str,
            "int": int,
            "float": float,
            "list": list,
            "dict": dict,
            "set": set,
            "enumerate": enumerate
        }
    }

    try:
        with contextlib.redirect_stdout(output):
            exec(code, safe_globals, {})
        return jsonify({"ok": True, "output": output.getvalue() or "Code ran with no printed output."})
    except Exception as e:
        return jsonify({"ok": False, "output": f"{type(e).__name__}: {e}"})

@app.route("/api/run-sql", methods=["POST"])
def run_sql():
    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"ok": False, "error": "Enter a SQL query."}), 400

    lowered = query.lower()
    blocked = ["drop", "alter", "attach", "detach", "pragma"]

    if any(word in lowered for word in blocked):
        return jsonify({"ok": False, "error": "That SQL command is blocked in the learning sandbox."}), 400

    conn = get_connection()

    try:
        cur = conn.cursor()
        cur.execute(query)

        if lowered.startswith("select"):
            rows = cur.fetchall()
            columns = [description[0] for description in cur.description]
            conn.close()
            return jsonify({
                "ok": True,
                "columns": columns,
                "rows": [list(row) for row in rows],
                "message": f"{len(rows)} row(s) returned."
            })

        conn.commit()
        affected = cur.rowcount
        conn.close()
        return jsonify({
            "ok": True,
            "columns": [],
            "rows": [],
            "message": f"Query ran successfully. Rows affected: {affected}"
        })
    except Exception as e:
        conn.close()
        return jsonify({"ok": False, "error": f"{type(e).__name__}: {e}"}), 400

@app.route("/api/check-answer", methods=["POST"])
def check_answer():
    data = request.get_json()
    challenge_id = int(data.get("challenge_id", 0))
    answer = data.get("answer", "")

    conn = get_connection()
    row = conn.execute("SELECT expected FROM challenges WHERE id=?", (challenge_id,)).fetchone()
    conn.close()

    if row is None:
        return jsonify({"ok": False, "message": "Challenge not found."})

    expected = row["expected"].lower()
    if expected in answer.lower():
        return jsonify({"ok": True, "message": "Good job. Your answer includes the key idea."})

    return jsonify({
        "ok": False,
        "message": f"Not quite. Try including this key idea: {row['expected']}"
    })

@app.route("/api/portfolio", methods=["GET", "POST"])
def portfolio():
    conn = get_connection()

    if request.method == "POST":
        data = request.get_json()
        title = data.get("title", "").strip()
        status = data.get("status", "Idea").strip()
        notes = data.get("notes", "").strip()

        if not title:
            conn.close()
            return jsonify({"error": "Project title is required"}), 400

        conn.execute(
            "INSERT INTO portfolio (title, status, notes, created_at) VALUES (?, ?, ?, ?)",
            (title, status, notes, datetime.now().isoformat(timespec="seconds"))
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Portfolio project saved"}), 201

    rows = conn.execute("SELECT * FROM portfolio ORDER BY created_at DESC").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# Initialize the SQLite database when the app starts.
init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
