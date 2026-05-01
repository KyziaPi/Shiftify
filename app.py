from flask import Flask, render_template, request, session, redirect, url_for, flash, abort, jsonify
import sqlite3
from os import urandom
import time

# import the game logic to this file
from puzzle_logic import generate_board, is_solved, can_move, move_tile

app = Flask(__name__)
app.secret_key = urandom(24)

leaderboard_db = sqlite3.connect("leaderboard.db")
cursor = leaderboard_db.cursor()

# Check if the table exists
table_name = "easy_scores"
cursor.execute("""
    SELECT name 
    FROM sqlite_master 
    WHERE type='table' AND name=?;
""", (table_name,))
exists = cursor.fetchone()

# Create the tables if it doesn't exist
if not exists:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS easy_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            time REAL,
            tiles_moved INTEGER
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS normal_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            time REAL,
            tiles_moved INTEGER
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hard_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            time REAL,
            tiles_moved INTEGER
        );
    """)

leaderboard_db.close()

modes = {
    "easy": "play/easy",
    "normal": "play/normal",
    "hard": "play/hard"
}


# Menu
@app.route("/")
def menu():
    return render_template(
        "index.html",
        page="menu")


# Instructions
@app.route("/instructions")
def instructions():
    """Instructions here"""
    return render_template("instructions.html")


@app.route("/reshuffle", methods=["POST"])
def reshuffle():
    # Get the mode the user is in
    mode = request.form.get("mode")

    # Validate the mode
    if mode not in modes:
        abort(400, "Invalid mode selected!")

    html = modes[mode]
    # Clear the session to reset everything
    session.clear()

    return redirect(f"/{html}")  # Redirect to the page


@app.route("/play/<mode>", methods=["GET", "POST"])
def play(mode):
    if mode not in ['easy', 'normal', 'hard']:
        return "Invalid mode", 400

    """Game function here"""

    board_widths = {
        'easy': 3,
        'normal': 4,
        'hard': 5
    }

    htmls = {
        'easy': "mode_easy.html",
        'normal': "mode_normal.html",
        'hard': "mode_hard.html"
    }

    if "board" not in session:
        session["board"] = generate_board(board_widths[mode])
        session["mode"] = mode  # For the result page
        session["tiles_moved"] = 0
        session["elapsed_time"] = 0.0

    # check post request and validation
    if request.method == "POST":
        tile = int(request.form.get("tile"))

        if can_move(session["board"], tile):
            move_tile(session["board"], tile)  # Move the tile

            session["tiles_moved"] += 1  # Update counter

            # Start the timer on first tile click
            if not session.get("running", False):
                session["start_time"] = time.time()
                session["running"] = True

            session["elapsed_time"] = time.time() - session["start_time"]  # Update the timer

        if is_solved(session["board"], board_widths[mode]):
            session["running"] = False
            session["solved"] = True
            session["final_time"] = round(session["elapsed_time"], 2)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    "solved": True
                })

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            "board": session["board"],
            "tiles_moved": session["tiles_moved"],
            "elapsed_time": round(session["elapsed_time"], 2)
        })
    else:
        return render_template(htmls[mode],
            board=session["board"])


# Used to update the time
@app.route("/get_timer")
def get_timer():
    """API endpoint to fetch elapsed time"""
    if session.get("running", False):  # Check if the stopwatch is running
        elapsed_time = time.time() - session["start_time"]  # Calculate current elapsed time
    else:
        elapsed_time = session.get("elapsed_time", 0.0)  # Get previously stopped time

    return {
        "elapsed_time": round(elapsed_time, 2),  # Elapsed time
        "running": session.get("running", False)  # Timer status
    }


@app.route("/result")
def result():
    if not session.get("solved"):
        return redirect("/")  # prevent direct access

    text_colors = {
        "easy": "text-success",
        "normal": "text-warning",
        "hard": "text-danger"
    }

    return render_template("result.html",
                           text_color=text_colors[session["mode"]],
                           mode=session["mode"],
                           final_time=session.get("final_time"),
                           tiles_moved=session.get("tiles_moved"))


# Leaderboard (stored in database using sqlite)
@app.route("/leaderboard", methods=["GET", "POST"])
def leaderboard():
    """Leaderboard here"""
    if request.method == "POST":
        username = request.form.get("name").strip()  # Get username from inputfield
        mode = session["mode"]
        final_time = session.get("final_time")
        tiles_moved = session.get("tiles_moved")

        text_colors = {"easy": "text-success", "normal": "text-warning", "hard": "text-danger"}
        text_color = text_colors[mode]

        if not username:
            flash("Please insert your name to submit to leaderboard!")
            return render_template("result.html",
                                   mode=mode, text_color=text_color,
                                   final_time=final_time,
                                   tiles_moved=tiles_moved)

        # input values in the database
        try:
            with sqlite3.connect('leaderboard.db') as conn:
                print(f"Inserting into table: {mode}_scores")
                query = f"INSERT INTO {mode}_scores(username, time, tiles_moved) VALUES(?, ?, ?)"
                scores = (username, final_time, tiles_moved)

                # query to insert score in db
                cur = conn.cursor()
                cur.execute(query, scores)

                # display data inserted
                last_id = cur.lastrowid
                cur.execute(f"SELECT * FROM {mode}_scores WHERE id = ?", (last_id,))
                row = cur.fetchone()
                print(row)

                # commit changes to db
                conn.commit()
        except sqlite3.Error as e:
            print(e)

        # Redirect user to leaderboard
        flash("Added to the leaderboard!")
        return redirect("/leaderboard")

    else:
        conn = sqlite3.connect('leaderboard.db')
        cur = conn.cursor()

        # View tables
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print("Tables:", cur.fetchall())

        # View rows from a specific tables
        cur.execute("SELECT * FROM easy_scores;")  # change 'users' to your table
        rows = cur.fetchall()
        for row in rows:
            print(row)

        cur.execute("SELECT * FROM normal_scores;")  # change 'users' to your table
        rows = cur.fetchall()
        for row in rows:
            print(row)

        cur.execute("SELECT * FROM hard_scores;")  # change 'users' to your table
        rows = cur.fetchall()
        for row in rows:
            print(row)

        conn.close()

        return render_template("leaderboard.html")


# Fetch scores from database
@app.route("/fetch_score", methods=["POST"])
def fetch_score():
    mode = request.form.get("mode")
    try:
        with sqlite3.connect('leaderboard.db') as conn:
            cur = conn.cursor()

            by_time = []
            by_tiles_moved = []

            # View rows by time (least to greatest)
            cur.execute(f"SELECT * FROM {mode}_scores ORDER BY time ASC LIMIT 10;")  # change 'users' to your table
            rows = cur.fetchall()
            for row in rows:
                by_time.append(row)

            # View rows by time (least to greatest)
            cur.execute(f"SELECT * FROM {mode}_scores ORDER BY tiles_moved ASC LIMIT 10;")  # change 'users' to your table
            rows = cur.fetchall()
            for row in rows:
                by_tiles_moved.append(row)

            return jsonify({
                "time_leaderboard": by_time,
                "tiles_moved_leaderboard": by_tiles_moved
            })
    except sqlite3.Error as e:
        print(e)


# run webapp program
if __name__ == "__main__":
    app.run(debug=True)
