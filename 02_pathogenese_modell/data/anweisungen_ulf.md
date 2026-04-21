# Anweisung: ULF-Metrik in `hrv_aggregate.py`

## Ziel

Erweiterung von `02_pathogenese_modell/data/hrv_aggregate.py` um eine ULF-Spektralmetrik (Ultra Low Frequency) auf Basis der RR-Intervall-Rohdaten (`HEART_RR_INTERVAL_SAMPLE`). Ergebnis: drei zusätzliche Spalten pro Minute in `HRV_MINUTE_AGGREGATED`, berechnet über ein 120-min Sliding-Window, literaturkonform (ESC/NASPE 1996; Shaffer & Ginsberg 2017; Laguna 1998 für Lomb-Scargle auf irregulärem Sampling).

## Eingabe

Unverändert zum bestehenden Pfad des Scripts:

- `02_pathogenese_modell/data/Gadgetbridge` (SQLite)
- Tabelle: `HEART_RR_INTERVAL_SAMPLE` (RR in Millisekunden, Timestamp in Millisekunden, UTC)
- Device: Coospo-Brustgurt (siehe User-Memory — ektopie-freies Profil, `ARTIFACT_THRESHOLD_MS=500` bleibt der korrekte Default)

## Wissenschaftlicher Hintergrund

ULF umfasst per ESC/NASPE 1996 Task Force den Bereich **<0.0033 Hz** (Perioden > 5 min) und wird klassisch aus 24-h-Aufzeichnungen bestimmt. Für die Nachtskala der vorhandenen Daten wird das Band in zwei Sub-Bänder aufgeteilt, um unterschiedliche physiologische Periodiken getrennt zu isolieren:

- **ULF1 (0.0005–0.0033 Hz, Perioden ~5–33 min):** NREM/REM-Zyklus (~90 min), circa-semiultradiane Rhythmen, möglicherweise B7/B8-Schwebung im Minutenbereich.
- **ULF2 (0.0001–0.0005 Hz, Perioden ~33–167 min):** langsame sympatho-vagale Drift, circadian-näherliegende Komponenten über mehrere Schlafzyklen.

Unterhalb 0.0001 Hz wird nicht ausgewertet (Perioden >2.8 h liegen unterhalb der Fensterlänge).

## Frequenzbänder

```python
ULF1_BAND = (0.0005, 0.0033)  # Hz
ULF2_BAND = (0.0001, 0.0005)  # Hz
ULF_BAND  = (0.0001, 0.0033)  # Hz  (Summenband für ULF_MS2)
```

## Sliding-Window

- **Länge:** 120 min, zentriert auf die aktuelle Minute (`minute_start ± 60 min`).
- **Minimum-Beats:** `ULF_MIN_BEATS = 3600` (entspricht ~30 bpm Durchschnitt über 120 min). Darunter: ULF\*=NULL.
- **Keine Gap-Obergrenze:** die Metrik soll robust gegen Gaps sein (Lomb-Scargle operiert direkt auf den irregulär gesampelten RR-Timestamps).
- **Fensterbeschaffung analog VLF:** `np.searchsorted(all_ts, win_start/end, side="left")` auf dem bereits sortierten `all_ts`-Array.

```python
ULF_WINDOW_MS = 120 * 60 * 1000
ULF_MIN_BEATS = 3600
```

## Spektralmethode: Lomb-Scargle

Statt cubic-spline + Welch (aktueller VLF/LF/HF-Pfad) wird für ULF **Lomb-Scargle** verwendet, weil lange Fenster typischerweise Gaps enthalten und Spline-Interpolation über mehrminütige Lücken spurious ULF-Power erzeugt. Lomb-Scargle ist der literaturkonforme Weg für Spektralanalyse irregulärer biomedizinischer Zeitreihen (Laguna et al. 1998, *IEEE Trans. Biomed. Eng.*; Clifford & Tarassenko 2005).

### Ablauf pro 120-min Fenster

1. **Zeitachse:** `t_sec = cumsum(rr) / 1000` (relative Zeit seit erstem Beat im Fenster, in Sekunden). Alternativ `t_sec = (ts_ms - ts_ms[0]) / 1000` falls die Ursprungs-Timestamps stabiler sind — **bevorzugt letzteres**, da dies die echten Gaps preserviert.
2. **Artefaktkorrektur:** `correct_artifacts(rr)` anwenden (bestehende Funktion). Abbruch mit ULF\*=NULL falls >5% Artefakte.
3. **Linear detrend:** Lineare Regression `rr ~ t` subtrahieren (entfernt Basislinien-Drift und langsame HR-Senkung im Schlaf). Äquivalent zum `detrend="linear"` im VLF-Pfad, aber hier manuell, da Lomb-Scargle keinen internen Detrend hat:
   ```python
   slope, intercept = np.polyfit(t_sec, rr, 1)
   rr_detrended = rr - (slope * t_sec + intercept)
   ```
