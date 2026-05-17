#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple Snake game that runs entirely in the terminal (CLI).

Features:
* Arrow-key control (or WASD) – change direction.
* Non-blocking input – the game runs at a constant speed.
* Growing tail, food spawning, score counter.
* Collision detection with walls and self.
* Playfield adapts to the terminal window size.
* After game over: show score and choose restart or quit.
* Works on Unix terminals and on Windows with `pip install windows-curses`.

Run:  python snake.py
"""

import curses
import random
from collections import deque

# ----------------------------------------------------------------------
# Configuration (tweak these to change game behavior)
# ----------------------------------------------------------------------
FRAME_DELAY = 0.1  # Seconds between frames (≈10 FPS)

# Symbols used for drawing
WALL = '#'
FOOD = '*'
SNAKE = '○'
SNAKE_HEAD = '●'
EMPTY = ' '

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def init_curses(stdscr):
    """Configure the curses window."""
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(int(FRAME_DELAY * 1000))
    stdscr.clear()
    stdscr.refresh()
    return stdscr


def get_playfield_size(stdscr):
    """
    Return inner play area (height, width) from the current terminal size.

    Border uses rows/cols 0 .. height+1 and 0 .. width+1. We leave one extra
    row/column free because curses cannot write to the bottom-right screen cell.
    """
    term_h, term_w = stdscr.getmaxyx()
    return max(1, term_h - 3), max(1, term_w - 3)


def safe_addch(stdscr, y, x, ch):
    """addch that never raises (terminal edge / bottom-right quirk)."""
    max_y, max_x = stdscr.getmaxyx()
    if y < 0 or x < 0 or y >= max_y or x >= max_x:
        return
    if y == max_y - 1 and x == max_x - 1:
        return
    try:
        stdscr.addch(y, x, ch)
    except curses.error:
        pass


def place_food(snake_body, height, width):
    """Return a random position that is NOT occupied by the snake."""
    while True:
        y = random.randint(1, height)
        x = random.randint(1, width)
        if (y, x) not in snake_body:
            return (y, x)


def draw_border(stdscr, height, width):
    """Draw a simple box around the playfield."""
    for x in range(width + 2):
        safe_addch(stdscr, 0, x, WALL)
        safe_addch(stdscr, height + 1, x, WALL)
    for y in range(height + 2):
        safe_addch(stdscr, y, 0, WALL)
        safe_addch(stdscr, y, width + 1, WALL)


def draw_game(stdscr, snake_body, food_pos, score, height, width):
    """Render the whole frame."""
    stdscr.clear()
    draw_border(stdscr, height, width)

    fy, fx = food_pos
    safe_addch(stdscr, fy, fx, FOOD)

    for y, x in snake_body:
        ch = SNAKE_HEAD if (y, x) == snake_body[0] else SNAKE
        safe_addch(stdscr, y, x, ch)

    try:
        stdscr.addstr(0, 2, f" Score: {score} ")
    except curses.error:
        pass
    stdscr.refresh()


def show_game_over_menu(stdscr, score):
    """
    Show final score and wait for restart [R] or quit [Q]/ESC.
    Returns True to play again, False to exit.
    """
    stdscr.nodelay(False)
    stdscr.clear()

    term_h, term_w = stdscr.getmaxyx()
    lines = [
        f" GAME OVER! Score: {score} ",
        "",
        " [R] Restart    [Q] Quit ",
    ]
    start_y = max(0, term_h // 2 - len(lines) // 2)

    for i, line in enumerate(lines):
        y = start_y + i
        if y >= term_h:
            break
        x = max(0, (term_w - len(line)) // 2)
        try:
            stdscr.addstr(y, x, line[: max(0, term_w - x - 1)])
        except curses.error:
            pass

    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key in (ord('r'), ord('R')):
            return True
        if key in (ord('q'), ord('Q'), 27):
            return False


def run_game(stdscr):
    """Play one round. Returns the final score."""
    stdscr = init_curses(stdscr)
    height, width = get_playfield_size(stdscr)

    init_len = min(5, max(1, width - width // 2))
    snake = deque()
    start_y = max(1, min(height, height // 2))
    start_x = max(1, min(width - init_len, width // 2))
    direction = curses.KEY_RIGHT
    for i in range(init_len):
        snake.appendleft((start_y, start_x + i))
    food = place_food(snake, height, width)
    score = 0

    while True:
        key = stdscr.getch()

        if key in (
            curses.KEY_UP,
            curses.KEY_DOWN,
            curses.KEY_LEFT,
            curses.KEY_RIGHT,
            ord('w'),
            ord('a'),
            ord('s'),
            ord('d'),
        ):
            new_dir = key
            opposite = {
                curses.KEY_UP: curses.KEY_DOWN,
                curses.KEY_DOWN: curses.KEY_UP,
                curses.KEY_LEFT: curses.KEY_RIGHT,
                curses.KEY_RIGHT: curses.KEY_LEFT,
                ord('w'): ord('s'),
                ord('s'): ord('w'),
                ord('a'): ord('d'),
                ord('d'): ord('a'),
            }.get(new_dir, None)

            if opposite != direction:
                direction = new_dir

        if key == ord('q') or key == 27:
            return score

        head_y, head_x = snake[0]
        if direction == curses.KEY_UP:
            new_head = (head_y - 1, head_x)
        elif direction == curses.KEY_DOWN:
            new_head = (head_y + 1, head_x)
        elif direction == curses.KEY_LEFT:
            new_head = (head_y, head_x - 1)
        else:
            new_head = (head_y, head_x + 1)

        if (
            new_head[0] == 0
            or new_head[0] == height + 1
            or new_head[1] == 0
            or new_head[1] == width + 1
        ):
            return score

        if new_head in snake:
            return score

        snake.appendleft(new_head)

        if new_head == food:
            score += 1
            food = place_food(snake, height, width)
        else:
            snake.pop()

        draw_game(stdscr, snake, food, score, height, width)


def main(stdscr):
    while True:
        score = run_game(stdscr)
        if not show_game_over_menu(stdscr, score):
            break


if __name__ == "__main__":
    curses.wrapper(main)
