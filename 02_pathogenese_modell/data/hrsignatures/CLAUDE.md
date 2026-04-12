# Signaturprofilierung — Anfallszyklus-Analyse

## Übersicht

Zwei Skripte, die auf den Ergebnissen der HR-Plateau-Analyse aufbauen und die Schlafarchitektur-Signatur des Anfallszyklus quantifizieren:

1. **night_characterization.py** — Berechnet pro Nacht 25 Modulationsqualitäts-Metriken
2. **statistical_summary.py** — Korreliert diese Metriken mit Anfällen und vergleicht PRE/POST-Perioden

## Theoretischer Hintergrund

Die Analyse basiert auf dem Zwei-Oszillatoren-Modell der nächtlichen HR:

- **Schneller Oszillator** (Phasen, ~15–40 min): HR-Hügel zwischen Nadirs
- **Langsamer Oszillator** (Plateaus, ~60–120 min): Hüllkurve, auf der die Hügel reiten

Die Plateau-Hierarchie (Stack) bildet die B7-Modulationstiefe ins ANS ab:

- **Tiefe Plateaus** (stack_depth 0–1): B7-Reichweite — wie tief er die ANS-Eigendynamik moduliert
- **Hohe Plateaus** (stack_depth ≥ 3): ANS-Eigenzeit — Phasen ohne B7-Modulation
- **Modulationsbrüche**: Stellen, an denen die hierarchische Schichtung inkonsistent wird

Der Anfallszyklus zeigt eine charakteristische Signatur:

| Phase | Tag | B7-Zustand | HR-Signatur |
|-------|-----|-----------|-------------|
| Funktional | −2 | Stabile Modulation | Wenige Brüche, gleichmäßige Level-Abstände |
| Rigide | −1 | Verliert Flexibilität | Gleichförmige Phasendauern, reduzierte Adaptivität |
| Trigger | 0 | Restart mit desolatem Takt | Flacher nadir_slope, bodenlastiger Stack, hoher spacing_cv |

## Dateien

### `night_characterization.py`

Liest `nadirs.csv`, `phases.csv`, `plateaus.csv` und berechnet pro Nacht 25 Metriken.

**Ausführung:**
```bash
python3 night_characterization.py
python3 night_characterization.py --data-dir ../hrphases --out-dir .
```

**Eingabe:** Die drei CSVs aus `plateau_analysis.py`
**Ausgabe:** `night_characteristics.csv`

**Parameter:**
| Flag | Default | Beschreibung |
|------|---------|-------------|
| `--data-dir` | `.` | Verzeichnis mit nadirs.csv, phases.csv, plateaus.csv |
| `--out-dir` | `.` | Ausgabeverzeichnis |

### `night_characteristics.csv` — Spalten

#### Plateau-Struktur

| Spalte | Beschreibung |
|--------|-------------|
| `night_date` | Nacht-Datum (Aufwach-Tag) |
| `n_plateaus` | Anzahl der Plateaus |
| `max_depth` | Maximale Stacktiefe |
| `base_level` | Niveau des tiefsten Plateaus (bpm) |
| `top_level` | Niveau des höchsten Plateaus (bpm) |
| `total_range` | top_level − base_level (bpm) |

#### Modulationsqualität

| Spalte | Beschreibung | Interpretation |
|--------|-------------|----------------|
| `dur_cv` | CV der Gesamt-Plateaudauer pro Stacktiefe | Hoch = ungleichmäßige Zeitalokation über Tiefen |
| `count_cv` | CV der Plateau-Anzahl pro Stacktiefe | Hoch = einige Tiefen überrepräsentiert |
| `break_frac` | Anteil der Plateaus mit >2× Dauerabweichung von Nachbar-Stacktiefen | Hoch = gestörte hierarchische Konsistenz |
| `spacing_cv` | CV der Level-Abstände zwischen Plateaus | Niedrig = gleichmäßige Niveau-Verteilung; hoch = irreguläre Sprünge |
| `stack_symmetry` | Mittlere Dauer obere Hälfte / untere Hälfte des Stacks | <1 = bodenlastig (B7 drückt runter, hält oben nicht); >1 = kopflastig (ANS-Eigenzeit dominiert) |
| `intra_dur_cv` | Mittlerer CV der Plateaudauern innerhalb gleicher Stacktiefe | Hoch = Plateaus gleicher Tiefe sind ungleichmäßig |

#### ANS-Autonomie-Marker

| Spalte | Beschreibung |
|--------|-------------|
| `frac_high` | Anteil der Schlafzeit in Plateaus >5 bpm über Baseline |
| `frac_vhigh` | Anteil der Schlafzeit in Plateaus >8 bpm über Baseline |
| `n_d1`, `n_d2`, `n_d3` | Anzahl Plateaus ab Stacktiefe ≥1, ≥2, ≥3 |

#### Phasen-Metriken

| Spalte | Beschreibung |
|--------|-------------|
| `n_phases` | Anzahl der Phasen (Segmente zwischen Nadirs) |
| `mean_phase_dur` | Mittlere Phasendauer (min) |
| `phase_dur_cv` | CV der Phasendauern — niedrig = rigide Zykluslänge |
| `mean_phase_std` | Mittlere HR-Std innerhalb der Phasen |
| `std_ratio_2nd_1st` | HR-Std zweite Nachthälfte / erste Nachthälfte |
| `dur_ratio_2nd_1st` | Phasendauer zweite / erste Nachthälfte |

#### Nadir-Metriken