4. **Frequenzgrid:**
   ```python
   f_min = 0.00005            # Hz  (unterhalb ULF2, Rand-Padding)
   f_max = 0.005              # Hz  (oberhalb ULF1, Rand-Padding)
   n_freq = 512               # ausreichend Auflösung für beide Sub-Bänder
   freqs = np.linspace(f_min, f_max, n_freq)
   angular = 2 * np.pi * freqs
   ```
5. **Lomb-Scargle via `scipy.signal.lombscargle`:**
   ```python
   from scipy.signal import lombscargle
   pgram = lombscargle(t_sec, rr_detrended, angular, normalize=False, precenter=False)
   ```
6. **PSD-Normalisierung auf ms²/Hz**, so dass `∫ PSD df ≈ var(rr_detrended)` — konsistent mit dem Welch-Pfad:
   ```python
   # scipy.signal.lombscargle (normalize=False) gibt P(ω) = 0.5 * [...]
   # in Einheiten (ms)². Skalierung zu PSD in ms²/Hz:
   T = t_sec[-1] - t_sec[0]              # Fensterlänge in s
   psd = pgram * (2.0 / T)               # Parseval-konform mit Welch 'density'
   ```
   Hinweis: die exakte Konstante im Verhältnis zum Welch-Pfad kann im Review-Schritt durch Cross-Check auf einem synthetischen Sinus-Signal bekannter Amplitude verifiziert werden.
7. **Bandintegration** (Trapez, analog `compute_band_power`):
   ```python
   def _band_power(freqs, psd, f_lo, f_hi):
       mask = (freqs >= f_lo) & (freqs <= f_hi)
       if not mask.any():
           return None
       return float(np.trapezoid(psd[mask], freqs[mask]))
   ```
8. **Rückgabe:** Dict `{"ulf_ms2": ..., "ulf1_ms2": ..., "ulf2_ms2": ...}`, alle ms². `ULF_MS2` als Integral über das Summenband (0.0001–0.0033 Hz), **nicht** als Summe der Sub-Band-Integrale (letzteres wäre identisch hier, da die Bänder zusammenhängend sind — ersteres ist aber per Definition sauberer, falls Sub-Band-Ränder später angepasst werden).

## Neue Konstanten (oben im Script)

```python
ULF_WINDOW_MS = 120 * 60 * 1000
ULF_MIN_BEATS = 3600
ULF1_BAND = (0.0005, 0.0033)
ULF2_BAND = (0.0001, 0.0005)
ULF_BAND  = (0.0001, 0.0033)
ULF_FREQ_MIN = 0.00005
ULF_FREQ_MAX = 0.005
ULF_N_FREQ   = 512
```

## Neue Funktion

```python
def compute_ulf_power(t_ms: np.ndarray, rr: np.ndarray) -> dict | None:
    """Lomb-Scargle ULF power on irregularly-sampled RR with gaps.

    Returns {'ulf_ms2': float, 'ulf1_ms2': float, 'ulf2_ms2': float}
    or None if artefact fraction > 5 % or insufficient data.
    """
    ...
```

Platziert unterhalb von `compute_band_power`. Nutzt `correct_artifacts()` für Konsistenz mit dem PSD-Pfad.

## Integration in `compute_minute_metrics`

Neuer Parameter `enable_ulf: bool = False`. Im Minuten-Loop, analog zum VLF-Block:

```python
ulf_ms2, ulf1_ms2, ulf2_ms2 = None, None, None
if enable_ulf:
    t_ulf = time.monotonic()
    win_ulf_start = minute_start - 60 * 60 * 1000
    win_ulf_end   = minute_start + 60 * 60 * 1000
    i_ulf_lo = int(np.searchsorted(all_ts, win_ulf_start, side="left"))
    i_ulf_hi = int(np.searchsorted(all_ts, win_ulf_end,   side="left"))
    if (i_ulf_hi - i_ulf_lo) >= ULF_MIN_BEATS:
        ulf_res = compute_ulf_power(
            all_ts[i_ulf_lo:i_ulf_hi].astype(np.int64),
            all_rr[i_ulf_lo:i_ulf_hi].astype(float),
        )
        if ulf_res is not None:
            ulf_ms2  = ulf_res["ulf_ms2"]
            ulf1_ms2 = ulf_res["ulf1_ms2"]
            ulf2_ms2 = ulf_res["ulf2_ms2"]
    time_ulf += time.monotonic() - t_ulf
```

Timing-Zähler `time_ulf` in Progress-Log und Summary einbauen (analog `time_vlf`).

