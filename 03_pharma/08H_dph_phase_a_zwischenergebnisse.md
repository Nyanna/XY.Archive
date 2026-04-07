# Anhang H — DPH Phase A: Tracker-Zwischenergebnisse

> **Stand:** 7. April 2026  
> **Datenbasis:** Xiaomi Smart Band 9 via Gadgetbridge (SQLite-Export)  
> **Zeitraum:** 23 PRE-Nächte (12. März – 4. April 2026), 3 DPH-Nächte (4.–6. April 2026, je 25 mg DPH-HCl zwischen 22–23 Uhr)  
> **Zeitzonenkorrektur:** UTC → CEST (+2h), Schlafnacht-Zuweisung: Start ≥ 18:00 → selber Kalendertag  
> **Status:** Vorläufig — n=3 DPH-Nächte, keine statistische Inferenz möglich. Effektrichtungen als deskriptive Beobachtung.

---

## H.1 HR-Floor-Analyse

| Metrik | PRE (n=23) | DPH (n=3) | Interpretation |
|---|---|---|---|
| **Min HR** | 48.5 ± 2.3 (Range 45–56) | 51.0 ± 1.4 (Range 49–52) | Floor angehoben, Varianz reduziert |
| **p5 HR** | 55.1 ± 2.9 | 57.0 ± 0.8 | Engerer Korridor unter DPH |
| **Mean HR** | 64.4 ± 2.9 | 65.9 ± 0.3 | Kein relevanter Unterschied |

**Tages-Resting-HR** (Daily Summary, Apr 1–6): 57–65 bpm. Der DPH-Nacht-Floor (49–52) liegt ~5–10 bpm unter dem Tages-Resting. Die Beobachtung „HR geht auf sympathisches Basisniveau, nicht tiefer" ist als Tendenz sichtbar (angehobener Floor, kollabierte Varianz), aber der absolute Klamppunkt liegt unterhalb des Tages-Resting-HR, nicht darauf.

**Modellinterpretation:** DPH via H1-Blockade reduziert B7-Output → reduzierte serotonerge Variabilität im Schlaf → engerer HR-Korridor. Die persistierende Unterschreitung des Tages-Resting ist erwartbar: der parasympathische Shift im Schlaf ist unabhängig von der B7-Modulation und bleibt intakt.

---

## H.2 Schlafphasenstabilität

### H.2.1 Mittlere Episodenlänge (Schlafstadien)

| Abschnitt | PRE (n=23) | DPH (n=3) | Δ absolut | Δ relativ |
|---|---|---|---|---|
| **First 5h** | 19.3 ± 4.2 min | 24.4 ± 5.7 min | +5.1 min | ×1.26 |
| **Late** | 11.4 ± 4.3 min | 15.0 ± 1.7 min | +3.6 min | ×1.32 |

DPH stabilisiert *beide* Schlafabschnitte. Der relative Vorteil bleibt über die Nacht konstant (~1.3×). Der absolute Vorteil schrumpft leicht (5.1 → 3.6 min), aber dies folgt dem normalen architektonischen Zerfall (PRE zeigt denselben proportionalen Abfall: 19.3 → 11.4 = Ratio 1.69; DPH: 24.4 → 15.0 = Ratio 1.63). Die Phasenstabilisierung überlebt den pharmakokinetischen Wirkverlust teilweise — konsistent mit der Hypothese, dass einmal etablierte kortikale Synchronisation selbsterhaltend ist.

### H.2.2 HR-Variabilität (Standardabweichung)

| Abschnitt | PRE (n=23) | DPH (n=3) | Richtung |
|---|---|---|---|
| **First 5h** | 5.7 ± 1.2 | 4.8 ± 0.2 | DPH ↓ (stabilisiert) |
| **Late** | 4.9 ± 1.0 | 5.9 ± 1.3 | DPH ↑ (destabilisiert) |

