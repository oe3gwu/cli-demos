# cli-demos

Sammlung von **Spielen und Simulationen für die Kommandozeile** — auf dem PC als Python-Terminalprogramme (`curses`) und auf klassischen Commodore-Rechnern als BASIC-Demos.

## Übersicht

| Plattform | Programm | Beschreibung |
|-----------|----------|--------------|
| PC | [Snake](pc/snake.py) | Klassisches Snake-Spiel, Spielfeld passt sich der Terminalgröße an |
| PC | [Tetris](pc/tetris.py) | Tetris mit Hold, Ghost-Piece, Next-Vorschau und Level-System |
| PC | [Game of Life](pc/game_of_life.py) | Conway’s Game of Life mit Editor, Mustern und mehreren Regelwerken |
| C64 | [Game of Life](c64/game_of_life.bas) | Automatische Simulation, 40×23 Spielfeld, Statuszeile |
| C128 | [Game of Life (VIC-II)](c128/game_of_life_vic2-40.bas) | Wie C64, 40 Spalten im VIC-II-Fenster |
| C128 | [Game of Life (VDC)](c128/game_of_life_vdc-80.bas) | 80 Spalten über den VDC-Chip (Graphics 5) |

## Verzeichnisstruktur

```
cli-demos/
├── README.md
├── pc/                          # Python 3, nur Standardbibliothek (+ curses)
│   ├── snake.py
│   ├── tetris.py
│   └── game_of_life.py
├── c64/
│   └── game_of_life.bas         # Commodore 64 BASIC V2
└── c128/
    ├── game_of_life_vic2-40.bas # C128, VIC-II 40 Spalten
    └── game_of_life_vdc-80.bas  # C128, VDC 80 Spalten
```

---

## PC-Demos (Python 3)

### Voraussetzungen

- **Python 3.8+** (empfohlen)
- Ein echtes Terminal (nicht nur eine IDE-Konsole ohne Tastatur- und Größenunterstützung)
- Unter **Linux/macOS**: Modul `curses` ist in der Standardbibliothek enthalten
- Unter **Windows**: zusätzlich installieren:

  ```bash
  pip install windows-curses
  ```

### Starten

Alle PC-Programme vom Repository-Root aus starten:

```bash
python3 pc/snake.py
python3 pc/tetris.py
python3 pc/game_of_life.py
```

Das Terminal sollte ausreichend groß sein (mindestens ca. 80×24 Zeichen für Tetris und Game of Life; kleinere Fenster funktionieren teilweise mit eingeschränktem Layout).

### Gemeinsame Hinweise

- **Unicode-Zeichen** (Blöcke, Rahmen) werden für Darstellung genutzt; die Terminal-Schriftart sollte UTF-8 unterstützen.
- **Fenstergröße**: Snake und Game of Life passen das Raster an die aktuelle Terminalgröße an; Tetris skaliert Zellenbreite/-höhe nach verfügbarem Platz.
- Beenden: meist **`Q`** oder **ESC**; Tetris und Snake bieten nach Game Over ein Neustart-Menü (**`R`**).

---

### Snake (`pc/snake.py`)

Einfaches Snake-Spiel im Terminal.

| Taste | Aktion |
|-------|--------|
| Pfeiltasten / **W A S D** | Richtung ändern |
| **Q** / ESC | Spiel beenden |
| **R** (nach Game Over) | Neustart |
| **Q** (nach Game Over) | Beenden |

- Kollision mit Wand oder eigenem Schwanz beendet die Runde.
- Punkte steigen pro gefressenem Futter (`*`).

---

### Tetris (`pc/tetris.py`)

Klassisches Tetris mit 10×20-Spielfeld, 7-Bag-Randomizer, Hold, Ghost-Piece und Vorschau der nächsten Steine.

| Taste | Aktion |
|-------|--------|
| ← → / **A D** | Stein bewegen |
| ↑ / **W** | Drehen |
| ↓ / **S** | Soft Drop |
| Leertaste | Hard Drop |
| **F** / **H** | Hold |
| **C** | Farben ein/aus |
| **P** | Pause |
| **Q** / ESC | Beenden |
| **R** (nach Game Over) | Neustart |

