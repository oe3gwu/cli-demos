#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tetris — terminal edition (CLI only, no pygame).

Features:
* Classic 10×20 well with 7-bag randomizer, hold, ghost piece, next preview.
* Arrow keys / WASD, space = hard drop, P = pause, C = colours on/off.
* Score, lines, level; speed increases with level.
* Playfield fills the terminal: wide cells (2–4 cols) and optional double row height.
* Sidebar panels for stats, next, hold, and controls; full-width status bar.
* Unicode borders; optional per-piece colours (toggle with C).
* Game over menu: restart or quit.
* Unix terminals and Windows with `pip install windows-curses`.

Run:  python pc/tetris.py
"""

import curses
import random
import time

# ----------------------------------------------------------------------
# Timing & scoring
# ----------------------------------------------------------------------
BASE_DELAY_MS = 800
MIN_DELAY_MS = 80
LINES_PER_LEVEL = 10

SCORE_TABLE = {1: 100, 2: 300, 3: 500, 4: 800}
SOFT_DROP_POINTS = 1
HARD_DROP_POINTS = 2

# ----------------------------------------------------------------------
# Display — terminal chars are ~2× taller than wide, so each cell uses
# cw terminal columns (and optionally ch rows) for a square look.
# ----------------------------------------------------------------------
BORDER_H = '═'
BORDER_V = '║'
CORNER_TL = '╔'
CORNER_TR = '╗'
CORNER_BL = '╚'
CORNER_BR = '╝'
PAIR_WELL_BG = 11
PAIR_GHOST_BG = 12

# Piece colours (pair index when colours enabled)
PIECE_NAMES = 'IOTSZJL'
PIECE_COLORS = {
    'I': 1,
    'O': 2,
    'T': 3,
    'S': 4,
    'Z': 5,
    'J': 6,
    'L': 7,
}

# Rotations: list of (dy, dx) offsets from anchor (row, col) — rotation 0..3
PIECES = {
    'I': [
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 2), (1, 2), (2, 2), (3, 2)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
        [(0, 1), (1, 1), (2, 1), (3, 1)],
    ],
    'O': [
        [(0, 0), (0, 1), (1, 0), (1, 1)],
    ] * 4,
    'T': [
        [(0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (1, 2), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 1)],
        [(0, 1), (1, 0), (1, 1), (2, 1)],
    ],
    'S': [
        [(0, 1), (0, 2), (1, 0), (1, 1)],
        [(0, 1), (1, 1), (1, 2), (2, 2)],
        [(1, 1), (1, 2), (2, 0), (2, 1)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
    ],
    'Z': [
        [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(0, 2), (1, 1), (1, 2), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
        [(0, 1), (1, 0), (1, 1), (2, 0)],
    ],
    'J': [
        [(0, 0), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (0, 2), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 0), (2, 1)],
    ],
    'L': [
        [(0, 2), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (1, 2), (2, 0)],
        [(0, 0), (0, 1), (1, 1), (2, 1)],
    ],
}

BOARD_W = 10
BOARD_H = 20
SIDEBAR_MIN_W = 26
STATUS_ROWS = 1
# Typical terminal cell aspect ≈ 2:1 (height:width)
CELL_ASPECT = 2


# ----------------------------------------------------------------------
# Curses helpers (aligned with snake.py)
# ----------------------------------------------------------------------
def safe_addch(stdscr, y, x, ch, attr=0):
    max_y, max_x = stdscr.getmaxyx()
    if y < 0 or x < 0 or y >= max_y or x >= max_x:
        return
    if y == max_y - 1 and x == max_x - 1:
        return
    try:
        stdscr.addch(y, x, ch, attr)
    except curses.error:
        pass


def safe_addstr(stdscr, y, x, text, attr=0):
    max_y, max_x = stdscr.getmaxyx()
    if y < 0 or y >= max_y or x >= max_x:
        return
    try:
        stdscr.addstr(y, x, text[: max(0, max_x - x - 1)], attr)
    except curses.error:
        pass


def init_colors():
    """Return True if colour pairs were configured."""
    if not curses.has_colors():
        return False
    curses.start_color()
    try:
        curses.use_default_colors()
    except curses.error:
        pass
    # Piece hues (foreground)
    palette = [
        (curses.COLOR_CYAN, -1),      # I
        (curses.COLOR_YELLOW, -1),    # O
        (curses.COLOR_MAGENTA, -1),   # T
        (curses.COLOR_GREEN, -1),     # S
        (curses.COLOR_RED, -1),       # Z
        (curses.COLOR_BLUE, -1),      # J
        (curses.COLOR_WHITE, -1),     # L
    ]
    for i, (fg, bg) in enumerate(palette, start=1):
        curses.init_pair(i, fg, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(10, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    try:
        curses.init_pair(PAIR_WELL_BG, -1, curses.COLOR_BLACK)
        curses.init_pair(PAIR_GHOST_BG, curses.COLOR_BLACK, curses.COLOR_BLACK)
    except curses.error:
        curses.init_pair(PAIR_WELL_BG, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(PAIR_GHOST_BG, curses.COLOR_WHITE, curses.COLOR_BLACK)
    return True


def piece_attr(piece_name, use_color, ghost=False):
    if not use_color:
        return curses.A_DIM if ghost else curses.A_REVERSE
    pair = curses.color_pair(PIECE_COLORS[piece_name])
    if ghost:
        return pair | curses.A_DIM
    return pair | curses.A_BOLD


def well_bg_attr(use_color):
    return curses.color_pair(PAIR_WELL_BG) if use_color else curses.A_REVERSE


def label_attr(use_color):
    return curses.color_pair(8) if use_color else 0


def title_attr(use_color):
    return curses.color_pair(10) | curses.A_BOLD if use_color else curses.A_BOLD


# ----------------------------------------------------------------------
# Layout — use the terminal, not a postage stamp in the middle
# ----------------------------------------------------------------------
class Layout:
    """Map logical board cells to terminal rows/cols (cw × ch each)."""

    def __init__(self, stdscr):
        self.term_h, self.term_w = stdscr.getmaxyx()
        self.status_y = self.term_h - STATUS_ROWS
        self.compact = self.term_h < 26 or self.term_w < 56

        sidebar_w = min(36, max(SIDEBAR_MIN_W, self.term_w // 3))
        play_w = max(24, self.term_w - sidebar_w - 1)
        play_h = max(12, self.term_h - STATUS_ROWS - 1)

        # Width: at least 2 cols per cell so blocks look square
        self.cw = max(2, min(4, (play_w - 2) // BOARD_W))
        # Height: 2 terminal rows per cell when there is room
        need_h = BOARD_H * 2 + 2
        self.ch = 2 if play_h >= need_h and self.cw >= 2 else 1
        if self.ch == 1:
            self.cw = max(2, min(4, (play_w - 2) // BOARD_W))

        self.inner_w = BOARD_W * self.cw
        self.inner_h = BOARD_H * self.ch
        self.border_w = self.inner_w + 2
        self.border_h = self.inner_h + 2

        self.well_x = 0
        self.well_y = 0
        self.sidebar_x = self.well_x + self.border_w + 1
        self.sidebar_w = self.term_w - self.sidebar_x

    def cell_origin(self, row, col):
        """Top-left terminal position for logical board cell (row, col)."""
        return (
            self.well_y + 1 + row * self.ch,
            self.well_x + 1 + col * self.cw,
        )


def block_fill(cw, solid=True):
    if solid:
        return '█' * cw
    return '░' * cw


def get_drop_delay_ms(level):
    return max(MIN_DELAY_MS, BASE_DELAY_MS - (level - 1) * 70)


# ----------------------------------------------------------------------
# Game logic
# ----------------------------------------------------------------------
class Bag:
    def __init__(self):
        self.queue = []

    def refill(self):
        bag = list(PIECE_NAMES)
        random.shuffle(bag)
        self.queue.extend(bag)

    def take(self):
        if len(self.queue) < 7:
            self.refill()
        return self.queue.pop(0)


class Board:
    def __init__(self):
        self.cells = {}  # (row, col) -> piece name
        self.width = BOARD_W
        self.height = BOARD_H

    def in_bounds(self, row, col):
        return 0 <= col < self.width and row < self.height

    def occupied(self, row, col):
        if not self.in_bounds(row, col):
            return row >= self.height or col < 0 or col >= self.width
        return (row, col) in self.cells

    def collides(self, cells, anchor_row, anchor_col):
        for dy, dx in cells:
            r, c = anchor_row + dy, anchor_col + dx
            if c < 0 or c >= self.width or r >= self.height:
                return True
            if r >= 0 and (r, c) in self.cells:
                return True
        return False

    def lock(self, piece_name, cells, anchor_row, anchor_col):
        for dy, dx in cells:
            r, c = anchor_row + dy, anchor_col + dx
            if r >= 0:
                self.cells[(r, c)] = piece_name

    def clear_lines(self):
        full_rows = [
            r for r in range(self.height)
            if all((r, c) in self.cells for c in range(self.width))
        ]
        for r in sorted(full_rows):
            for c in range(self.width):
                self.cells.pop((r, c), None)
        if not full_rows:
            return 0
        remaining = {}
        for (r, c), name in self.cells.items():
            shift = sum(1 for fr in full_rows if fr < r)
            remaining[(r - shift, c)] = name
        self.cells = remaining
        return len(full_rows)


class ActivePiece:
    def __init__(self, name, bag):
        self.name = name
        self.rotation = 0
        self.row = 0
        self.col = BOARD_W // 2 - 2
        self.bag = bag

    def cells(self):
        return PIECES[self.name][self.rotation % len(PIECES[self.name])]

    def rotated_cells(self, direction=1):
        rots = PIECES[self.name]
        new_rot = (self.rotation + direction) % len(rots)
        return rots[new_rot], new_rot

    def ghost_row(self, board):
        row = self.row
        while not board.collides(self.cells(), row + 1, self.col):
            row += 1
        return row


class GameState:
    def __init__(self):
        self.board = Board()
        self.bag = Bag()
        self.bag.refill()
        self.hold = None
        self.hold_used = False
        self.next_queue = [self.bag.take() for _ in range(3)]
        self.active = None
        self.score = 0
        self.lines = 0
        self.level = 1
        self.use_color = True
        self.colors_available = False
        self.paused = False
        self.game_over = False
        self.last_drop = time.monotonic()
        self.message = ''
        self.message_ttl = 0
        self.spawn_piece()

    def spawn_piece(self):
        name = self.next_queue.pop(0)
        self.next_queue.append(self.bag.take())
        self.active = ActivePiece(name, self.bag)
        self.hold_used = False
        if self.board.collides(self.active.cells(), self.active.row, self.active.col):
            self.game_over = True

    def level_up_lines(self):
        return self.lines // LINES_PER_LEVEL + 1

    def tick_level(self):
        self.level = self.level_up_lines()

    def drop_delay(self):
        return get_drop_delay_ms(self.level) / 1000.0

    def add_score(self, points):
        self.score += points * self.level

    def set_message(self, text, ttl=60):
        self.message = text
        self.message_ttl = ttl


# ----------------------------------------------------------------------
# Drawing
# ----------------------------------------------------------------------
def draw_cell(stdscr, layout, row, col, piece_name, use_color, ghost=False):
    if row < 0:
        return
    y, x = layout.cell_origin(row, col)
    attr = piece_attr(piece_name, use_color, ghost=ghost)
    fill = block_fill(layout.cw, solid=not ghost)
    for dy in range(layout.ch):
        safe_addstr(stdscr, y + dy, x, fill, attr)


def draw_piece(stdscr, layout, cells, anchor_row, anchor_col, piece_name, use_color,
               ghost=False):
    for dy, dx in cells:
        draw_cell(stdscr, layout, anchor_row + dy, anchor_col + dx, piece_name,
                  use_color, ghost=ghost)


def draw_well_background(stdscr, layout, use_color):
    """Fill the playfield so it reads as one large panel."""
    bg = well_bg_attr(use_color)
    empty = ' ' * layout.cw
    for row in range(BOARD_H):
        y, x = layout.cell_origin(row, 0)
        for dy in range(layout.ch):
            for col in range(BOARD_W):
                safe_addstr(stdscr, y + dy, x + col * layout.cw, empty, bg)


def draw_well_border(stdscr, layout, use_color):
    attr = label_attr(use_color)
    x0, y0 = layout.well_x, layout.well_y
    bw, bh = layout.border_w, layout.border_h

    safe_addch(stdscr, y0, x0, CORNER_TL, attr)
    for col in range(BOARD_W):
        seg = BORDER_H * layout.cw
        safe_addstr(stdscr, y0, x0 + 1 + col * layout.cw, seg[: layout.cw], attr)
    safe_addch(stdscr, y0, x0 + bw - 1, CORNER_TR, attr)

    for row in range(BOARD_H):
        y = y0 + 1 + row * layout.ch
        for dy in range(layout.ch):
            safe_addch(stdscr, y + dy, x0, BORDER_V, attr)
            safe_addch(stdscr, y + dy, x0 + bw - 1, BORDER_V, attr)

    yb = y0 + bh - 1
    safe_addch(stdscr, yb, x0, CORNER_BL, attr)
    for col in range(BOARD_W):
        seg = BORDER_H * layout.cw
        safe_addstr(stdscr, yb, x0 + 1 + col * layout.cw, seg[: layout.cw], attr)
    safe_addch(stdscr, yb, x0 + bw - 1, CORNER_BR, attr)


def draw_board(stdscr, state, layout):
    draw_well_background(stdscr, layout, state.use_color)
    for (r, c), name in state.board.cells.items():
        draw_cell(stdscr, layout, r, c, name, state.use_color)

    if state.active and not state.game_over:
        piece = state.active
        ghost_r = piece.ghost_row(state.board)
        draw_piece(stdscr, layout, piece.cells(), ghost_r, piece.col,
                   piece.name, state.use_color, ghost=True)
        draw_piece(stdscr, layout, piece.cells(), piece.row, piece.col,
                   piece.name, state.use_color)


def draw_mini_piece(stdscr, layout, name, top_y, left_x, use_color, cell=2):
    """Preview box — same double-width cells as the main well."""
    cells = PIECES[name][0]
    min_r = min(dy for dy, _ in cells)
    min_c = min(dx for _, dx in cells)
    cw = max(2, cell)
    fill = block_fill(cw)
    for dy, dx in cells:
        y = top_y + (dy - min_r) * 2
        x = left_x + (dx - min_c) * cw
        attr = piece_attr(name, use_color)
        safe_addstr(stdscr, y, x, fill, attr)
        safe_addstr(stdscr, y + 1, x, fill, attr)


def draw_panel_border(stdscr, y, x, h, w, title, use_color):
    attr = label_attr(use_color)
    if w < 4 or h < 3:
        return
    safe_addch(stdscr, y, x, CORNER_TL, attr)
    title_s = f' {title} '
    inner = w - 2
    if len(title_s) <= inner:
        safe_addstr(stdscr, y, x + 1, title_s, title_attr(use_color))
        rest = inner - len(title_s)
        if rest > 0:
            safe_addstr(stdscr, y, x + 1 + len(title_s), BORDER_H * rest, attr)
    else:
        safe_addstr(stdscr, y, x + 1, BORDER_H * inner, attr)
    safe_addch(stdscr, y, x + w - 1, CORNER_TR, attr)
    for row in range(1, h - 1):
        safe_addch(stdscr, y + row, x, BORDER_V, attr)
        safe_addch(stdscr, y + row, x + w - 1, BORDER_V, attr)
    safe_addch(stdscr, y + h - 1, x, CORNER_BL, attr)
    safe_addstr(stdscr, y + h - 1, x + 1, BORDER_H * inner, attr)
    safe_addch(stdscr, y + h - 1, x + w - 1, CORNER_BR, attr)


def draw_sidebar(stdscr, state, layout):
    sx = layout.sidebar_x
    sw = max(10, layout.sidebar_w)
    uc = state.use_color
    la = label_attr(uc)
    ta = title_attr(uc)

    # Stats panel (top)
    ph = min(10, layout.border_h)
    draw_panel_border(stdscr, 0, sx, ph, sw, 'TETRIS', uc)
    safe_addstr(stdscr, 2, sx + 2, f'Score  {state.score:>8}', ta)
    safe_addstr(stdscr, 3, sx + 2, f'Lines  {state.lines:>8}', la)
    safe_addstr(stdscr, 4, sx + 2, f'Level  {state.level:>8}', la)
    safe_addstr(stdscr, 5, sx + 2, f'Speed  {get_drop_delay_ms(state.level):>5} ms', la)
    color_txt = 'Farbe: AN' if state.use_color else 'Farbe: AUS'
    if not state.colors_available:
        color_txt = 'Farbe: n/v'
    safe_addstr(stdscr, 6, sx + 2, color_txt, la)

    # Next + Hold panels
    mid_y = ph + 1
    box_h = 8
    draw_panel_border(stdscr, mid_y, sx, box_h, sw, 'NEXT', uc)
    pcw = min(3, layout.cw)
    if state.next_queue:
        draw_mini_piece(stdscr, layout, state.next_queue[0], mid_y + 2, sx + 3, uc, pcw)

    hold_y = mid_y + box_h + 1
    draw_panel_border(stdscr, hold_y, sx, box_h, sw, 'HOLD', uc)
    if state.hold:
        draw_mini_piece(stdscr, layout, state.hold, hold_y + 2, sx + 3, uc, pcw)
    else:
        safe_addstr(stdscr, hold_y + 3, sx + 3, '— leer —', la)

    if not layout.compact:
        hints_y = hold_y + box_h + 2
        draw_panel_border(stdscr, hints_y, sx, min(12, layout.term_h - hints_y), sw,
                          'STEUERUNG', uc)
        hints = [
            '  ← → / A D     bewegen',
            '  ↑ / W         drehen',
            '  ↓ / S         soft drop',
            '  Leertaste       hard drop',
            '  F               hold',
            '  C               farbe',
            '  P               pause',
            '  Q               beenden',
        ]
        for i, line in enumerate(hints):
            if hints_y + 2 + i >= layout.term_h - STATUS_ROWS:
                break
            safe_addstr(stdscr, hints_y + 2 + i, sx + 1, line, la)


def draw_status_bar(stdscr, state, layout):
    y = layout.status_y
    if y >= layout.term_h:
        y = layout.term_h - 1
    uc = state.use_color
    mode = 'PAUSE' if state.paused else ('GAME OVER' if state.game_over else 'SPIEL')
    sep = '─' * max(0, layout.term_w - 2)
    safe_addstr(stdscr, y, 0, sep[: layout.term_w], label_attr(uc))
    left = f' {mode} │ Score {state.score} │ Zeilen {state.lines} │ Lv {state.level} '
    safe_addstr(stdscr, y, 0, left[: layout.term_w - 1], title_attr(uc))
    if state.message and state.message_ttl > 0:
        msg = f' {state.message} '
        safe_addstr(stdscr, y, max(0, layout.term_w - len(msg) - 1), msg, label_attr(uc))


def draw_frame(stdscr, state, layout):
    stdscr.clear()
    try:
        stdscr.bkgd(' ', well_bg_attr(state.use_color))
    except curses.error:
        pass
    draw_well_border(stdscr, layout, state.use_color)
    draw_board(stdscr, state, layout)
    draw_sidebar(stdscr, state, layout)
    draw_status_bar(stdscr, state, layout)
    stdscr.refresh()


def draw_centered_box(stdscr, lines, use_color):
    stdscr.clear()
    term_h, term_w = stdscr.getmaxyx()
    start_y = max(0, term_h // 2 - len(lines) // 2)
    la = label_attr(use_color)
    ta = title_attr(use_color)
    for i, (text, is_title) in enumerate(lines):
        y = start_y + i
        if y >= term_h:
            break
        x = max(0, (term_w - len(text)) // 2)
        safe_addstr(stdscr, y, x, text[: max(0, term_w - x - 1)], ta if is_title else la)
    stdscr.refresh()


def show_pause_menu(stdscr, use_color):
    draw_centered_box(stdscr, [
        (' ═══ PAUSE ═══ ', True),
        ('', False),
        (' [P] Continue ', False),
        (' [Q] Quit ', False),
    ], use_color)
    stdscr.nodelay(False)
    while True:
        key = stdscr.getch()
        if key in (ord('p'), ord('P')):
            stdscr.nodelay(True)
            return True
        if key in (ord('q'), ord('Q'), 27):
            return False


def show_game_over_menu(stdscr, state):
    draw_centered_box(stdscr, [
        (' GAME OVER ', True),
        (f' Score: {state.score}  Lines: {state.lines} ', False),
        ('', False),
        (' [R] Restart    [Q] Quit ', False),
    ], state.use_color)
    stdscr.nodelay(False)
    while True:
        key = stdscr.getch()
        if key in (ord('r'), ord('R')):
            stdscr.nodelay(True)
            return True
        if key in (ord('q'), ord('Q'), 27):
            return False


# ----------------------------------------------------------------------
# Input & actions
# ----------------------------------------------------------------------
def try_move(state, drow, dcol):
    if state.paused or state.game_over or not state.active:
        return False
    piece = state.active
    if not state.board.collides(piece.cells(), piece.row + drow, piece.col + dcol):
        piece.row += drow
        piece.col += dcol
        return True
    return False


def try_rotate(state, direction=1):
    if state.paused or state.game_over or not state.active:
        return False
    piece = state.active
    new_cells, new_rot = piece.rotated_cells(direction)
    for kick in (0, -1, 1, -2, 2):
        if not state.board.collides(new_cells, piece.row, piece.col + kick):
            piece.rotation = new_rot
            piece.col += kick
            return True
    return False


def hard_drop(state):
    if state.paused or state.game_over or not state.active:
        return
    piece = state.active
    dist = 0
    while not state.board.collides(piece.cells(), piece.row + 1, piece.col):
        piece.row += 1
        dist += 1
    state.add_score(dist * HARD_DROP_POINTS)
    lock_piece(state)


def lock_piece(state):
    piece = state.active
    if not piece:
        return
    state.board.lock(piece.name, piece.cells(), piece.row, piece.col)
    cleared = state.board.clear_lines()
    if cleared:
        state.lines += cleared
        state.add_score(SCORE_TABLE.get(cleared, 0))
        names = {1: 'Single', 2: 'Double', 3: 'Triple', 4: 'TETRIS!'}.get(cleared, '')
        state.set_message(f'{names} +{SCORE_TABLE.get(cleared, 0) * state.level}')
        state.tick_level()
    state.spawn_piece()
    state.last_drop = time.monotonic()


def soft_drop_tick(state):
    if try_move(state, 1, 0):
        state.add_score(SOFT_DROP_POINTS)


def hold_piece(state):
    if state.paused or state.game_over or not state.active or state.hold_used:
        return
    piece = state.active
    current = piece.name
    if state.hold is None:
        state.hold = current
        state.spawn_piece()
    else:
        state.hold, swap = current, state.hold
        state.active = ActivePiece(swap, state.bag)
        state.active.row = 0
        state.active.col = BOARD_W // 2 - 2
        if state.board.collides(state.active.cells(), state.active.row, state.active.col):
            state.game_over = True
    state.hold_used = True


def gravity_tick(state):
    if state.paused or state.game_over:
        return
    now = time.monotonic()
    if now - state.last_drop < state.drop_delay():
        return
    state.last_drop = now
    if not try_move(state, 1, 0):
        lock_piece(state)


def handle_key(state, key):
    if key == ord('c') or key == ord('C'):
        if state.colors_available:
            state.use_color = not state.use_color
            state.set_message(
                'Farben an' if state.use_color else 'Farben aus', ttl=40,
            )
        return

    if key == ord('q') or key == ord('Q') or key == 27:
        state.game_over = True
        return 'quit'

    if state.paused or state.game_over:
        return

    if key in (curses.KEY_LEFT, ord('a')):
        try_move(state, 0, -1)
    elif key in (curses.KEY_RIGHT, ord('d')):
        try_move(state, 0, 1)
    elif key in (curses.KEY_DOWN, ord('s')):
        if try_move(state, 1, 0):
            state.add_score(SOFT_DROP_POINTS)
            state.last_drop = time.monotonic()
    elif key in (curses.KEY_UP, ord('w')):
        try_rotate(state)
    elif key == ord(' '):
        hard_drop(state)
    elif key in (ord('H'), ord('f'), ord('F')):
        hold_piece(state)

    return None


# ----------------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------------
def init_curses(stdscr, delay_ms):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(delay_ms)
    stdscr.keypad(True)
    stdscr.clear()
    stdscr.refresh()
    return stdscr


def run_game(stdscr):
    colors_ok = init_colors()
    state = GameState()
    state.colors_available = colors_ok
    state.use_color = colors_ok

    delay_ms = get_drop_delay_ms(1)
    stdscr = init_curses(stdscr, delay_ms)

    while True:
        layout = Layout(stdscr)
        delay_ms = get_drop_delay_ms(state.level)
        stdscr.timeout(delay_ms if not state.paused else 100)

        if state.message_ttl > 0:
            state.message_ttl -= 1

        key = stdscr.getch()
        if key != -1:
            if key in (ord('p'), ord('P')):
                if not state.paused:
                    state.paused = True
                    if not show_pause_menu(stdscr, state.use_color):
                        return state
                    state.paused = False
                    init_curses(stdscr, delay_ms)
                continue
            if key == ord('q') or key == ord('Q') or key == 27:
                return state
            result = handle_key(state, key)
            if result == 'quit':
                return state

        if not state.paused:
            gravity_tick(state)

        draw_frame(stdscr, state, layout)

        if state.game_over:
            return state


def main(stdscr):
    while True:
        state = run_game(stdscr)
        if not show_game_over_menu(stdscr, state):
            break


if __name__ == '__main__':
    curses.wrapper(main)
