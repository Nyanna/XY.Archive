# HR-Plateau-Analyse

## Übersicht

Dieses Projekt extrahiert aus nächtlichen Herzfrequenzdaten (Xiaomi Smart Band 9 via Gadgetbridge) drei hierarchische Strukturebenen: **Nadirs**, **Phasen** und **Plateaus**. Ziel ist die Korrelation dieser Schlafarchitektur-Parameter mit epileptischen Anfällen (`seizures.csv`).

## Begriffsdefinitionen

### MHR10
Gleitender Mittelwert der Herzfrequenz über 10 Minuten (zentriert). Glättet Einzelschlag-Varianz und macht die Wellenstruktur der Nacht sichtbar. Basis aller weiteren Berechnungen.

### Nadir
Ein lokales Minimum der MHR10-Kurve. Markiert den tiefsten Punkt zwischen zwei HR-Hügeln. Nadirs sind die atomaren Bausteine der Analyse — sie definieren sowohl Phasengrenzen als auch Plateau-Zugehörigkeit.

**Detektionsparameter:**
- `min_depth=0.5` — Nadir muss mindestens 0.5 bpm tiefer liegen als die Umgebung (beidseitig)
- `min_dist=10` — Mindestabstand 10 Minuten zwischen zwei Nadirs
- Flache Böden (mehrere aufeinanderfolgende Minimalwerte) werden korrekt als ein Nadir erkannt

### Phase
Ein Zeitabschnitt zwischen zwei aufeinanderfolgenden Nadirs. Repräsentiert einen einzelnen HR-Hügel. Phasen sind die Grundeinheiten der Schlafzyklus-Analyse auf der schnellen Oszillatorebene.

### Plateau
Ein HR-Niveau, das durch einen oder mehrere Nadirs auf gleicher Höhe definiert wird. Plateaus repräsentieren die langsame Oszillatorebene — die Hüllkurve, auf der die schnellen Hügel (Phasen) reiten.

**Zwei Typen:**
- **Gruppen-Plateau**: Mehrere Nadirs mit ähnlichem MHR10-Wert (`n_nadirs > 1`), verbunden durch 1D-Merge-Tree-Konnektivität (die MHR10-Kurve unterschreitet ihr gemeinsames Niveau zwischen ihnen nicht)
- **Einzel-Plateau**: Ein einzelner Nadir, dessen Niveau sich von allen Nachbarn unterscheidet

**Plateau-Niveau (`level`):** Der MHR10-Wert des tiefsten Nadirs in der Gruppe. Definiert die horizontale Linie des Plateaus.

**Plateau-Grenzen (`start_time`, `end_time`):** Vom tiefsten Nadir aus wird die horizontale Linie bei `level` nach links und rechts verlängert, bis die MHR10-Kurve sie unterschreitet. Diese Schnittpunkte sind Start und Ende.

### Nadir-Konnektivität (1D Merge Tree)
Zwei Nadirs sind auf Plateau-Ebene verbunden, wenn die MHR10-Kurve zwischen ihnen nirgends unter das gemeinsame Niveau (den niedrigeren der beiden Nadir-Werte) fällt. Dies entspricht einem 1D-Merge-Tree (Topological Data Analysis): Beim schrittweisen Anheben eines Schwellwerts von unten verschmelzen benachbarte Bassins zu einem gemeinsamen Plateau, sobald der Schwellwert ihr trennendes Minimum erreicht. Dasselbe Prinzip findet sich als Watershed Transform in der Bildverarbeitung (dort auf 2D) und ist verwandt mit dem Prominenz-Begriff in Topographie und Signalverarbeitung.

### Stacktiefe (`stack_depth`)
Anzahl der Plateaus mit *niedrigerem* Niveau, die dieses Plateau zeitlich vollständig umschließen. Das tiefste Plateau der Nacht (Baseline) hat Stacktiefe 0. Höhere Plateaus, die innerhalb der Baseline liegen, haben Stacktiefe 1, usw. Die Stacktiefe bildet die hierarchische Verschachtelung der Plateaus ab.

### Nacht-Datum (`night_date`)
Das Datum des Aufwachzeitpunkts laut Schlafzusammenfassung. Eine Schlafphase, die am 12.12. beginnt und am 13.12. endet, hat `night_date = 2024-12-13`. Bei mehreren Schlafphasen pro Nacht wird die längste verwendet.

## Dateien

### `plateau_analysis.py`
Hauptskript. Liest die Gadgetbridge-SQLite-DB und `seizures.csv`, verarbeitet alle Nächte und schreibt drei CSV-Dateien.

**Ausführung:**
```bash
python3 plateau_analysis.py
```

**Voraussetzungen:**
- `Gadgetbridge` (SQLite-DB) unter `../`
- `seizures.csv` `../`
- Python-Pakete: `numpy`, `pandas` (Standardbibliothek: `sqlite3`, `zoneinfo`)