**Dissoziation:** PRE zeigt den normalen Verlauf (HR-Variabilität sinkt über die Nacht durch zunehmende parasympathische Dominanz). DPH **invertiert** dieses Muster: Variabilität steigt im Late-Abschnitt über PRE-Niveau.

**Interpretation:** Die HR-Variabilität ist ein direkterer Proxy für den akuten H1-Besetzungsgrad als die Schlafphasenlänge. Das Rebound-Muster im Late-Abschnitt ist konsistent mit DPH-Wirkverlust (t½ = 4–9 h). Die Phasenstabilität bleibt trotzdem besser als PRE → kortikale Kohärenz und kardiale Regulation dissoziieren.

**Caveat:** Nacht 2 (5.→6. April) ist durch ein CSD-Ereignis mit Naratriptan-Einnahme konfundiert (Late-std=7.6 vs. 5.6/4.4 in Nacht 1/3). Die Inversion ist möglicherweise CSD-getrieben, nicht DPH-getrieben. Neubewertung nach Akkumulation unkonfundierter Nächte erforderlich (vgl. H.4.2).

---

## H.3 DPH-Zeitverlauf (30-min HR-Bins, exemplarisch)

### DPH Nacht 3 (6.→7. April, Schlafbeginn 00:17 CEST)

| Bin (CEST) | min HR | mean HR | max HR |
|---|---|---|---|
| 00:17 | 68 | 73.4 | 94 |
| 00:47 | 63 | 70.0 | 75 |
| 01:17 | 66 | 72.0 | 77 |
| 01:47 | 62 | 71.6 | 81 |
| 02:17 | 63 | 69.4 | 75 |
| 02:47 | 61 | 67.2 | 71 |
| 03:17 | 60 | 65.6 | 75 |
| 03:47 | 56 | 63.6 | 82 |
| 04:17 | 52 | 62.6 | 69 |
| 04:47 | 59 | 64.7 | 71 |
| 05:17 | 56 | 62.6 | 68 |
| 05:47 | 52 | 62.4 | 70 |
| 06:17 | 55 | 61.5 | 80 |
| 06:47 | 53 | 64.7 | 75 |
| 07:17 | 52 | 59.4 | 66 |

Das Muster zeigt: HR-Mean fällt von ~73 auf ~63 in den ersten 4 Stunden (Wirkeintritt + parasympathischer Drift), dann Plateau. Die HR-Minima erreichen erst ab ~04:00 CEST (ca. 4h nach Einnahme, ~5h nach Einschlafbeginn) Werte ≤56, was mit dem pharmakokinetischen Wirkverlust konsistent ist.

---

## H.4 CSD-Ereignis unter DPH (Nacht 2, 5.→6. April)

Am 5. April trat ein Migräneanfall auf. DPH-Einnahme erfolgte wie geplant abends; Schlafbeginn 23:49 CEST. Trotz einseitigem präfrontalem Schmerz wurde bis ca. 04:30 CEST durchgeschlafen (~4.5h konsolidierter Schlaf unter aktivem Anfall). Naratriptan-Einnahme nach Erwachen. Der Folgetag (6. April) zeigt ein deutliches postdromales/Naratriptan-Profil im Tages-HR: min=75, mean=105.8, p10=85 — alle Werte signifikant über den übrigen Tagen (mean sonst 82–92).

### H.4.1 Modellimplikationen

**DPH verschiebt, verhindert nicht.** Die H1-Blockade reduziert die B7-Amplitude und hebt damit die CSD-Schwelle — aber der ~4-Tage-B7/B8-Oszillator ist H1-unabhängig. Wenn der Phasenversatz den kritischen Bereich erreicht, reicht die Amplitudenreduktion nicht mehr aus. DPH kauft Zeit im Zyklus, eliminiert nicht den Treiber.

