# Anweisung: B7-Abschaltzeitkonstante τ aus nächtlichen HR-Daten

## Ziel

Für jede Schlafnacht die Zeitkonstante τ der sympathischen Abschaltung berechnen durch Fit einer Exponential-Sättigungskurve auf die HR-Daten. Ergebnis: eine lückenlose Zeitreihe von τ pro Nacht.

## Eingabe

- `02_pathogenese_modell/data/Gadgetbridge` (SQLite)
- `02_pathogenese_modell/data/seizures.csv` (CSV)
- Gerät: Xiaomi Smart Band 9

## Relevante Tabellen

| Tabelle | Inhalt | Timestamp-Format |
|---------|--------|------------------|
| `XIAOMI_SLEEP_TIME_SAMPLE` | Schlafsessions | Millisekunden (÷1000) |
| `XIAOMI_ACTIVITY_SAMPLE` | HR-Samples (minutenweise) | Sekunden |

**Achtung:** Sleep-Tabellen verwenden Millisekunden, Activity-Tabelle verwendet Sekunden.

## Timezone

Alle Timestamps sind UTC. Konvertierung nach `Europe/Berlin` (CET/CEST):

```python
from zoneinfo import ZoneInfo
tz = ZoneInfo('Europe/Berlin')
```

## Schlafnacht-Zuordnung

Cutoff 12:00 Lokalzeit. Sessions mit Einschlafzeitpunkt vor 12:00 gehören zur Vornacht:

```python
def sleep_night(ts_utc_seconds):
    dt = datetime.fromtimestamp(ts_utc_seconds, tz=timezone.utc).astimezone(tz)
    if dt.hour < 12:
        dt = dt - timedelta(days=1)
    return dt.strftime('%Y-%m-%d')
```

## Filter

- Nur Hauptschlaf: `TOTAL_DURATION >= 90` (Minuten)
- HR-Samples: `HEART_RATE > 0`
- Mindestens 10 HR-Samples pro Nacht

## Modell

Exponentieller Sättigungsabfall:

```
HR(t) = floor + amplitude × e^(−t / τ)
```

Drei freie Parameter:
- `amplitude`: Differenz Entry − Floor (bpm)
- `tau`: Abschaltzeitkonstante (Stunden) — Zielgröße
- `floor`: asymptotischer HR-Boden (bpm)

## Berechnung pro Nacht

### 1. HR-Daten laden

Alle HR-Samples zwischen `sleep_start_ts` und `wakeup_ts` (Activity-Tabelle, Sekunden-Timestamps).

### 2. Linearen Slope prüfen

```python
ts_hours = (hr_timestamps - sleep_start_ts) / 3600  # Stunden seit Einschlafen
slope, intercept = np.polyfit(ts_hours, hr_values, 1)
r2 = np.corrcoef(ts_hours, hr_values)[0,1]**2
```

### 3. Entry/Exit HR

- `entry_hr`: Mean HR der ersten 15 Minuten
- `exit_hr`: Der niedrigste Wert eines gleitenden Mittelwerts über den Gesamten Schlafzyklus mit einer Fenstergröße von 10 Minuten.
- `drop`: `entry_hr - exit_hr`

### 4. Anfall markieren

Laden der seizures.csv und markieren der Anfallstage mit 1 sonst 0.

```python
    # Add seizure column from seizures.csv
    seizure_df = pd.read_csv(SEIZURES_PATH)
    seizure_dates = set(
        pd.to_datetime(seizure_df["Date"], format="%d/%m/%y").dt.strftime("%Y-%m-%d")
    )
    result["seizure"] = result["night"].apply(lambda d: 1 if d in seizure_dates else 0)
```

## Ausgabe-CSV: `tau_timeseries.csv`

| Spalte | Typ | Beschreibung |
|--------|-----|-------------|
| `sleep_night` | str | Schlafnacht (YYYY-MM-DD) |
| `period` | str | PRE (<2025-03-01) / POST (≥2026-03-01) |
| `start_time` | str | Einschlafzeit lokal (HH:MM) |
| `dur_h` | float | Schlafdauer in Stunden |
| `tau_h` | float | Abschaltzeitkonstante in Stunden|
| `amplitude` | float | Entry − Floor (bpm)|
| `floor` | float | Asymptotischer HR-Boden (bpm) |
| `seizure` | integer | Markierung der Anfallstage |

## Kontext

τ ist die B7-Abschaltzeitkonstante — die Zeit, die das serotonerge Raphe-System braucht, um im Schlaf zu supprimieren. τ oszilliert mit ~6.7-Tage-Periodizität (B7/B8-Schwebungsfrequenz).