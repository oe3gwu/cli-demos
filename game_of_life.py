#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Conway's Game of Life — detailed terminal edition (CLI only).

Features:
* Full simulation with configurable rulesets (B/S notation) and torus mode.
* Playfield size follows the terminal window (like snake.py).
* Pattern library (oscillators, spaceships, methuselahs, guns, etc.).
* Interactive editor: cursor, draw/erase, place patterns, random fill, clear.
* Run / pause, single-step, variable speed, population & birth/death stats.
* Optional cell-age visualization; stability hint after repeated states.
* Help overlay and post-session summary.
* Works on Unix and Windows (`pip install windows-curses`).

Run:  python game_of_life.py
"""

import curses
import random

# ----------------------------------------------------------------------
# Display symbols
# ----------------------------------------------------------------------
DEAD = '·'
ALIVE = '█'
ALIVE_YOUNG = '▓'
ALIVE_MATURE = '█'
ALIVE_OLD = '░'
CURSOR = '╋'
CURSOR_ON = '⊕'
BORDER = '│'
BORDER_H = '─'
BORDER_CORNER = '┌'

# ----------------------------------------------------------------------
# Timing defaults
# ----------------------------------------------------------------------
MIN_DELAY_MS = 20
MAX_DELAY_MS = 2000
DEFAULT_DELAY_MS = 120

# ----------------------------------------------------------------------
# Rulesets: name -> (birth_counts, survive_counts)
# ----------------------------------------------------------------------
RULESETS = {
    'Conway (B3/S23)': ({3}, {2, 3}),
    'HighLife (B36/S23)': ({3, 6}, {2, 3}),
    'Day & Night (B3678/S34678)': ({3, 6, 7, 8}, {3, 4, 6, 7, 8}),
    'Seeds (B2/S)': ({2}, set()),
    'Maze (B3/S12345)': ({3}, {1, 2, 3, 4, 5}),
    'Anneal (B4678/S35678)': ({4, 6, 7, 8}, {3, 5, 6, 7, 8}),
    'LifeWithoutDeath (B3/S012345678)': ({3}, {0, 1, 2, 3, 4, 5, 6, 7, 8}),
    'Morley (B368/S245)': ({3, 6, 8}, {2, 4, 5}),
    'Replicator (B1357/S1357)': ({1, 3, 5, 7}, {1, 3, 5, 7}),
}
RULESET_NAMES = list(RULESETS.keys())

# ----------------------------------------------------------------------
# Pattern library: name -> list of (dy, dx) relative to anchor (top-left)
# ----------------------------------------------------------------------


def _gosper_gun_cells():
    """Gosper glider gun (standard layout, two block oscillators + glider stream)."""
    left = [
        (4, 0), (5, 0), (4, 1), (5, 1),
        (4, 2), (5, 2), (3, 3), (7, 3),
        (2, 4), (8, 4), (2, 5), (8, 5),
        (2, 6), (8, 6), (5, 6),
        (3, 7), (7, 7), (5, 8),
        (5, 9),
    ]
    right = [
        (0, 12), (1, 12), (0, 13), (1, 13),
        (0, 14), (1, 14), (2, 13), (2, 15),
        (3, 12), (4, 12), (3, 16), (4, 16),
        (5, 13), (5, 14), (5, 15), (6, 14),
        (7, 12), (8, 12), (7, 13), (8, 13),
        (7, 14), (8, 14), (6, 16), (7, 16), (8, 16),
        (9, 15),
    ]
    return left + [(y, x + 20) for y, x in right]


PATTERNS = {
    'Block': [(0, 0), (0, 1), (1, 0), (1, 1)],
    'Beehive': [(0, 1), (0, 2), (1, 0), (1, 3), (2, 1), (2, 2)],
    'Blinker': [(1, 0), (1, 1), (1, 2)],
    'Toad': [(1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2)],
    'Beacon': [(0, 0), (0, 1), (1, 0), (3, 2), (3, 3), (2, 3)],
    'Pulsar': [
        (2, 4), (2, 5), (2, 6), (2, 10), (2, 11), (2, 12),
        (4, 2), (4, 7), (4, 9), (4, 14),
        (5, 2), (5, 7), (5, 9), (5, 14),
        (6, 2), (6, 7), (6, 9), (6, 14),
        (7, 4), (7, 5), (7, 6), (7, 10), (7, 11), (7, 12),
        (9, 4), (9, 5), (9, 6), (9, 10), (9, 11), (9, 12),
        (10, 2), (10, 7), (10, 9), (10, 14),
        (11, 2), (11, 7), (11, 9), (11, 14),
        (12, 2), (12, 7), (12, 9), (12, 14),
        (4, 4), (4, 5), (4, 6), (4, 10), (4, 11), (4, 12),
        (12, 4), (12, 5), (12, 6), (12, 10), (12, 11), (12, 12),
    ],
    'Glider': [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
    'LWSS': [
        (0, 1), (0, 4),
        (1, 0),
        (2, 0), (2, 4),
        (3, 0), (3, 1), (3, 2), (3, 3),
    ],
    'MWSS': [
        (0, 2), (0, 5),
        (1, 0), (1, 5),
        (2, 0), (2, 5),
        (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
    ],
    'HWSS': [
        (0, 3), (0, 7),
        (1, 0), (1, 7),
        (2, 0), (2, 7),
        (3, 0), (3, 8),
        (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7),
    ],
    'Pentomino (R)': [(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)],
    'Acorn': [(0, 1), (1, 3), (2, 0), (2, 1), (2, 4), (2, 5), (2, 6)],
    'Diehard': [(0, 6), (1, 0), (1, 1), (2, 1), (2, 5), (2, 6), (2, 7)],
    'Glider Gun': _gosper_gun_cells(),
}

PATTERN_NAMES = list(PATTERNS.keys())


# ----------------------------------------------------------------------
# Curses helpers (aligned with snake.py)
# ----------------------------------------------------------------------
def safe_addch(stdscr, y, x, ch):
    max_y, max_x = stdscr.getmaxyx()
    if y < 0 or x < 0 or y >= max_y or x >= max_x:
        return
    if y == max_y - 1 and x == max_x - 1:
        return
    try:
        stdscr.addch(y, x, ch)
    except curses.error:
        pass


def safe_addstr(stdscr, y, x, text):
    max_y, max_x = stdscr.getmaxyx()
    if y < 0 or y >= max_y or x >= max_x:
        return
    try:
        stdscr.addstr(y, x, text[: max(0, max_x - x - 1)])
    except curses.error:
        pass


def get_grid_size(stdscr):
    """Inner grid (rows, cols); reserve rows for status + help hint."""
    term_h, term_w = stdscr.getmaxyx()
    status_rows = 3
    return max(5, term_h - status_rows - 2), max(5, term_w - 4)


def init_screen(stdscr, delay_ms):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(delay_ms)
    stdscr.clear()
    stdscr.refresh()
    return stdscr


# ----------------------------------------------------------------------
# Simulation core
# ----------------------------------------------------------------------
class LifeState:
    """Grid state, ages, statistics, and evolution."""

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.alive = set()
        self.ages = {}
        self.generation = 0
        self.births_total = 0
        self.deaths_total = 0
        self.last_population = 0
        self.stable_generations = 0
        self._prev_hash = None
        self.torus = True
        self.rules_name = RULESET_NAMES[0]
        self.birth, self.survive = RULESETS[self.rules_name]

    def resize(self, height, width):
        self.height = height
        self.width = width
        self.alive = {(y, x) for y, x in self.alive if 0 <= y < height and 0 <= x < width}
        self.ages = {p: a for p, a in self.ages.items() if p in self.alive}

    def clear(self):
        self.alive.clear()
        self.ages.clear()
        self.generation = 0
        self.births_total = 0
        self.deaths_total = 0
        self.last_population = 0
        self.stable_generations = 0
        self._prev_hash = None

    def toggle_cell(self, y, x):
        if not (0 <= y < self.height and 0 <= x < self.width):
            return
        if (y, x) in self.alive:
            self.alive.remove((y, x))
            self.ages.pop((y, x), None)
        else:
            self.alive.add((y, x))
            self.ages[(y, x)] = 0

    def set_cell(self, y, x, alive):
        if not (0 <= y < self.height and 0 <= x < self.width):
            return
        if alive:
            self.alive.add((y, x))
            self.ages.setdefault((y, x), 0)
        elif (y, x) in self.alive:
            self.alive.remove((y, x))
            self.ages.pop((y, x), None)

    def random_fill(self, density=0.25):
        self.clear()
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < density:
                    self.alive.add((y, x))
                    self.ages[(y, x)] = 0

    def place_pattern(self, cells, anchor_y, anchor_x, clear_area=False):
        if clear_area:
            for dy, dx in cells:
                self.set_cell(anchor_y + dy, anchor_x + dx, False)
        for dy, dx in cells:
            self.set_cell(anchor_y + dy, anchor_x + dx, True)

    def cycle_ruleset(self, direction=1):
        idx = RULESET_NAMES.index(self.rules_name)
        idx = (idx + direction) % len(RULESET_NAMES)
        self.rules_name = RULESET_NAMES[idx]
        self.birth, self.survive = RULESETS[self.rules_name]

    def _wrap(self, y, x):
        if self.torus:
            return y % self.height, x % self.width
        return y, x

    def _in_bounds(self, y, x):
        return 0 <= y < self.height and 0 <= x < self.width

    def neighbor_count(self, y, x):
        count = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                ny, nx = y + dy, x + dx
                if self.torus:
                    ny, nx = ny % self.height, nx % self.width
                elif not self._in_bounds(ny, nx):
                    continue
                if (ny, nx) in self.alive:
                    count += 1
        return count

    def _cells_to_consider(self):
        candidates = set(self.alive)
        for y, x in self.alive:
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dy == 0 and dx == 0:
                        continue
                    ny, nx = y + dy, x + dx
                    if self.torus:
                        candidates.add((ny % self.height, nx % self.width))
                    elif self._in_bounds(ny, nx):
                        candidates.add((ny, nx))
        return candidates

    def step(self):
        birth_set = set()
        survive_set = set()
        deaths = 0
        births = 0

        for y, x in self._cells_to_consider():
            n = self.neighbor_count(y, x)
            alive = (y, x) in self.alive
            if alive:
                if n in self.survive:
                    survive_set.add((y, x))
                else:
                    deaths += 1
            elif n in self.birth:
                birth_set.add((y, x))
                births += 1

        new_alive = birth_set | survive_set
        new_ages = {}
        for cell in new_alive:
            if cell in self.alive:
                new_ages[cell] = self.ages.get(cell, 0) + 1
            else:
                new_ages[cell] = 0

        self.alive = new_alive
        self.ages = new_ages
        self.generation += 1
        self.births_total += births
        self.deaths_total += deaths

        pop = len(self.alive)
        state_hash = (pop, frozenset(self.alive))
        if state_hash == self._prev_hash:
            self.stable_generations += 1
        else:
            self.stable_generations = 0
        self._prev_hash = state_hash
        self.last_population = pop

        return births, deaths, pop


# ----------------------------------------------------------------------
# UI state
# ----------------------------------------------------------------------
class UI:
    def __init__(self):
        self.cursor_y = 0
        self.cursor_x = 0
        self.running = False
        self.show_age = True
        self.pattern_index = 0
        self.draw_mode = True  # True = draw, False = erase
        self.brush = 1
        self.delay_ms = DEFAULT_DELAY_MS
        self.message = ''
        self.message_ttl = 0
        self.show_help = False

    def set_message(self, text, ttl=80):
        self.message = text
        self.message_ttl = ttl

    def tick_message(self):
        if self.message_ttl > 0:
            self.message_ttl -= 1
            if self.message_ttl == 0:
                self.message = ''


def cell_char(state, y, x, ui):
    if (y, x) not in state.alive:
        return DEAD
    if not ui.show_age:
        return ALIVE
    age = state.ages.get((y, x), 0)
    if age <= 2:
        return ALIVE_YOUNG
    if age <= 10:
        return ALIVE_MATURE
    return ALIVE_OLD


def draw_frame(stdscr, state, ui, grid_h, grid_w, offset_y, offset_x):
    stdscr.clear()

    # Border
    for x in range(grid_w + 2):
        safe_addch(stdscr, offset_y - 1, offset_x - 1 + x, BORDER_H if x else BORDER_CORNER)
        safe_addch(stdscr, offset_y + grid_h, offset_x - 1 + x, BORDER_H)
    for y in range(grid_h):
        safe_addch(stdscr, offset_y + y, offset_x - 1, BORDER)
        safe_addch(stdscr, offset_y + y, offset_x + grid_w, BORDER)

    for y in range(grid_h):
        for x in range(grid_w):
            ch = cell_char(state, y, x, ui)
            cy, cx = offset_y + y, offset_x + x
            if y == ui.cursor_y and x == ui.cursor_x:
                ch = CURSOR_ON if (y, x) in state.alive else CURSOR
            safe_addch(stdscr, cy, cx, ch)

    draw_status(stdscr, state, ui, grid_h, grid_w, offset_y)
    stdscr.refresh()


def draw_status(stdscr, state, ui, grid_h, grid_w, offset_y):
    term_h, term_w = stdscr.getmaxyx()
    status_y = offset_y + grid_h + 1

    mode = 'RUN' if ui.running else 'PAUSE'
    topo = 'Torus' if state.torus else 'Rand'
    draw = 'Zeichnen' if ui.draw_mode else 'Radieren'
    pat = PATTERN_NAMES[ui.pattern_index]

    line1 = (
        f" Gen {state.generation}  Pop {len(state.alive)}  "
        f"+{state.births_total} -{state.deaths_total}  [{mode}]  {state.rules_name[:28]}"
    )
    line2 = (
        f" {topo}  {draw}  Pinsel {ui.brush}  Muster: {pat[:20]}  "
        f"Geschw {ui.delay_ms}ms  Alter:{'an' if ui.show_age else 'aus'}"
    )
    hint = ' Leertaste=Start/Stop  .=Schritt  h=Hilfe  q=Beenden '

    safe_addstr(stdscr, status_y, 1, line1[: term_w - 2])
    safe_addstr(stdscr, status_y + 1, 1, line2[: term_w - 2])
    if ui.message:
        safe_addstr(stdscr, status_y, max(1, term_w - len(ui.message) - 2), ui.message[:40])
    if state.stable_generations >= 2:
        safe_addstr(stdscr, status_y + 1, max(1, term_w - 22), '[ stabil? ]')
    safe_addstr(stdscr, min(term_h - 1, status_y + 2), 1, hint[: term_w - 2])


def draw_help_overlay(stdscr):
    stdscr.clear()
    term_h, term_w = stdscr.getmaxyx()
    lines = [
        ' === Game of Life — Steuerung === ',
        '',
        ' Pfeile / WASD     Cursor bewegen',
        ' Leertaste         Simulation starten/stoppen',
        ' . oder n          Ein Schritt (wenn pausiert)',
        ' Enter / e         Zelle umschalten',
        ' f                 Pinsel am Cursor anwenden',
        ' x                 Pinsel-Modus: zeichnen/radieren',
        ' c                 Alles löschen',
        ' r                 Zufällig füllen (25 %)',
        ' R                 Zufällig füllen (40 %)',
        ' p                 Muster am Cursor platzieren',
        ' [ / ]             Vorheriges / nächstes Muster',
        ' o / O             Regelwerk vor/zurück',
        ' t                 Torus (Randlos) an/aus',
        ' g                 Zellalter-Farben an/aus',
        ' + / -             Schneller / langsamer',
        ' 1..9              Pinselgröße',
        ' z                 Zentrum: Glider',
        ' Z                 Zentrum: Gosper-Gun (großes Feld)',
        ' h / ?             Diese Hilfe',
        ' q / ESC           Beenden',
        '',
        ' Fenstergröße ändern passt das Raster an.',
        '',
        ' [ beliebige Taste zum Schließen ] ',
    ]
    start_y = max(0, term_h // 2 - len(lines) // 2)
    for i, line in enumerate(lines):
        y = start_y + i
        if y >= term_h:
            break
        x = max(0, (term_w - len(line)) // 2)
        safe_addstr(stdscr, y, x, line)
    stdscr.refresh()
    stdscr.nodelay(False)
    stdscr.getch()
    stdscr.nodelay(True)


def apply_brush(state, cy, cx, alive, radius):
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if abs(dy) + abs(dx) <= radius + (1 if radius else 0):
                state.set_cell(cy + dy, cx + dx, alive)


def move_cursor(ui, state, dy, dx):
    ui.cursor_y = (ui.cursor_y + dy) % state.height
    ui.cursor_x = (ui.cursor_x + dx) % state.width


def handle_key(key, stdscr, state, ui):
    if key == -1:
        return True

    if ui.show_help:
        return True

    if key in (ord('q'), ord('Q'), 27):
        return False

    if key in (ord('h'), ord('H'), ord('?')):
        ui.show_help = True
        draw_help_overlay(stdscr)
        ui.show_help = False
        stdscr.timeout(ui.delay_ms)
        return True

    if key == ord(' '):
        ui.running = not ui.running
        ui.set_message('Simulation läuft' if ui.running else 'Pausiert')
        return True

    if key in (ord('.'), ord('n'), ord('N')):
        if not ui.running:
            b, d, p = state.step()
            ui.set_message(f'Schritt: +{b} -{d} → {p}')
        return True

    if key in (curses.KEY_UP, ord('w'), ord('W')):
        move_cursor(ui, state, -1, 0)
    elif key in (curses.KEY_DOWN, ord('s'), ord('S')):
        move_cursor(ui, state, 1, 0)
    elif key in (curses.KEY_LEFT, ord('a'), ord('A')):
        move_cursor(ui, state, 0, -1)
    elif key in (curses.KEY_RIGHT, ord('d'), ord('D')):
        move_cursor(ui, state, 0, 1)

    if key in (10, 13, ord('e'), ord('E')):
        state.toggle_cell(ui.cursor_y, ui.cursor_x)

    if key == ord('x'):
        ui.draw_mode = not ui.draw_mode
        ui.set_message('Zeichnen' if ui.draw_mode else 'Radieren')

    if key in (ord('c'), ord('C')):
        state.clear()
        ui.running = False
        ui.set_message('Gitter geleert')

    if key == ord('r'):
        state.random_fill(0.25)
        ui.running = False
        ui.set_message('25 % Zufallsfüllung')

    if key == ord('R'):
        state.random_fill(0.40)
        ui.running = False
        ui.set_message('40 % Zufallsfüllung')

    if key == ord('p'):
        name = PATTERN_NAMES[ui.pattern_index]
        state.place_pattern(PATTERNS[name], ui.cursor_y, ui.cursor_x)
        ui.set_message(f'Muster „{name}" platziert')

    if key == ord('['):
        ui.pattern_index = (ui.pattern_index - 1) % len(PATTERN_NAMES)
        ui.set_message(PATTERN_NAMES[ui.pattern_index])

    if key == ord(']'):
        ui.pattern_index = (ui.pattern_index + 1) % len(PATTERN_NAMES)
        ui.set_message(PATTERN_NAMES[ui.pattern_index])

    if key == ord('o'):
        state.cycle_ruleset(1)
        ui.set_message(state.rules_name)

    if key == ord('O'):
        state.cycle_ruleset(-1)
        ui.set_message(state.rules_name)

    if key == ord('t'):
        state.torus = not state.torus
        ui.set_message(f'Topologie: {"Torus" if state.torus else "Begrenzt"}')

    if key == ord('g'):
        ui.show_age = not ui.show_age

    if key in (ord('+'), ord('=')):
        ui.delay_ms = max(MIN_DELAY_MS, ui.delay_ms - 30)
        stdscr.timeout(ui.delay_ms)
        ui.set_message(f'{ui.delay_ms} ms')

    if key in (ord('-'), ord('_')):
        ui.delay_ms = min(MAX_DELAY_MS, ui.delay_ms + 30)
        stdscr.timeout(ui.delay_ms)
        ui.set_message(f'{ui.delay_ms} ms')

    if ord('1') <= key <= ord('9'):
        ui.brush = key - ord('0')
        ui.set_message(f'Pinsel {ui.brush}')

    if key == ord('z'):
        cy, cx = state.height // 2, state.width // 2
        state.place_pattern(PATTERNS['Glider'], cy, cx)
        ui.cursor_y, ui.cursor_x = cy, cx
        ui.set_message('Glider in der Mitte')

    if key == ord('Z'):
        if state.height >= 12 and state.width >= 40:
            cy, cx = state.height // 2 - 5, max(0, state.width // 2 - 20)
            state.clear()
            state.place_pattern(PATTERNS['Glider Gun'], cy, cx)
            ui.cursor_y, ui.cursor_x = cy, cx
            ui.set_message('Gosper-Glider-Gun platziert')
        else:
            ui.set_message('Terminal zu klein für Gun (mind. ~40×12)')

    if not ui.running and key in (ord('f'), ord('F')):
        apply_brush(state, ui.cursor_y, ui.cursor_x, ui.draw_mode, ui.brush - 1)

    return True


def show_exit_summary(stdscr, state):
    stdscr.nodelay(False)
    stdscr.clear()
    term_h, term_w = stdscr.getmaxyx()
    lines = [
        ' Session beendet ',
        '',
        f' Generationen: {state.generation}',
        f' Lebende Zellen: {len(state.alive)}',
        f' Geburten gesamt: {state.births_total}',
        f' Tode gesamt: {state.deaths_total}',
        f' Regelwerk: {state.rules_name}',
        '',
        ' [ Enter zum Schließen ] ',
    ]
    start_y = max(0, term_h // 2 - len(lines) // 2)
    for i, line in enumerate(lines):
        y = start_y + i
        x = max(0, (term_w - len(line)) // 2)
        safe_addstr(stdscr, y, x, line)
    stdscr.refresh()
    stdscr.getch()


def run_session(stdscr):
    stdscr = init_screen(stdscr, DEFAULT_DELAY_MS)
    grid_h, grid_w = get_grid_size(stdscr)
    state = LifeState(grid_h, grid_w)
    ui = UI()
    ui.cursor_y = grid_h // 2
    ui.cursor_x = grid_w // 2

    # Start with a small blinker in the center
    state.place_pattern(PATTERNS['Blinker'], grid_h // 2 - 1, grid_w // 2 - 1)
    offset_y, offset_x = 2, 2

    last_size = (grid_h, grid_w)

    while True:
        term_h, term_w = stdscr.getmaxyx()
        new_h, new_w = get_grid_size(stdscr)
        if (new_h, new_w) != last_size:
            state.resize(new_h, new_w)
            grid_h, grid_w = new_h, new_w
            ui.cursor_y = min(ui.cursor_y, grid_h - 1)
            ui.cursor_x = min(ui.cursor_x, grid_w - 1)
            last_size = (grid_h, grid_w)
            ui.set_message(f'Raster {grid_w}×{grid_h}')

        key = stdscr.getch()
        if not handle_key(key, stdscr, state, ui):
            break

        if ui.running:
            state.step()

        ui.tick_message()
        draw_frame(stdscr, state, ui, grid_h, grid_w, offset_y, offset_x)

    show_exit_summary(stdscr, state)


def main(stdscr):
    run_session(stdscr)


if __name__ == '__main__':
    curses.wrapper(main)