**Konfigurationskonstanten (oben im Script):**
| Konstante | Wert | Bedeutung |
|-----------|------|-----------|
| `TZ` | Europe/Berlin | Zeitzone für alle Zeitangaben |
| `MHR_WINDOW` | 10 | Fenstergröße des gleitenden Mittelwerts (Minuten) |
| `NADIR_MIN_DEPTH` | 0.5 | Mindest-Prominenz eines Nadirs (bpm) |
| `NADIR_MIN_DIST` | 10 | Mindestabstand zwischen Nadirs (Minuten) |
| `PLATEAU_TOL1` | 1.0 | Toleranz Pass 1: Nadir-Wert vs. Gruppenmittel (bpm) |
| `PLATEAU_TOL2` | 1.3 | Toleranz Pass 2: Singleton-Merge (bpm) |
| `MIN_SLEEP_DURATION` | 60 | Mindestdauer einer Schlafphase (Minuten) |

**Algorithmus-Pipeline pro Nacht:**
1. HR-Rohdaten aus `XIAOMI_ACTIVITY_SAMPLE` für das Schlafzeitfenster extrahieren
2. MHR10 berechnen (zentrierter 10-min Rolling Mean)
3. Nadirs detektieren (Custom-Finder mit Flat-Bottom-Handling)
4. Phasen zwischen konsekutiven Nadirs berechnen
5. Plateaus gruppieren (Zwei-Pass: erst tol=1.0 greedy temporal, dann Singleton-Merge bei tol=1.3)
6. Plateau-Grenzen via Merge-Tree-Konnektivität bestimmen
7. Stacktiefe berechnen

### `nadirs.csv`
Ein Nadir pro Zeile.

| Spalte | Typ | Beschreibung |
|--------|-----|-------------|
| `night_date` | date | Nacht-Datum (Aufwach-Tag) |
| `time` | HH:MM | Uhrzeit des Nadirs (Europe/Berlin) |
| `timestamp` | int | Unix-Epoch (Sekunden, UTC) |
| `mhr10` | float | MHR10-Wert am Nadir-Punkt (bpm) |

### `phases.csv`
Eine Phase pro Zeile. Phasen sind lückenlos und decken die gesamte Schlafzeit ab (inklusive Rand-Phasen vor dem ersten und nach dem letzten Nadir).

| Spalte | Typ | Beschreibung |
|--------|-----|-------------|
| `night_date` | date | Nacht-Datum |
| `start_time` | HH:MM | Beginn der Phase |
| `end_time` | HH:MM | Ende der Phase |
| `duration_min` | int | Dauer in Minuten |
| `hr_mean` | float | Mittlere Herzfrequenz (Rohdaten, nicht MHR10) |
| `hr_std` | float | Standardabweichung der HR innerhalb der Phase |

### `phases.csv` — Hinweise zur Interpretation
- `hr_mean` und `hr_std` werden aus den **Rohdaten** (1-Minuten-Takt) berechnet, nicht aus MHR10
- Die erste Phase beginnt am Schlafstart, die letzte endet am Schlafende
- Phasen mit hohem `hr_std` bei niedrigem `hr_mean` deuten auf Übergangszonen hin

### `plateaus.csv`
Ein Plateau pro Zeile.

| Spalte | Typ | Beschreibung |
|--------|-----|-------------|
| `night_date` | date | Nacht-Datum |
| `start_time` | HH:MM | Beginn des Plateaus (linker Schnittpunkt mit Hüllkurve) |
| `end_time` | HH:MM | Ende des Plateaus (rechter Schnittpunkt mit Hüllkurve) |
| `duration_min` | int | Dauer in Minuten |
| `level` | float | Plateau-Niveau = MHR10 des tiefsten Nadirs der Gruppe (bpm) |
| `n_nadirs` | int | Anzahl der Nadirs in dieser Plateau-Gruppe |
| `stack_depth` | int | Verschachtelungstiefe (0 = Baseline der Nacht) |

### `plateaus.csv` — Hinweise zur Interpretation
- `stack_depth=0` ist das tiefste Plateau der Nacht (oft nur 1 pro Nacht)
- Plateaus mit `n_nadirs=1` sind Einzel-Plateaus
- Plateaus können sich zeitlich überlappen (ein hohes Plateau liegt *innerhalb* eines tieferen)
- `level` ist nicht der mittlere HR auf dem Plateau, sondern das Nadir-Niveau — der tiefste Punkt der Hüllkurve innerhalb des Plateaus
- Die `duration_min` eines tiefen Plateaus kann die gesamte Nacht umfassen

## Visualisierung

### `render_charts.py`
Rendert interaktive HTML-Charts für eine einzelne Nacht. Liest die Gadgetbridge-DB (für Roh-HR und MHR10) sowie die generierten CSVs, füllt die HTML-Templates und schreibt zwei selbständige HTML-Dateien.

**Ausführung:**
```bash
python3 render_charts.py 2024-12-13
python3 render_charts.py 2024-12-13 --out-dir ../../../docs/charts
```

**Voraussetzungen:**
- `Gadgetbridge` (SQLite-DB) im selben Verzeichnis oder unter `../`
- `nadirs.csv`, `plateaus.csv` (generiert von `plateau_analysis.py`)
- `template_nadirs.html`, `template_plateaus.html`

