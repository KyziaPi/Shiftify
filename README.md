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