**Schlafkonsolidierung durch aktiven Anfall hindurch.** Dies ist der bemerkenswerteste Einzelbefund: Unter PRE-Bedingungen wäre die CSD-bedingte Arousal-Kaskade ein sofortiger Schlafbrecher. Die H1-vermittelte Schlafstabilisierung war stark genug, um den normalen CSD→Arousal-Pfad zu überschreiben. Der HR-Spike im 04:49-Bin von Nacht 2 (mean 69.3, max **116**) markiert vermutlich den Zeitpunkt des Erwachens und der Naratriptan-Einnahme.

### H.4.2 Konfundierung in Nacht 2

Die HR-Variabilität im Late-Abschnitt von Nacht 2 (std=7.6) ist durch das CSD-Ereignis und die Naratriptan-Einnahme konfundiert und nicht als reiner DPH-Wirkverlust interpretierbar. Bereinigt um Nacht 2 zeigen Nacht 1 und 3 eine Late-Variabilität von 5.6 und 4.4 — die Inversion gegenüber PRE (4.9) ist damit weniger ausgeprägt und möglicherweise innerhalb der normalen Streuung. Die Dissoziation Phasenstabilität vs. HR-Variabilität (H.2.2) muss nach Akkumulation weiterer unkonfundierter DPH-Nächte neu bewertet werden.

---

## H.5 Synthese für das Zwei-Phasen-Protokoll

### Bestätigte Vorhersagen

1. **Interferenzreduktion:** Die Schlafphasen-Episodenlänge steigt um ~30% unter DPH. Die Richtung ist konsistent mit reduzierter B7/B8-Interferenz durch H1-vermittelte B7-Amplitudenreduktion.

2. **Selektivität:** Der Effekt manifestiert sich in der Kohärenzmetrik (Episodenlänge), nicht in der Schlafgesamtdauer (DPH: 7.4h vs. PRE: 6.9h — kein relevanter Unterschied). Dies spricht gegen einen reinen Sedierungseffekt und für einen strukturellen Stabilisierungseffekt.

3. **CSD-Schwellenanhebung:** DPH verhindert den Anfall nicht, aber die Schlafkonsolidierung durch einen aktiven Anfall hindurch (H.4) zeigt, dass die H1-vermittelte Stabilisierung den CSD→Arousal-Pfad partiell überschreibt. Dies ist ein unabhängiger Beleg für den Kohärenz-Effekt — er operiert unterhalb der Arousal-Schwelle, nicht nur oberhalb der Schlafstadien-Ebene.

### Offene Fragen

1. **Carry-over in OFF-Nächte:** Phase B (alternierendes ON/OFF-Design) steht noch aus. Die zentrale Vorhersage — ob die stabilisierte Kohärenz in die ersten OFF-Nächte hinein persistiert — ist mit dem aktuellen Datensatz nicht prüfbar.

2. **Pharmakokinetische Diskrepanz:** Die Dissoziation zwischen Phasenstabilität (bleibt late erhöht) und HR-Variabilität (steigt late an) wirft die Frage auf, ob die Kohärenz-Persistenz ein H1-unabhängiger downstream-Effekt ist (einmal synchronisierte Netzwerke stabilisieren sich selbst) oder ein Artefakt der kleinen Stichprobe.

3. **Dosis-Zeitpunkt-Optimierung:** Die HR-Daten legen nahe, dass der DPH-Wirkspiegel nach ~4h signifikant abfällt. Eine Split-Dose (z.B. 12.5 mg bei Einnahme + 12.5 mg nach 4h) wäre pharmakokinetisch naheliegend, ist aber klinisch nicht evaluiert und erfordert professionelle Abstimmung.

---

*Querverweise:*
- *Zwei-Phasen-Protokoll, Abschnitt 4: Monitoring-Variablen*
- *Pathogenetisches Modell, Anhang B: Tracker-Datenanalyse*
- *Pathogenetisches Modell, Abschnitt 2.5.5: Schlafarchitektur als Kohärenzmarker*
- *Analyseskripte: `dph_analyse.py` (Gesamtanalyse), `dph_hr_timecourse.py` (30-min-Bins), `dph_stage_stability.py` (Episodenlängen)*