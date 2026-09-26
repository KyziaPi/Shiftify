# Shiftify

Sliding puzzle game built with Flask, SQLite, and JavaScript. Players choose a difficulty level, solve the board by sliding tiles into the empty space, and compete on a local leaderboard based on time and move count.

Demo: https://youtu.be/6pWC3xlOnkY

## Overview

Shiftify includes:
- Easy mode: 3x3 board
- Normal mode: 4x4 board
- Hard mode: 5x5 board
- Live timer and move counter
- Solvable board generation using puzzle logic
- Per-difficulty leaderboard ranked by shortest time and fewest moves
- AJAX-driven gameplay to avoid full page reloads

## Tech Stack

- Python
- Flask
- SQLite
- JavaScript
- HTML/CSS
- Bootstrap

## Project Structure

- `app.py` — Flask routes, game state, leaderboard logic, and database setup
- `puzzle_logic.py` — board generation, movement rules, solvability checks, and win detection
- `templates/` — HTML views for the game, results, instructions, and leaderboard
- `static/` — CSS and JavaScript frontend logic
- `leaderboard.db` — SQLite database created at runtime for saved scores

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the application:

```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000/`

#### Description:
This is a sliding puzzle minigame with 3 difficulties: easy (3x3), medium (4x4), and hard (5x5). In case the player is unfamiliar with sliding puzzles, the board begins as a shuffled arrangement of numbered tiles. The objective is to reorder the tiles into ascending order by sliding them into the empty space until the final position is solved.

After selecting a mode, the player clicks a tile. If a blank space is adjacent, the tile moves into that position, leaving the previous space empty. The timer begins on the first valid move, and the move counter increases with each successful tile shift.

In addition to the core gameplay, the app includes a leaderboard for the top 10 scores in each difficulty level across two categories: fastest completion time and fewest moves.

## Languages and Files

### Python
- `puzzle_logic.py` — generates solvable boards, validates movement, and checks completion.
- `app.py` — contains the Flask routes, game flow, and leaderboard logic.

### Frontend
- `templates/` — pages for the menu, instructions, gameplay, result screen, and leaderboard.
- `static/` — CSS and JavaScript for board interactions, timer updates, and AJAX requests.

### Data
- `leaderboard.db` — SQLite database used to store scores by difficulty and ranking category.
4. Open the app in your browser:

```text
http://127.0.0.1:5000/
```

## How to Play

1. Select a difficulty from the main menu.
2. Move tiles into the empty space to arrange the numbers in ascending order.
3. The timer starts after the first valid move.
4. Once the puzzle is solved, enter your username to submit your score.
5. View the leaderboard to compare your result against the top scores.

## Gameplay Logic

The puzzle logic ensures board generation produces a solvable arrangement by checking inversion rules based on board size. The game validates movement, tracks elapsed time, updates move counts, and detects when the board is solved.

## Leaderboard

Scores are stored in SQLite and grouped by game mode. Each mode tracks:
- Fastest completion time
- Fewest tiles moved

The leaderboard displays the top 10 results for each category.

## Notes

This project was designed as a web-based sliding puzzle with responsive interaction using AJAX so the board updates smoothly without reloading the page.
