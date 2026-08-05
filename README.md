# cli-demos

Sammlung von **Spielen für die Kommandozeile** (Python/`curses`).

Game-of-Life-Demos (PC + Commodore/MEGA65) liegen im separaten Repo **[game-of-life](https://github.com/oe3gwu/game-of-life)**.

## Übersicht

| Plattform | Programm | Beschreibung |
|-----------|----------|--------------|
| PC | [Snake](pc/snake.py) | Klassisches Snake-Spiel, Spielfeld passt sich der Terminalgröße an |
| PC | [Tetris](pc/tetris.py) | Tetris mit Hold, Ghost-Piece, Next-Vorschau und Level-System |

## Verzeichnisstruktur

```
cli-demos/
├── README.md
└── pc/                          # Python 3, nur Standardbibliothek (+ curses)
    ├── snake.py
    └── tetris.py
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

```bash
python3 pc/snake.py
python3 pc/tetris.py
```

Das Terminal sollte ausreichend groß sein (mindestens ca. 80×24 Zeichen für Tetris; kleinere Fenster funktionieren teilweise mit eingeschränktem Layout).

### Gemeinsame Hinweise

- **Unicode-Zeichen** (Blöcke, Rahmen) werden für Darstellung genutzt; die Terminal-Schriftart sollte UTF-8 unterstützen.
- **Fenstergröße**: Snake passt das Raster an die aktuelle Terminalgröße an; Tetris skaliert Zellenbreite/-höhe nach verfügbarem Platz.
- Beenden: meist **`Q`** oder **ESC**; nach Game Over Neustart mit **`R`**.

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

## Lizenz

Keine Lizenzdatei im Repository — bei Weitergabe oder Veröffentlichung bitte eine passende Lizenz ergänzen oder mit dem Maintainer klären.