Score, Zeilen und Level steigen mit gelöschten Reihen; die Fallgeschwindigkeit nimmt mit dem Level zu.

---

### Game of Life (`pc/game_of_life.py`)

Ausführliche Terminal-Version von **Conway’s Game of Life** mit Editor, Musterbibliothek und wählbaren Regelwerken (B/S-Notation).

**Funktionen:**

- Simulation mit Pause, Einzelschritt und variabler Geschwindigkeit
- Torus-Modus (randlos) oder begrenztes Gitter
- Muster: Block, Glider, Gosper-Gun, Pulsar, LWSS, u. a.
- Regelwerke: Conway, HighLife, Day & Night, Seeds, …
- Optional: Zellalter als unterschiedliche Zeichen
- Statistik (Population, Geburten/Tode, Stabilitätshinweis)

| Taste | Aktion |
|-------|--------|
| Pfeile / **W A S D** | Cursor |
| Leertaste | Simulation starten/stoppen |
| **.** / **N** | Ein Schritt (pausiert) |
| Enter / **E** | Zelle umschalten |
| **F** | Pinsel am Cursor |
| **X** | Zeichnen / Radieren |
| **C** | Gitter leeren |
| **R** / **r** | Zufallsfüllung (40 % / 25 %) |
| **P** | Muster platzieren |
| **[** / **]** | Muster wählen |
| **O** / **o** | Regelwerk wechseln |
| **T** | Torus an/aus |
| **G** | Zellalter-Anzeige |
| **+** / **-** | Geschwindigkeit |
| **1**–**9** | Pinselgröße |
| **Z** / **z** | Glider / Gosper-Gun in der Mitte |
| **H** / **?** | Hilfe |
| **Q** / ESC | Beenden |

---

## Commodore-Demos (BASIC)

Alle drei BASIC-Programme implementieren **Conway’s Game of Life (B3/S23)** als Endlosschleife: Zufallsstart plus zwei eingebettete Glider, Anzeige von **Population** und **Generation** in der untersten Zeile.

### Commodore 64 — `c64/game_of_life.bas`

- **Auflösung:** 40×23 aktive Zellen (Zeilen 1–23), Zeile 24 leer, Zeile 25 Status
- **Darstellung:** POKE in Bildschirm- (`1024`) und Farbspeicher (`55296`), invertierte Blöcke
- **Start:** Zwei Glider aus `DATA`-Zeilen + ca. 25 % Zufallsbelegung (230 Zellen)

**Emulator (z. B. VICE):**

1. `x64` starten, BASIC laden: `.load"game_of_life.bas",8` oder Datei per Drag & Drop
2. `RUN`

### Commodore 128 — VIC-II 40 Spalten — `c128/game_of_life_vic2-40.bas`

- Entspricht der C64-Version, angepasst für **BASIC 7** und C128
- **Wichtig:** Nur das **40-Spalten-VIC-II-Fenster** — **80-Spalten-Modus aus**
- In VICE: Graphics 0, VIC-Ansicht, 80 columns **off**

```text
GRAPHICS 0
RUN
```

### Commodore 128 — VDC 80 Spalten — `c128/game_of_life_vdc-80.bas`

- **80×23** Spielfeld über den **VDC** (`GRAPHICS 5`)
- CPU im **FAST**-Modus (2 MHz) für flüssigere Updates
- Schreibzugriffe über VDC-Register (`54784`/`54785`); ca. 25 % Zufallsfüllung (460 Zellen)
- **VICE:** C128, 80-Spalten-/VDC-Ansicht aktivieren, dann Programm laden und `RUN`

---

## Entwicklung & Beiträge

- PC-Code: nur Standardbibliothek; keine `requirements.txt` nötig (außer `windows-curses` unter Windows).
- Commodore-Code: in **VICE** oder auf echter Hardware testen; Pfade beim Laden an das jeweilige Medium (Diskette, `.d64`, SD2IEC) anpassen.
- Änderungen an Spielregeln oder Layout: jeweilige Datei enthält Konfigurationskonstanten und Kommentare am Dateianfang.

## Lizenz

Keine Lizenzdatei im Repository — bei Weitergabe oder Veröffentlichung bitte eine passende Lizenz ergänzen oder mit dem Maintainer klären.
