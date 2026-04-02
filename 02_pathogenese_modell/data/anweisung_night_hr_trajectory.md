# Anweisung: Night HR Trajectory aus Gadgetbridge-DB generieren

## Ziel

Aus einer Gadgetbridge SQLite-Datenbank (`Gadgetbridge`) die nächtliche HR-Trajektorie pro Schlafnacht klassifizieren und als CSV exportieren.

## Ausführung

**Das Script existiert bereits — NICHT neu generieren, nur ausführen:**

```bash
python3 02_pathogenese_modell/data/gen_night_hr_trajectory.py
```

Erzeugt `02_pathogenese_modell/data/night_hr_trajectory.csv` und gibt eine Pattern-Verteilungstabelle (PRE/POST) auf stdout aus.

Die nachfolgende Dokumentation beschreibt die Logik des bestehenden Scripts als Referenz, nicht als Implementierungsanweisung. Ignoriere sie wenn das Script funktioniert.

## Eingabe

- `02_pathogenese_modell/data/Gadgetbridge` (SQLite)
- Gerät: Xiaomi Smart Band 9

## Relevante Tabellen

| Tabelle | Inhalt | Timestamp-Format |
|---------|--------|------------------|
| `XIAOMI_SLEEP_TIME_SAMPLE` | Schlafsessions (Start, Wakeup, Phasendauern) | Millisekunden (÷1000) |
| `XIAOMI_SLEEP_STAGE_SAMPLE` | Hypnogramm-Transitionen. Codes: 2=REM, 3=Light, 4=Deep, 5=Awake | Millisekunden (÷1000) |
| `XIAOMI_ACTIVITY_SAMPLE` | HR-Samples (minutenweise) | Sekunden |

**Achtung:** Sleep-Tabellen verwenden Millisekunden, Activity-Tabelle verwendet Sekunden.

## Timezone

Alle Timestamps sind UTC. Konvertierung nach `Europe/Berlin` (CET/CEST) erforderlich:

```python
from zoneinfo import ZoneInfo
tz = ZoneInfo('Europe/Berlin')
```

## Schlafnacht-Zuordnung

Cutoff 18:00 Lokalzeit. Sessions mit Einschlafzeitpunkt vor 18:00 gehören zur Vornacht:

```python
def sleep_night(ts_utc_seconds):
    dt = datetime.fromtimestamp(ts_utc_seconds, tz=timezone.utc).astimezone(tz)
    if dt.hour < 18:
        dt = dt - timedelta(days=1)
    return dt.strftime('%Y-%m-%d')
```

## Filter

- Nur Hauptschlaf-Sessions: `TOTAL_DURATION >= 180` (Minuten)
- HR-Samples: `HEART_RATE > 0`
- Mindestens 10 HR-Samples pro Nacht

## Berechnung pro Nacht

### 1. HR-Daten extrahieren

Alle HR-Samples zwischen `sleep_start_ts` und `wakeup_ts` (Activity-Tabelle, Sekunden-Timestamps).

### 2. Lineare Regression

```python
ts_hours = (hr_timestamps - sleep_start_ts) / 3600  # Stunden seit Einschlafen
slope, intercept = np.polyfit(ts_hours, hr_values, 1)
r2 = np.corrcoef(ts_hours, hr_values)[0,1]**2
```

### 3. Entry/Exit HR

- `entry_hr`: Mean HR der ersten 30 Minuten
- `exit_hr`: Mean HR der letzten 30 Minuten
- `drop`: `entry_hr - exit_hr`

### 4. Quartal-Mittelwerte

Nacht in 4 gleiche Zeitabschnitte teilen, Mean HR pro Quartal berechnen (`q1_mean` bis `q4_mean`).

### 5. Anomalie-Detektion

Late Rise = HR-Anstieg >3 bpm zwischen Q2→Q3 oder Q3→Q4:

```python
late_rise = (q3_mean > q2_mean + 3) or (q4_mean > q3_mean + 3)
```

### 6. Pattern-Klassifikation

```python
if r2 > 0.25 and slope < -1.0:
    pattern = 'LINEAR_STARK'
elif r2 > 0.12 and slope < -0.5:
    pattern = 'LINEAR_MODERAT'
elif r2 < 0.05 and abs(slope) < 0.5:
    pattern = 'FLAT'
elif slope > 0.3 and r2 > 0.05:
    pattern = 'ANSTIEG'
elif late_rise:
    pattern = 'ANOMALIE_LATE_RISE'
else:
    pattern = 'GEMISCHT'
```

### 7. Perioden-Zuordnung

```python
period = 'PRE' if night < '2025-03-01' else 'POST'
```

PRE = Metoprolol-Periode, POST = LDX-Periode. Dazwischen liegt eine 13-monatige Trackinglücke.

## Ausgabe-CSV: `night_hr_trajectory.csv`

| Spalte | Typ | Beschreibung |
|--------|-----|-------------|
| `night` | str | Schlafnacht (YYYY-MM-DD) |
| `period` | str | PRE / POST |
| `start_time` | str | Einschlafzeit lokal (HH:MM) |
| `dur_h` | float | Schlafdauer in Stunden |
| `slope` | float | HR-Steigung (bpm/h), negativ = Abfall |
| `r2` | float | R² der linearen Regression |
| `entry_hr` | float | Mean HR erste 30 min |
| `exit_hr` | float | Mean HR letzte 30 min |
| `drop` | float | entry_hr - exit_hr |
| `q1_mean` | float | Mean HR 1. Quartal |
| `q2_mean` | float | Mean HR 2. Quartal |
| `q3_mean` | float | Mean HR 3. Quartal |
| `q4_mean` | float | Mean HR 4. Quartal |
| `pattern` | str | LINEAR_STARK / LINEAR_MODERAT / FLAT / GEMISCHT / ANSTIEG / ANOMALIE_LATE_RISE |

## Zusammenfassung

Das Script gibt nach Export eine Tabelle mit Pattern-Verteilung auf stdout aus, aufgeteilt nach PRE/POST, mit Mean Entry HR, Exit HR und Drop pro Pattern.
