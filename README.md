# cli-demos

Sammlung von **Spielen und Simulationen für die Kommandozeile** — auf dem PC als Python-Terminalprogramme (`curses`) und auf klassischen Commodore-Rechnern als BASIC-Demos.

## Übersicht

| Plattform | Programm | Beschreibung |
|-----------|----------|--------------|
| PC | [Snake](pc/snake.py) | Klassisches Snake-Spiel, Spielfeld passt sich der Terminalgröße an |
| PC | [Tetris](pc/tetris.py) | Tetris mit Hold, Ghost-Piece, Next-Vorschau und Level-System |
| PC | [2D Game of Life](pc/2d_game_of_life.py) | Conway’s Game of Life mit Editor, Mustern und mehreren Regelwerken |
| C64 | [2D Game of Life](c64/2d_game_of_life.bas) | 40×23; **extrem langsam** (reines BASIC) |
| C64 | [1D Game of Life](c64/1d_game_of_life.bas) | Millen/BYTE 1D-Life, Evolution-Ansicht |
| C16 | [2D Game of Life](c16/2d_game_of_life.bas) | TED; **extrem langsam**; schwarz + Boot-Lila |
| C16 | [1D Game of Life](c16/1d_game_of_life.bas) | Millen/BYTE 1D-Life, Evolution-Ansicht |
| C128 | [2D Game of Life (VIC-II)](c128/2d_game_of_life_vic2-40.bas) | 40 Spalten; **extrem langsam** |
| C128 | [1D Game of Life (VIC-II)](c128/1d_game_of_life_vic2-40.bas) | 1D-Life, 40 Spalten VIC-II |
| C128 | [2D Game of Life (VDC)](c128/2d_game_of_life_vdc-80.bas) | 80 Spalten VDC; **extrem langsam** |
| C128 | [1D Game of Life (VDC)](c128/1d_game_of_life_vdc-80.bas) | 1D-Life, 80 Spalten VDC |
| MEGA65 | [2D Game of Life](mega65/2d_game_of_life_80.bas) | 80×25 Text; auf Hardware getestet |
| MEGA65 | [1D Game of Life](mega65/1d_game_of_life_80.bas) | 1D-Life, 80 Spalten, Evolution-Ansicht |

## Verzeichnisstruktur

```
cli-demos/
├── README.md
├── pc/                          # Python 3, nur Standardbibliothek (+ curses)
│   ├── snake.py
│   ├── tetris.py
│   └── 2d_game_of_life.py
├── c64/
│   ├── 2d_game_of_life.bas       # Commodore 64 BASIC V2
│   └── 1d_game_of_life.bas       # 1D Life (Millen)
├── c16/
│   ├── 2d_game_of_life.bas       # C16 / Plus/4 BASIC 3.5 (TED)
│   └── 1d_game_of_life.bas       # 1D Life (Millen), Evolution-Ansicht
├── c128/
│   ├── 2d_game_of_life_vic2-40.bas  # C128 BASIC, VIC-II 40 Spalten
│   ├── 1d_game_of_life_vic2-40.bas  # 1D Life, VIC-II 40
│   ├── 2d_game_of_life_vdc-80.bas   # C128 BASIC, VDC 80 Spalten
│   └── 1d_game_of_life_vdc-80.bas   # 1D Life, VDC 80
└── mega65/
    ├── 2d_game_of_life_80.bas    # MEGA65, BASIC 65, 80×25 Text
    ├── 1d_game_of_life_80.bas    # 1D Life, 80 Spalten
    ├── 2d_game_of_life_80.prg
    └── 2d_game_of_life.d81
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
python3 pc/2d_game_of_life.py
```

Das Terminal sollte ausreichend groß sein (mindestens ca. 80×24 Zeichen für Tetris und 2D Game of Life; kleinere Fenster funktionieren teilweise mit eingeschränktem Layout).

### Gemeinsame Hinweise

- **Unicode-Zeichen** (Blöcke, Rahmen) werden für Darstellung genutzt; die Terminal-Schriftart sollte UTF-8 unterstützen.
- **Fenstergröße**: Snake und 2D Game of Life passen das Raster an die aktuelle Terminalgröße an; Tetris skaliert Zellenbreite/-höhe nach verfügbarem Platz.
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

### 2D Game of Life (`pc/2d_game_of_life.py`)

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

**2D:** Conway’s Game of Life (B3/S23) als Endlosschleife mit **simultanem Update** (Doppelpuffer): Zufallsstart (RNG **15–20 %**) plus zwei Glider; `POP`/`GEN`; Neustart nach **20** Gen. Auf **C64 / C16 / C128 extrem langsam** (reine BASIC-Schleifen über das ganze Gitter); auf dem **MEGA65 getestet und lauffähig** (`SPEED`).

