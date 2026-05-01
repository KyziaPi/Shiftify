# SHIFTIFY
#### Video Demo:  https://youtu.be/6pWC3xlOnkY
#### Description:
This is my final project for CS50x, and it is a sliding puzzle minigame with 3 difficulties: easy (3x3), medium (4x4), 
hard (5x5). In case you are unfamiliar with sliding puzzle, it basically starts as a shuffled numbered tiles that you will
unshuffle by sliding the tiles through the one gap present in the board. Once you unshuffled the numbers (1 to x) with the 
gap at the lower-right most space, you clear the game.

After picking on of the modes, you click the tile and if there is a blank space beside that tile, then it will move to 
that place, leaving the tile it was on before blank. The moment you click the first tile that can be moved, the timer 
will start and the number of tiles moved will increment per tile click that does move.

Aside from the game aspect, I added a challenge by making a leaderboard for the top 10 of each difficulty in two categories
(least time and least amount of tiles moved).

## Languages used and files associated with it
### Python
#### puzzle_logic.py
This contains the main logic for the puzzle minigame. First off, the generation of the board itself AKA the shuffling of 
the numbers. Because you can only slide all the tiles through one gap, it is possible that the randomly generated array
for the board will not be solvable. To solve this, I utilized the inversion formula. Here is the conditions for the 
set of array to be solvable:
1. If odd, the number of inversion must be even to be solvable
>     if board_width % 2 == 1:
>        # Odd width is solvable if inversions are even (width - 1)
>        return inversions % 2 == 0
2. Else if even, then the number of inversions plus the row number (bottom-up, last row is 1, first row is 4) must be odd
>     else:
>        # Even width needs to consider the empty space's row (count from bottom to up)
>        empty_row_from_bottom = board_width - (board.index(0) // board_width)
>        return (inversions + empty_row_from_bottom) % 2 == 1

This also contains the is_solved() that checks whether the arrangement of the list is 1 to x with 0 at the very end, 
can_move() that checks whether a tile is movable, and move_tile() that moves the tile itself.

#### app.py
This contains the controllers and the models for the web application. Here you will see how the game logic from a simple
list and a couple arithmetics is converted to the actual GUI that can be seen from the web app. This is also where the 
database tables are created and updated.

My initial design for every time a tile is moved was to simply render_template(), but it was a huge hassle because every
click, the page reloads to update the board. However, I got busy with school and postponed this for 6 months. Within 
those 6 months I learned a lot about web applications and more importantly, javascript. In javascript I learned about jquery 
AJAX. So, when I got back to this project, I changed the design that always loads upon tile movement to a more responsive
AJAX that no longer reloads, but instead utilizes json to receive data from the backend (python) to the javascript (frontend),
where I manipulate the HTML to update.

#### database table creation (in app.py)
Going back to python, here is the database for my leaderboard. It is quite simple and I've handled bigger databases, but 
I am still learning on database for python:
>       CREATE TABLE IF NOT EXISTS easy_scores (
>            id INTEGER PRIMARY KEY AUTOINCREMENT,
>            username TEXT,
>            time REAL,
>            tiles_moved INTEGER
>        );
>       CREATE TABLE IF NOT EXISTS normal_scores (
>            id INTEGER PRIMARY KEY AUTOINCREMENT,
>            username TEXT,
>            time REAL,
>            tiles_moved INTEGER
>        );
>       CREATE TABLE IF NOT EXISTS hard_scores (
>            id INTEGER PRIMARY KEY AUTOINCREMENT,
>            username TEXT,
>            time REAL,
>            tiles_moved INTEGER
>        );

While I didn't need to include the id, it is a good afterthought just in case I add an admin for this system. They
can delete a score if they wanted to, especially if it turns out that they hacked their way through the leaderboard.

#### database data manipulation (in app.py)
Here is the data insertion within the database:
>        try:
>                print(f"Inserting into table: {mode}_scores")
>                query = f"INSERT INTO {mode}_scores(username, time, tiles_moved) VALUES(?, ?, ?)"
>                scores = (username, final_time, tiles_moved)
>
>                # query to insert score in db
>                cur = conn.cursor()
>                cur.execute(query, scores)
>
>                # commit changes to db
>                conn.commit()
>        except sqlite3.Error as e:
>            print(e)

It is fairly simple, after the player finishes a puzzle and put their name in the input field at the result page, all they 
need to do is click the "Submit Score to the Leaderboard" button so this code snippet will run and their score will be put
in the database.

#### database querying (in app.py)
>     try:
>        with sqlite3.connect('leaderboard.db') as conn:
>            cur = conn.cursor()
>
>            by_time = []
>            by_tiles_moved = []
>
>            # View rows by time (least to greatest)
>            cur.execute(f"SELECT * FROM {mode}_scores ORDER BY time ASC LIMIT 10;")  # change 'users' to your table
>            rows = cur.fetchall()
>            for row in rows:
>                by_time.append(row)
>
>            # View rows by time (least to greatest)
>            cur.execute(f"SELECT * FROM {mode}_scores ORDER BY tiles_moved ASC LIMIT 10;")  # change 'users' to your table
>            rows = cur.fetchall()
>            for row in rows:
>                by_tiles_moved.append(row)
>
>            return jsonify({
>                "time_leaderboard": by_time,
>                "tiles_moved_leaderboard": by_tiles_moved
>            })
>     except sqlite3.Error as e:
>        print(e)

This time, this is the code + query for how the rows within the database is shown on the leaderboard. As you can see from 
the jsonify(), I also utilized AJAX on this leaderboard so that it doesn't need to reload when switching between modes.
Meanwhile, for the actual query, I utilized "ORDER BY time ASC" or "ORDER BY tiles_moved ASC" to have the least to greatest 
for both types of leaderboard per modes. Lastly, as mentioned in the description - since the leaderboard will only show top 10,
I included "LIMIT 10" on the query.

### routes (app.py)
#### simple routes - "/", "/instructions", "/reshuffle", "/get_timer", "/result"
**"/"** - index, shows the main menu of Shiftify with 3 buttons - easy, normal, and hard mode

**"/instructions"** - introduction for Shiftify and me, the creator of the system. Also contains the instructions and 
leaderboard details.

**"/reshuffle"** - reshuffles the tile position and resets the timer and the tiles moved count if it is currently being monitored. 

**"/get_timer"** - if board is already in session (player already moved one tile), it gets how much time has elapsed since started.

**"/result"** - redirects player to the result page the moment the board is solved. It shows the mode of the board that was
finished, how long it took for the player to finish the game in decimals, and how many tiles were moved. From this page, 
the player can submit their score to the leaderboard for other players to see if they do reach top 10.

#### main route - "/play/<mode>"
Here, it is dynamically set to whatever mode(easy, normal, hard) the player picked before starting the game. This is where
all the backend logic from puzzle_logic.py is applied to connect to the frontend via javascript. Session is utilized to 
keep the board's progress. If the session is not yet in progress, then it will simply render_template(), else it will 
send the data to frontend via AJAX to prevent from constantly reloading per tile movement.

#### main route - "/leaderboard"
This is where the leaderboard is found. It also contains a POST method for when the player is submitting a score to the 
leaderboard. Within the POST method, you will find the data manipulation language for inserting a row into one of the 
tables depending on the mode.

#### main route - "/fetch_score"
This gets the top 10 existing rows within each mode by utilizing data query language. Two categories per mode, least 
time it took and least tile move it took. This is connected to the frontend through json to prevent reload when a mode is 
selected in the leaderboard.

### /templates
**layout.html** - contains the backbone of all the other templates within this system. The backbone includes: libraries 
(bootstrap, jQuery, stylesheet), navbar, and footer. Prevents repetitive coding by utilizing Django from Flask.

**index.html** - The main menu of this system/game. You can see the logo, title, and click buttons to play easy, normal,
or hard mode.

**instructions.html** - contains the introduction for this game, its purpose (CS50x final project), its creator (me), 
game instructions, and explanation to the leaderboard system.

**mode_easy.html, mode_normal.html, mode_hard.html** - these are the pages for the different modes of the game. Main 
difference is the reshuffle button and the number of tiles.

**result.html** - when the tile is solved, immediately gets redirected to this page. Can type name and submit to show your
score in the leaderboard if it is top 10.

**leaderboard.html** - shows top 10 per mode for the time category and tiles-moved category. Can switch to different mode's
leaderboard by pressing the button for the mode you want.

#### script.js
Contains the AJAX for the tile update and timer update (updates per second or when a tile is clicked). "/get_timer" and 
"/play/<mode>" routes were utilized from frontend to connect to UI. "/get_timer" returns whether the board is currently 
running and the elapsed time. "/play/<mode>" returns the current arrangement of the numbers in the tile, the number of
tiles that's been moved, and the current time that's elapsed if the board is still not solved. If it's already solved, 
it returns true that it's solved to prevent error because once it's solved, the board no longer exists.

#### leaderboard.js
Contains the AJAX for the leaderboard details. Leaderboard's difficulty mode that is shown depends on the radio button 
that is currently "checked" or active. "/fetch_score" was utilized from frontend to connect to UI. "/fetch_score" returns
two arrays, all the rows for the selected difficulty in ascending order of time and in ascending order of tiles moved. 
Within those array of rows are another array containing the id, username, time, and tiles_moved.

## Parting Words
I am truly thankful for this course. Thanks to CS50x, I have grown to like the feeling of my brain just hurting so much
from trying to figure out the bug within my code. That's where you truly learn, because a problem that takes you hours or
even days to find a solution to will make you really remember that dumb mistake that you did, therefore remembering it 
better for the next time you encounter it. I've been very lazy to self-study and code on my own free time, but this course 
has made me appreciate just how much progress you can gain from self-studying. I am interested in data science, so after
this I will learn STAT110x and then Introduction to Data Science with Python. Thank you Dr. Malan for inspiring me to be
the best version of myself!