Drei neue Keys im Result-Dict: `"ulf_ms2"`, `"ulf1_ms2"`, `"ulf2_ms2"`.

## Schema-Änderung `HRV_MINUTE_AGGREGATED`

`DROP TABLE` + `CREATE TABLE` (bestehendes Verhalten) erweitern um:

```sql
ULF_MS2  REAL,
ULF1_MS2 REAL,
ULF2_MS2 REAL,
```

Einzufügen **nach** `HF_MS2` und **vor** `LF_HF_RATIO`, damit die Band-Spalten logisch gruppiert bleiben:

```
VLF_MS2, LF_MS2, HF_MS2, ULF_MS2, ULF1_MS2, ULF2_MS2, LF_HF_RATIO, DFA_ALPHA1
```

Das zugehörige `INSERT`-Statement (21 → 24 Spalten) und die Result-Tuple-Serialisierung in `write_results` entsprechend erweitern.

## CLI-Flag

Neues Flag **`--ulf`** in `main()`, analog `--dfa`:

```python
parser.add_argument(
    "--ulf",
    action="store_true",
    help="Enable ULF spectral analysis (2 h sliding window, Lomb-Scargle on "
         "irregular RR samples). Outputs ULF_MS2 + ULF1_MS2 + ULF2_MS2. "
         "Default: off (very slow).",
)
```

Weitergabe an `compute_minute_metrics(..., enable_ulf=args.ulf, ...)`.

Das Flag ist **unabhängig** von `--lf-hf` und `--dfa`; ULF kann isoliert berechnet werden.

## Gap-Verhalten (Begründung)

Kein explizites Gap-Gating. Lomb-Scargle operiert direkt auf `t_sec` (reelle RR-Timestamps inkl. Lücken) und interpoliert nicht; fehlende Beats erscheinen als verringertes Signal-to-Noise im Periodogramm, nicht als Scheinpower. Die einzige Integritätsbedingung ist `ULF_MIN_BEATS` — erfüllen 120 min <3600 Beats, wird NULL ausgegeben.

## Performance

- Lomb-Scargle ist O(N_beats × N_freq). Mit ~7200 Beats × 512 Freqs ≈ 3.7 M Operationen pro Minute.
- Laufzeit-Abschätzung (scipy.signal.lombscargle, C-kompiliert): ~50–200 ms pro Minute → für eine Nacht von 480 min ≈ 1–2 min, für den vollen Datensatz (geschätzt ~20–50k Minuten) ca. 30–90 min.
- Falls zu langsam: Wechsel auf `astropy.timeseries.LombScargle.autopower(method='fast')` (NFFT-basiert, O(N log N)). Optional als zweite Implementierungsstufe.
- Progress-Log im bestehenden 20-Schritt-Raster erweitern um `ulf {time_ulf:.1f}s`.

## Validierung / Akzeptanzkriterien

1. **Schema-Integrität:** Nach Lauf `SELECT COUNT(*) FROM HRV_MINUTE_AGGREGATED WHERE ULF_MS2 IS NOT NULL` > 0 für Nächte mit ≥2 h zusammenhängendem Schlaf.
2. **Plausibilität:** Für Referenz-Minuten tiefer NREM-Schlaf sollte `ULF2_MS2 > ULF1_MS2 × 0.1` gelten (langsame Drift dominiert tiefschlaf-nahe Intervalle). Für REM-nahe Minuten umgekehrt.
3. **Synthetischer Sinus-Test** (Einmal-Check, nicht persistent): RR-Reihe mit bekanntem Sinus bei 0.001 Hz und Amplitude 20 ms → integrierte Power im Band `[0.0005, 0.0033]` ≈ 200 ms² (= 20²/2). Toleranz ±30 %.
4. **Laufzeit-Report** im bestehenden Timing-Summary-Block.
5. **Kein Regressions-Impact** auf VLF/LF/HF/DFA: Ohne `--ulf` muss das Output-Schema und alle Werte bit-identisch zum Pre-Change-Stand sein (abgesehen von den drei neuen — und dann NULL gefüllten — Spalten).

## Out of Scope (explizit ausgeschlossen)

- Coverage-/Quality-Spalte (`ULF_COVERAGE`) — auf User-Wunsch weggelassen.
- Logarithmische Varianten (`LN_ULF`) — weggelassen.
- Anteilsmetrik (`ULF_PCT`) — weggelassen.
- Alternative Fensterlängen (30 min, 60 min) — 120 min ist fest.
- ULF3-Band <0.0001 Hz — außerhalb der Fensterauflösung.

## Kein Commit

Kein commit. Der nutzer reviewed die Änderungen und commited selbst.

(Vor dem Produktionslauf mit `--limit-minutes 200` testen.)
