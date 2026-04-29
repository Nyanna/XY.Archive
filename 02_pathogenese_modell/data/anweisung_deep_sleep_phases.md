# Anweisung: Tiefschlafphasen-Detektion (Nulldurchgänge)

## Ziel

Aus den minütlich aggregierten HRV-Daten (Postgres `HRV_MINUTE_AGGREGATED`) alle echten Tiefschlafphasen ("Nulldurchgänge") identifizieren und in eine separate SQLite-Datenbank exportieren. Pro Nacht werden Verteilung, Länge und Gesamtdauer der Phasen ermittelt.

## Ausführung

**Das Script existiert bereits — NICHT neu generieren, nur ausführen:**

```bash
python3 02_pathogenese_modell/data/gen_deep_sleep_phases.py
```

Erzeugt `02_pathogenese_modell/data/deep_sleep_phases.db` (SQLite) und gibt eine Zusammenfassung auf stdout aus.

## Eingabe

- Postgres-Tabelle `public."HRV_MINUTE_AGGREGATED"` (minütliche HRV-Metriken)
- Umgebungsvariablen: `PGHOST`, `PGPORT`, `PGDATABASE`, `PGPASSWORD`, `PGUSER`

## Nacht-Definition

Zwei Bedingungen grenzen den Nachtbereich ab:

1. **Vagale Dominanz:** Nur Minuten mit `B7B8_DOM > 0` (HF > LF, parasympathische Dominanz).
2. **Zeitfenster:** Zusätzlich auf **00:00–07:30 Lokalzeit** (`Europe/Berlin`) beschränkt, um Tagesruhe-Phasen mit ähnlicher Signatur auszuschließen.

Innerhalb dieses Bereichs werden zusammenhängende Blöcke (Lücke > 30 min = neue Session) zu Nächten gruppiert. Die Nacht wird dem Kalendertag zugeordnet.

## Glättung

Vor der Schwellwert-Prüfung werden HR, RMSSD und SDNN mit einem **zentrierten Rolling-Median** (Fenster = 5 Minuten) geglättet. Das verhindert, dass einzelne Ausreißer-Minuten Phasen auseinanderreißen. Die Stabilitätsmetriken werden auf den **ungeglätteten** Rohwerten berechnet.

## Phasen-Definition

Eine Tiefschlafphase ist ein zusammenhängender Block von Minuten, deren **geglättete** Werte **alle drei** Kriterien gleichzeitig erfüllen:

| Metrik | Schwelle | Bedeutung |
|--------|----------|-----------|
| `HR_BPM` | < 80 | Niedrige Herzfrequenz |
| `RMSSD_MS` | ≤ 60 | Am oder unter dem nächtlichen Rauschboden |
| `SDNN_MS` | ≤ 60 | Am oder unter dem nächtlichen Rauschboden |

**Mindestdauer:** 5 aufeinanderfolgende Minuten. Blöcke < 5 min werden verworfen.

Minuten mit NULL-Werten in einer der drei Metriken oder ohne vagale Dominanz sind nicht im Datensatz enthalten.

## Stabilitätscharakteristik

Pro Phase werden folgende Stabilitätsmetriken auf RMSSD und SDNN berechnet:

| Metrik | Beschreibung |
|--------|-------------|
| `rmssd_mean` | Mittlerer RMSSD innerhalb der Phase (ms) |
| `rmssd_std` | Standardabweichung RMSSD innerhalb der Phase (ms) |
| `rmssd_cv` | Variationskoeffizient RMSSD (std/mean) |
| `sdnn_mean` | Mittlerer SDNN innerhalb der Phase (ms) |
| `sdnn_std` | Standardabweichung SDNN innerhalb der Phase (ms) |
| `sdnn_cv` | Variationskoeffizient SDNN (std/mean) |
| `hr_mean` | Mittlere HR innerhalb der Phase (bpm) |
| `hr_std` | Standardabweichung HR innerhalb der Phase (bpm) |

## Ausgabe: SQLite `deep_sleep_phases.db`

### Tabelle `deep_sleep_phases`

Eine Zeile pro erkannter Phase.

| Spalte | Typ | Beschreibung |
|--------|-----|-------------|
| `id` | INTEGER PK | Auto-Increment |
| `night` | TEXT | Nacht-Datum (YYYY-MM-DD) |
| `start_time` | TEXT | Beginn der Phase (ISO 8601, Lokalzeit) |
| `end_time` | TEXT | Ende der Phase (ISO 8601, Lokalzeit) |
| `duration_min` | INTEGER | Dauer in Minuten |
| `hr_mean` | REAL | Mittlere HR (bpm) |
| `hr_std` | REAL | Standardabweichung HR (bpm) |
| `rmssd_mean` | REAL | Mittlerer RMSSD (ms) |
| `rmssd_std` | REAL | Standardabweichung RMSSD (ms) |
| `rmssd_cv` | REAL | Variationskoeffizient RMSSD |
| `sdnn_mean` | REAL | Mittlerer SDNN (ms) |
| `sdnn_std` | REAL | Standardabweichung SDNN (ms) |
| `sdnn_cv` | REAL | Variationskoeffizient SDNN |

### Tabelle `deep_sleep_nights`

Eine Zeile pro Nacht (nur Nächte mit ≥1 Phase).

| Spalte | Typ | Beschreibung |
|--------|-----|-------------|
| `night` | TEXT PK | Nacht-Datum (YYYY-MM-DD) |
| `n_phases` | INTEGER | Anzahl Tiefschlafphasen |
| `total_deep_min` | INTEGER | Summe aller Phasendauern (min) |
| `mean_phase_min` | REAL | Mittlere Phasenlänge (min) |
| `median_phase_min` | REAL | Median Phasenlänge (min) |
| `max_phase_min` | INTEGER | Längste Phase (min) |
| `min_phase_min` | INTEGER | Kürzeste Phase (min) |
| `first_phase_time` | TEXT | Beginn der frühesten Phase (HH:MM) |
| `last_phase_time` | TEXT | Beginn der spätesten Phase (HH:MM) |

## Kontext

"Nulldurchgang" bezeichnet im Modell den Zustand minimaler Raphe-Aktivität: HR fällt unter die sympathische Schwelle, RMSSD/SDNN kollabieren auf den Rauschboden. Diese Phasen korrespondieren mit den tiefsten SWS-Abschnitten, in denen das B7-System maximal supprimiert ist.