**Ausgabe:**
- `nadirs_YYYY-MM-DD.html` — MHR10-Kurve mit HR-Rohdaten und Nadir-Markern
- `plateaus_YYYY-MM-DD.html` — MHR10-Kurve mit Plateau-Balken und Nadir-Anbindungen

Die generierten HTML-Dateien sind self-contained (Chart.js + chartjs-plugin-annotation via CDN) und direkt im Browser öffenbar. Hover-Tooltips zeigen Zeitpunkt und HR-Wert.

### `template_nadirs.html`
HTML-Template für den Nadir-Chart. Enthält zwei Platzhalter:

| Platzhalter | Ersetzung |
|-------------|-----------|
| `{{NIGHT_DATE}}` | Nacht-Datum als String (z.B. `2024-12-13`) |
| `{{DATA_JSON}}` | JSON-Objekt mit den Feldern `t`, `hr`, `m10`, `nadir_indices`, `y_min`, `y_max` |

**Datenstruktur `DATA_JSON`:**

| Feld | Typ | Beschreibung |
|------|-----|-------------|
| `t` | string[] | Zeitlabels im Format HH:MM, ein Eintrag pro Minute |
| `hr` | int[] | HR-Rohdaten (1-Minuten-Takt) |
| `m10` | float[]|null[] | MHR10-Werte, `null` an den Rändern (Rolling-Window-Padding) |
| `nadir_indices` | int[] | Indizes in die Arrays `t`/`m10`, die auf Nadirs zeigen |
| `y_min` | int | Untere Y-Achsen-Grenze (bpm) |
| `y_max` | int | Obere Y-Achsen-Grenze (bpm) |

**Darstellung:** HR-Rohdaten als blasse blaue Linie, MHR10 als kräftige blaue Linie, Nadirs als orangefarbene Punkte mit alternierend ober-/unterhalb platzierten Labels (Zeit + MHR10-Wert).

### `template_plateaus.html`
HTML-Template für den Plateau-Chart. Dieselben Platzhalter wie oben.

**Datenstruktur `DATA_JSON`:**

| Feld | Typ | Beschreibung |
|------|-----|-------------|
| `t` | string[] | Zeitlabels (identisch zum Nadir-Template) |
| `m10` | float[]|null[] | MHR10-Werte |
| `plateaus` | object[] | Liste der Plateau-Objekte (siehe unten) |
| `y_min` | int | Untere Y-Achsen-Grenze |
| `y_max` | int | Obere Y-Achsen-Grenze |

**Plateau-Objekt innerhalb `plateaus`:**

| Feld | Typ | Beschreibung |
|------|-----|-------------|
| `level` | float | Plateau-Niveau (bpm) |
| `n_nadirs` | int | Anzahl Nadirs in der Gruppe |
| `stack_depth` | int | Verschachtelungstiefe |
| `nadir_indices` | int[] | Indizes der zugehörigen Nadirs in `t`/`m10` |
| `start_idx` | int | Index in `t`/`m10` für den linken Hüllkurven-Schnittpunkt |
| `end_idx` | int | Index in `t`/`m10` für den rechten Hüllkurven-Schnittpunkt |

**Darstellung:** MHR10 als dezente Linie, Plateaus als farbcodierte horizontale Balken von `start_idx` bis `end_idx` (Hüllkurven-Schnittpunkte, nicht Nadir-Positionen). Durchgezogen für Gruppen-Plateaus, gestrichelt für Einzel-Plateaus. Vertikale gestrichelte Linien verbinden jeden Nadir mit seinem Plateau-Niveau. Farbzuweisung automatisch aus einer 14-Farben-Palette. Label zeigt das Niveau in bpm.

## Zwei-Oszillatoren-Modell

Die Analyse basiert auf der Beobachtung zweier überlagernder Oszillatoren in der nächtlichen HR:

1. **Schneller Oszillator** (~15–40 min Periode): Erzeugt die HR-Hügel, sichtbar als MHR10-Wellen. Wird durch die **Phasen** abgebildet.

2. **Langsamer Oszillator** (~60–120 min Periode): Moduliert die Amplitude der Hügel. Erzeugt die **Plateaus** — Niveaus, auf denen mehrere Hügel reiten. Sichtbar als Hüllkurve (MHR30 approximiert dies, aber die Plateau-Detektion arbeitet direkt auf MHR10-Nadirs).

Die Plateau-Hierarchie (Stacktiefe) bildet ab, wie diese Niveaus ineinander verschachtelt sind: Das Baseline-Plateau umfasst die ganze Nacht, darauf sitzen mittlere Plateaus, darauf hohe.

## Datenquellen

- **Gadgetbridge SQLite-DB**: Tabellen `XIAOMI_ACTIVITY_SAMPLE` (HR im 1-Minuten-Takt) und `XIAOMI_SLEEP_TIME_SAMPLE` (Schlafzusammenfassungen)
- **seizures.csv**: Spalten `Date` (dd/mm/yyyy HH:MM:SS), `Empty` (immer 1). Eine Zeile pro Anfallstag.
- Alle Zeitstempel werden von UTC nach Europe/Berlin konvertiert