| Spalte | Beschreibung | Interpretation |
|--------|-------------|----------------|
| `n_nadirs` | Anzahl Nadirs | Mehr Nadirs = fragmentiertere Modulation |
| `nadir_mean` | Mittlerer MHR10 an Nadirs | Gesamtniveau der Talwerte |
| `nadir_std` | Std der Nadir-Werte | Hoch = heterogene Taltiefen |
| `nadir_range` | Max − Min der Nadir-Werte | Spannweite der Modulationstiefe |
| `nadir_slope` | Lineare Regression der Nadir-Werte über die Nacht | Negativ = physiologische Absenkung; flach/positiv = fehlende parasympathische Progression (B7-Defizienz) |

### `statistical_summary.py`

Liest `night_characteristics.csv` und `seizures.csv`, berechnet Korrelationen, Zyklusprofile und Periodenvergleiche.

**Ausführung:**
```bash
python3 statistical_summary.py
python3 statistical_summary.py --data-dir . --seizure-file ../seizures.csv
python3 statistical_summary.py --pre-end 2025-02-28 --post-start 2026-03-01
```

**Eingabe:** `night_characteristics.csv`, `seizures.csv`
**Ausgabe:** Bis zu drei CSV-Dateien

**Parameter:**
| Flag | Default | Beschreibung |
|------|---------|-------------|
| `--data-dir` | `.` | Verzeichnis mit night_characteristics.csv |
| `--seizure-file` | Automatische Suche | Pfad zur seizures.csv |
| `--out-dir` | `.` | Ausgabeverzeichnis |
| `--pre-end` | `2025-02-28` | Letzter Tag der PRE-Periode |
| `--post-start` | `2026-03-01` | Erster Tag der POST-Periode |

### Ausgabe-CSVs

#### `statistical_summary.csv`

Korrelationstabelle: jede Kombination aus Seizure-Lag × Parameter.

| Spalte | Beschreibung |
|--------|-------------|
| `lag` | Zeitlicher Bezug: `same` (Anfallstag), `next1` (Tag vor Anfall), `next2` (2 Tage vor), `prev1` (Tag nach Anfall) |
| `param` | Name der Metrik |
| `r` | Point-biserial Korrelation |
| `p_pointbiserial` | p-Wert der Korrelation |
| `p_mannwhitney` | p-Wert des Mann-Whitney-U-Tests |
| `p_min` | Minimum der beiden p-Werte |
| `median_no_seizure` | Median an anfallsfreien Tagen |
| `median_seizure` | Median an anfallsbezogenen Tagen |
| `n_no_seizure`, `n_seizure` | Stichprobengrößen |
| `significant` | p_min < 0.05 |
| `trend` | p_min < 0.15 |

#### `seizure_cycle_profile.csv`

Mittelwerte jeder Metrik an den Zyklus-Positionen, getrennt nach Periode.

| Spalte | Beschreibung |
|--------|-------------|
| `period` | `ALL`, `PRE` oder `POST` |
| `cycle_position` | `baseline`, `day_minus2`, `day_minus1`, `day_0` |
| `param` | Name der Metrik |
| `mean`, `std`, `median` | Deskriptive Statistiken |
| `n` | Stichprobengröße |

Die Zyklus-Position wird exklusiv zugewiesen: Eine Nacht, die sowohl Tag 0 eines Anfalls als auch Tag −2 eines anderen ist, wird als `day_0` klassifiziert (Priorität: day_0 > day_minus1 > day_minus2 > baseline).

#### `pre_post_comparison.csv`

Direkter Vergleich jeder Metrik zwischen PRE und POST.

| Spalte | Beschreibung |
|--------|-------------|
| `param` | Name der Metrik |
| `pre_median`, `post_median` | Mediane |
| `delta` | post − pre |
| `p_mannwhitney` | p-Wert |
| `n_pre`, `n_post` | Stichprobengrößen |

## Perioden-Definition

| Periode | Zeitraum | Medikation | Beschreibung |
|---------|----------|-----------|-------------|
| PRE | Dez 2024 – Feb 2025 | Metoprolol (Betablocker) | Baseline ohne serotonerge Intervention |
| GAP | Mär 2025 – Feb 2026 | — | Tracker nicht getragen, keine Daten |
| POST | Mär 2026+ | Lisdexamfetamin (LDX) | Stabilisierte DA-vermittelte Raphe-Modulation |

**Caveat PRE:** HR-Variabilität unter Betablocker (Metoprolol) pharmakologisch gedämpft. PRE-Metriken, die auf HR-Amplitude oder -Variabilität basieren, sind nicht direkt mit POST vergleichbar. Betroffen sind: `nadir_std`, `nadir_range`, `mean_phase_std`, `std_ratio`, `total_range`, `frac_high`, `frac_vhigh`, sowie indirekt `nadir_slope` (komprimierter HR-Korridor flacht die Regression ab). Auch die Anzahl detektierbarer Plateaus kann durch die höhere POST-Dynamik ohne Betablocker steigen, was `n_plateaus`, `n_d1`–`n_d3` beeinflusst. Strukturelle Metriken, die auf relativer Hierarchie basieren (`count_cv`, `break_frac`, `spacing_cv`, `stack_symmetry`, `intra_dur_cv`), sind robuster gegenüber dem Confounder, aber nicht vollständig frei davon.

**Caveat POST:** n=3 Anfälle in POST. Alle Anfalls-bezogenen POST-Statistiken sind explorativ.

## Pipeline

```
Gadgetbridge DB + seizures.csv
        │
        ▼
plateau_analysis.py
        │
        ├── nadirs.csv
        ├── phases.csv
        └── plateaus.csv
                │
                ▼
night_characterization.py
                │
                └── night_characteristics.csv
                        │
                        ▼
statistical_summary.py
                        │
                        ├── statistical_summary.csv
                        ├── seizure_cycle_profile.csv
                        └── pre_post_comparison.csv
```

## Voraussetzungen

- Python ≥ 3.9
- `numpy`, `pandas`, `scipy`