**1D:** Millen/BYTE-Life ([jonmillen.com/1dlife](https://jonmillen.com/1dlife/index.html)), Nachbarschaft `YYXYY`, Evolution-Ansicht (jede Gen. eine Zeile), Wrap-Ring, Seed **28–35 %**, Status `POP` / `SEED` / `GEN`, Neustart nach **20** Gen.

### Commodore 64 — `c64/2d_game_of_life.bas`

- **Extrem langsam** — jede Generation rechnet das volle 40×23-Gitter in BASIC
- **Auflösung:** 40×23 aktive Zellen (Zeilen 1–23), Zeile 24 leer, Zeile 25 Status
- **Darstellung:** POKE in Bildschirm- (`1024`) und Farbspeicher (`55296`), invertierte Blöcke
- **Start:** Zwei Glider aus `DATA`-Zeilen + Zufallsbelegung **15–20 %** (138–184 Zellen); alle **20 Gen.** Neustart

**Emulator (z. B. VICE):**

1. `x64` starten, BASIC laden: `.load"2d_game_of_life.bas",8` oder Datei per Drag & Drop
2. `RUN`

### Commodore 64 — 1D — `c64/1d_game_of_life.bas`

- 40er-Ring, Evolution-Ansicht, schwarzer Rahmen/Hintergrund
- Laden und `RUN` wie die 2D-Variante

### Commodore 16 / Plus/4 — `c16/2d_game_of_life.bas`

- **Extrem langsam** (BASIC über 40×23)
- **40×23** wie C64; TED-Screen `3072`, Farbe `2048`
- **Farben:** Hintergrund/Rahmen schwarz; Vordergrund echtes C16-Boot-Lila (`COLOR 1,15,6` = TED `$6E` aus dem Kernal, nicht Purple/5)
- Kompakte Arrays (16 K-tauglich); Zufallsfüllung **15–20 %**; Neustart nach **20** Gen.
- **VICE:** `xplus4` oder C16, Programm laden und `RUN`

### Commodore 16 / Plus/4 — 1D — `c16/1d_game_of_life.bas`

- **1D Life** nach Millen/BYTE (Nachbarschaft `YYXYY`): Geburt bei 2–3 Y-Nachbarn, Überleben bei 2 oder 4; 40er-Ring
- **Evolution-Ansicht:** jede Generation eine Bildschirmzeile (Space-Time), wie Default auf [jonmillen.com/1dlife](https://jonmillen.com/1dlife/index.html)
- Gleiche TED-Farben wie die 2D-C16-Demo; Zufalls-Seed **28–35 %**; Neustart nach **20** Gen.
- **VICE:** `xplus4` oder C16, laden und `RUN`

### Commodore 128 — VIC-II 40 Spalten

- 2D: [`c128/2d_game_of_life_vic2-40.bas`](c128/2d_game_of_life_vic2-40.bas) — **extrem langsam**
- 1D: [`c128/1d_game_of_life_vic2-40.bas`](c128/1d_game_of_life_vic2-40.bas)
- **Wichtig:** Nur **40-Spalten-VIC-II** — 80-Spalten aus; in VICE VIC-Ansicht
- `SLOW` (nicht `FAST` — sonst bleibt der VIC-Screen schwarz); Integer-Arrays; 2D: Seed **15–20 %**; 1D: Seed **28–35 %**; Neustart nach **20** Gen.

### Commodore 128 — VDC 80 Spalten

- 2D: [`c128/2d_game_of_life_vdc-80.bas`](c128/2d_game_of_life_vdc-80.bas) — **extrem langsam** (auch mit FAST)
- 1D: [`c128/1d_game_of_life_vdc-80.bas`](c128/1d_game_of_life_vdc-80.bas) — 80er-Ring, Evolution-Ansicht
- FAST 2 MHz; VDC-Schreiben mit voller Adresse (stabil)
- **VICE:** Zuerst **80col / VDC-Fenster** aktivieren (sonst bleibt der VIC-40-Screen leer/grün).

### MEGA65 — 80 Spalten

- 2D: [`mega65/2d_game_of_life_80.bas`](mega65/2d_game_of_life_80.bas) — **funktioniert auf Hardware**; **80×23**, `SPEED`, `T@&`, natives Blau/Weiß; Seed **15–20 %**
- 1D: [`mega65/1d_game_of_life_80.bas`](mega65/1d_game_of_life_80.bas) — 80er-Ring, Evolution-Ansicht; Seed **28–35 %**
- Schaltet bei Bedarf per ESC 8 auf 80 Spalten; Neustart nach **20** Gen.
- Disk (2D): [`mega65/2d_game_of_life.d81`](mega65/2d_game_of_life.d81) / PRG [`mega65/2d_game_of_life_80.prg`](mega65/2d_game_of_life_80.prg)
- **Hardware/Xemu:** Programm laden und `RUN` (80×25 Text)

---

## Entwicklung & Beiträge

- PC-Code: nur Standardbibliothek; keine `requirements.txt` nötig (außer `windows-curses` unter Windows).
- Commodore-/MEGA65-Code: in **VICE**, **Xemu** oder auf echter Hardware testen; Pfade beim Laden an das jeweilige Medium (Diskette, `.d64`, SD2IEC, SD-Karte) anpassen.
- Änderungen an Spielregeln oder Layout: jeweilige Datei enthält Konfigurationskonstanten und Kommentare am Dateianfang.

## Lizenz

Keine Lizenzdatei im Repository — bei Weitergabe oder Veröffentlichung bitte eine passende Lizenz ergänzen oder mit dem Maintainer klären.
