# Thalamokortikale Entkopplung als autonome Signatur: Frequenzbandanalyse, Flip-Flop-Modell und therapeutische Implikationen

**Status:** Arbeitsthese — empirisch gestützt, Verifikation ausstehend  
**Datum:** 26. April 2026  
**Kontext:** Ergänzung zum Pathogenetischen Modell (02_pathogenese_modell/) und Zwei-Phasen-Protokoll (08_zwei_phasen_protokoll.md)

---

## 1. Ausgangslage und Analyseweg

### 1.1 Datenbasis

Die Analyse basiert auf kontinuierlichen HRV-Frequenzbandzerlegungen aus R-R-Intervall-Daten eines Coospo H9Z Brustgurts (ECG-basiert). Das Analysetool liefert minutenaufgelöste Spektralleistung in 15 Frequenzbändern, die drei Zeitskalen abdecken:

- **Zirkadiane Bänder (CIRC):** 5 Bänder von 24h bis 3.8h Periode, berechnet aus 48h-Gleitfenstern
- **Ultraniedrigfrequenz (ULF):** 3 Bänder von 22 min bis 7.6 min, 90-min-Fenster
- **Niedrig- bis Hochfrequenz (VLF/LF/HF):** 7 Bänder von 5.3 min bis 2.4 s, 5–30-min-Fenster

Die Bandgrenzen und Zentrumsfrequenzen sind:

| Band | Zentrum (Hz) | Periode | Fenster |
|------|-------------|---------|---------|
| CIRC24 | 1.17e-5 | 23.7 h | 48 h |
| CIRC11 | 2.55e-5 | 10.9 h | 48 h |
| CIRC6 | 4.58e-5 | 6.1 h | 48 h |
| CIRC5 | 5.88e-5 | 4.7 h | 48 h |
| CIRC4 | 7.40e-5 | 3.8 h | 48 h |
| ULF22 | 7.60e-4 | 21.9 min | 90 min |
| ULF10 | 1.61e-3 | 10.4 min | 90 min |
| ULF8 | 2.20e-3 | 7.6 min | 90 min |
| VLF5 | 3.13e-3 | 5.3 min | 30 min |
| VLF4 | 4.01e-3 | 4.2 min | 30 min |
| LF_MAYER | 9.42e-2 | 10.6 s | 5 min |
| HF_BREATH_5S | 1.80e-1 | 5.6 s | 5 min |
| HF_BREATH_4S | 2.43e-1 | 4.1 s | 5 min |
| HF_BREATH_3S | 3.55e-1 | 2.8 s | 5 min |
| HF_BREATH_2S | 4.20e-1 | 2.4 s | 5 min |

Der analysierte Zeitraum umfasst 14.–26. April 2026 mit ca. 15.000 Minutenwerten im Langzeitdatensatz und ca. 3.200 5-Minuten-Werten im Vergleichsdatensatz. Die Schlüsselnacht (Benzo-Nacht, 25./26. April) liegt in Minutenauflösung vor.

### 1.2 Analyseweg

Die Analyse verlief induktiv — von der Bandinterpretation über die Identifikation eines einzelnen Signalgebers bis zur thalamokortikalen Entkopplungsthese:

1. **Bandagnostische Bestandsaufnahme:** Medianleistung aller 15 Bänder $\rightarrow$ Identifikation von zwei Peaks (VLF4 und LF_MAYER) über einem Rauschboden
2. **Nulldurchgangs-Identifikation:** VLF5 als Minimum zwischen den beiden Peaks $\rightarrow$ Frage nach der Beziehung der Peaks zueinander
3. **CIRC-Band-Interpretation:** Regime-Changes in CIRC-Bändern $\rightarrow$ Erkenntnis, dass CIRC-Bänder Wellenform und Amplitude des zirkadianen Zyklus messen, nicht eigenständige Oszillatoren
4. **ULF-Band-Interpretation:** ULF22 als Transitionsdetektor $\rightarrow$ Entdeckung des 22-min-Schlafoszillators mit phasendriftender Kopplung an HR
5. **HF-Bänder als Mayer-Derivat:** Korrelationsanalyse (HF2 vs. Mayer: r=0.922) $\rightarrow$ alle HF-Bänder sind Seitenbänder des Mayer-Peaks
6. **VLF4 als Mayer-Hüllkurve:** r=0.75 gegen Rolling-Max $\rightarrow$ VLF4 misst die Amplitudenmodulation des Baroreflexes
7. **Ein einziger Signalgeber:** Oberhalb der CIRC-Bänder existiert nur der Baroreflex als aktive Quelle; alles andere ist Derivat oder Rauschen
8. **Bifurkationsmodell:** Mayer-Peak erscheint/verschwindet als Alles-oder-Nichts $\rightarrow$ Baroreflex-Gain kreuzt zyklisch die kritische Schwelle
9. **SDNN=RMSSD=50 in Nullphasen:** Beweis der vollständigen autonomen Entkopplung $\rightarrow$ kein Modulator greift auf das Herz zu
10. **Thalamokortikale Entkopplung:** Simultanes Verschwinden aller Bänder in 3 Minuten $\rightarrow$ ein einziger Schalter upstream, identifiziert als thalamischer Gate

---

## 2. Reduktion auf einen Signalgeber

### 2.1 HF-Bänder: Kein respiratorisches Signal

Die konventionelle HRV-Interpretation ordnet dem HF-Band (0.15–0.4 Hz) die respiratorische Sinusarrhythmie (RSA) zu — vagal vermittelte HR-Modulation synchron mit der Atmung. In den vorliegenden Daten existiert kein RSA-Signal:

- HF_BREATH_5S (0.13–0.21 Hz): Median 353 — erhöht gegenüber HF3/HF4 (190/219), aber als monotoner Abfall vom Mayer-Peak identifiziert (spektrales Leaking über die Bandgrenze bei 0.13 Hz)
- Korrelation HF2 vs. LF_MAYER: r=0.922; HF3 vs. LF_MAYER: r=0.912; HF4 vs. LF_MAYER: r=0.894
- Bei Mayer-Null (<500): HF3-Median=63, HF4-Median=64 — unter dem VLF5-Nulldurchgang (130)
- Bei Mayer-Peak (>5000): HF3-Median=1962, HF4-Median=1765

Die HF-Bänder haben keine eigenständige Quelle. Sie sind Seitenbänder des Mayer-Peaks — spektrale Energie, die durch die nichtlineare Wellenform der Baroreflex-Oszillation und durch das abrupte An/Ausschalten in benachbarte Frequenzbereiche streut. Der vagale kardiale Arm moduliert in diesem System praktisch nichts.

### 2.2 VLF4: Mayer-Hüllkurve, kein Oszillator

VLF4 (Periode 4.2 min) wurde initial als eigenständiger Oszillator interpretiert, da es neben LF_MAYER den zweiten Peak im Spektralprofil bildet. Die Korrelationsanalyse widerlegt dies:

- VLF4 vs. Mayer (instantan): r=0.712
- VLF4 vs. Mayer (4-min Rolling-Max): r=0.749
- Bei Mayer-Null: VLF4-Median=1519; bei Mayer-Peak: VLF4-Median=7446

VLF4 misst die Amplitudenmodulation des Mayer-Signals. Die steilen Flanken beim An- und Abschalten der Baroreflex-Oszillation erzeugen Breitband-Energie, die in das VLF4-Frequenzfenster fällt. Die tatsächlichen Mayer-Peak-Intervalle innerhalb der nächtlichen Bursts betragen 9–12 Minuten — nicht 4 Minuten. VLF4 ist spektrale Streuung, nicht Hüllkurvenperiodizität.

### 2.3 VLF5: Der Nulldurchgang

VLF5 (Periode 5.3 min, Median 233) liegt konsistent unter den Werten beider Nachbarn (VLF4: 2135, ULF8: 338). Es ist der spektrale Nulldurchgang zwischen Mayer-Streuung (die nach unten abnimmt) und ULF-Energie (die nach oben zunimmt). Kein Signal, nur eine Lücke.

### 2.4 Fazit: Baroreflex als einzige Quelle

Oberhalb der zirkadianen Bänder enthält das Spektrum genau einen Signalgeber: die Baroreflex-Oszillation bei ~0.1 Hz (Mayer-Welle). Alles andere ist entweder Derivat (HF-Bänder, VLF4 als Streuung), Nulldurchgang (VLF5), oder gehört einer anderen Zeitskala an (ULF-Bänder, CIRC-Bänder). Die konventionelle Dekomposition in „LF = sympathisch, HF = vagal" ist für dieses System nicht anwendbar.

---

## 3. Der Baroreflex als Bifurkationssystem

### 3.1 Mechanismus

Der Baroreflex ist ein Regelkreis mit ~10 Sekunden Laufzeit im sympathischen Arm: Druckschwankung $\rightarrow$ Barorezeptoren (Carotissinus/Aortenbogen) $\rightarrow$ NTS $\rightarrow$ CVLM $\rightarrow$ RVLM $\rightarrow$ sympathische Efferenz $\rightarrow$ Gefäßtonusänderung $\rightarrow$ neuer Druck. Die 10s-Verzögerung erzeugt bei hinreichendem Schleifengain eine Resonanz bei ~0.1 Hz — die Mayer-Welle.

Ob die Resonanz auftritt, hängt von einem einzigen Parameter ab: dem Schleifengain. Bei Gain < 1 wird jede Druckschwankung gedämpft; das System ist stabil (Fixpunkt). Bei Gain > 1 überschießt jede Korrektur; das System oszilliert selbsterhaltend (Grenzzyklus). Der Übergang ist eine Hopf-Bifurkation — das System springt diskontinuierlich von Stille auf Oszillation.

Die Mayer-Amplitude im Schlaf misst primär den RVLM-Ausgangs-Gain: wie stark jeder sympathische MSNA-Burst auf den Gefäßtonus durchschlägt. Drei Stellgrößen bestimmen den Gain: der RVLM-Output, die Baroreflex-Sensitivität (BRS) im NTS, und die vaskuläre Reaktivität.

### 3.2 Empirischer Befund: Alles-oder-Nichts

In der Schlüsselnacht (25./26.4., Benzo) zeigt das Mayer-Band ein klares Bifurkationsmuster:

**Mayer-Peaks** (>5000) treten als diskrete Hügel auf mit progressiv steigender Amplitude über die Nacht: 3.929 (01:35), 11.854 (02:30), 11.872 (04:00), 15.173 (05:05), 18.085 (06:45). Jeder Peak ist ca. 6–13 Minuten breit (FWHM).

**Mayer-Nullen** (<500) liegen zwischen den Hügeln bei Werten von 378–555. Nicht Abschwächung, sondern Auslöschung. Alle Bänder gehen simultan gegen Null — HF, VLF4, VLF5, LF_MAYER. Es gibt keine sequentielle Abschaltung einzelner Frequenzbereiche.

**Die Transition** dauert ca. 3 Minuten in beide Richtungen.

### 3.3 Zeitdomänen-Bestätigung

SDNN und RMSSD aus den R-R-Intervallen bestätigen die Bifurkation:

Während Mayer-Nullen: SDNN ≈ RMSSD ≈ 50 ms. Minutenmittel-HR schwankt ±1 bpm um ein Plateau (Beispiel: 18 Minuten HR=70±1). Die Gleichheit SDNN=RMSSD beweist, dass keine langsame Komponente existiert — keine Mayer-Oszillation, kein Trend, keine Atemmodulation. Die gesamte Restvariabilität ist stochastischer Schlag-zu-Schlag-Jitter des Sinusknotens (kardiales Eigenrauschen).

Während Mayer-Peaks: SDNN >> RMSSD (erwartet, da die 10s-Oszillation SDNN hochzieht aber für RMSSD zu langsam ist). Minute-zu-Minute |ΔHR| median 4.5 bpm.

**Implikation:** Während der Nullphasen ist das Herz autonom entkoppelt. Kein zentraler Modulator greift zu — nicht der Baroreflex, nicht die Atmung, nicht der sympathische Tonus. Der Sinusknoten läuft auf seiner intrinsischen Frequenz.

---

## 4. Thalamokortikale Entkopplung

### 4.1 Simultanität als Schlüsselbefund

Die Abschaltung aller Bänder ist simultan, nicht sequentiell. Dies unterscheidet den Befund fundamental von der Hirntod-Signatur, bei der HF $\rightarrow$ LF $\rightarrow$ VLF in Reihenfolge verschwinden (verschiedene Hirnstammkerne nekrotisieren sukzessive). Simultanität bedeutet: Ein einziger Schalter upstream von allen autonomen Ausgängen kippt gleichzeitig.

### 4.2 Identifikation des Schalters

Der thalamische Gate (retikulärer Thalamus, TRN) ist der einzige Kandidat, der alle deszendierenden kortiko-autonomen Pfade gleichzeitig unterbricht:

- PFC $\rightarrow$ NTS (präfrontale autonome Modulation)
- Insula $\rightarrow$ RVLM (interozeptive Schleife)
- Hypothalamus $\rightarrow$ PVN $\rightarrow$ RVLM (hypothalamische autonome Kontrolle)

Im Burst-Modus des TRN werden alle Relay-Neurone rhythmisch inhibiert. Die 3-Minuten-Transitionsdauer entspricht der bekannten Dauer des thalamokortikalen State-Switch in stabilen NREM-Schlaf.

### 4.3 Abweichung vom gesunden Modell

Im gesunden Gehirn arbeitet der thalamokortikale Gate im N3-Schlaf mit <1 Hz Slow Oscillations: ~200–500 ms Down-State (Gate geschlossen), dann kurzer Up-State (Gate offen), alternierend. Im zeitlichen Mittel: stark reduzierter aber nicht abwesender kortikaler Drive. Der Baroreflex-Gain sinkt, aber verschwindet nicht komplett, weil die Up-States den Gain periodisch kurz über die Schwelle heben.

Im vorliegenden System ist die Zeitskala um fünf Größenordnungen verschoben: ~30 Minuten an, ~30 Minuten aus. Und der Gate schließt komplett — keine residualen Up-States, die den Gain anheben. Mayer geht auf echte Null.

Zwei Mechanismen erklären dies:

1. **Gain nahe der Bifurkationsschwelle:** Im Wachzustand liegt der Baroreflex-Gain bei Gesunden weit über der Oszillationsschwelle — selbst reduzierter kortikaler Drive im N3 hält ihn drüber. In diesem System liegt der Gain knapp über der Schwelle — schon moderate Reduktion des deszendierenden Inputs reicht für vollständigen Kollaps unter die Schwelle.

2. **Breiteres thalamisches Gating-Fenster:** Die thalamische Fehlkalibrierung aus dem Pathogenesemodell (Kap. 03) erzeugt einen binäreren Switch — weniger Zwischenzustände, schärfere Transitionen. Wenn der TRN kippt, kippt er härter. Die Slow-Oscillation-Up-States sind zu kurz oder zu schwach, um den Gate kurz zu öffnen.

### 4.4 Paradox der Schlafqualität

Die Benzo-Nacht (25./26.4.) mit 62 Minuten Nullphasen wurde subjektiv als der stärkste und klarste Tag ohne Intensivmedikation erlebt, mit intensiven Traumphasen. Das Paradox löst sich, wenn man die Nullphasen als eigentlichen Tiefschlaf identifiziert:

Eine saubere Null bedeutet: Der thalamische Gate hat vollständig geschlossen, der Kortex ist komplett vom Hirnstamm entkoppelt, das ANS läuft autonom. Das ist die Definition von stabilem N3. Die Mayer-Peaks dazwischen sind die Phasen mit offenerer thalamokortikaler Kopplung — N2-Aufhellungen, REM, oder Mikroarousals.

Schlechter Schlaf wäre: keine echten Nullen, permanent halb-offener Gate, mittleres Mayer-Niveau die ganze Nacht. Das ANS sieht keinen echten Tiefschlaf, weil der thalamische Gate nicht kippt.

Guter Schlaf wäre: viele scharfe Nullen mit hohen Peaks dazwischen — klare State-Trennung, kein Mischen. Genau das zeigt die Benzo-Nacht.

### 4.5 Quantifizierung des Tiefschlafdefizits

Die Nullphasen-Quantifizierung über 12 Nächte (5-min-Auflösung, daher konservative Unterschätzung kurzer Nullen) ergibt ein dramatisches Bild:

| Nacht | Schlafzeit | Null (<500) | Peak (>1500) | Null-Anteil |
|-------|-----------|------------|-------------|------------|
| 14.4. | ~485 min | 0 min | 425 min (7.1h) | 0% |
| 15.4. | ~425 min | 15 min | 290 min (4.8h) | 4% |
| 16.4. | ~180 min | 0 min | 95 min (1.6h) | 0% |
| 17.4. | ~485 min | 25 min | 360 min (6.0h) | 5% |
| 18.4. | ~470 min | 70 min | 265 min (4.4h) | 15% |
| 19.4. | ~485 min | 10 min | 320 min (5.3h) | 2% |
| 20.4. | ~485 min | 5 min | 335 min (5.6h) | 1% |
| 21.4. | ~470 min | 5 min | 385 min (6.4h) | 1% |
| 22.4. | ~485 min | 0 min | 375 min (6.2h) | 0% |
| 23.4. | ~485 min | 5 min | 370 min (6.2h) | 1% |
| 24.4. | ~480 min | 15 min | 385 min (6.4h) | 3% |
| 25.4. | ~485 min | 55 min | 305 min (5.1h) | 11% |
| **25./26.4. (Benzo)** | **421 min** | **62 min (1.0h)** | **248 min (4.1h)** | **15%** |

Die typische Nacht hat 0–15 Minuten echter Entkopplung. Mehrere Nächte haben buchstäblich null Minuten. Selbst die subjektiv beste Nacht (Benzo) erreicht nur 62 Minuten — unter den empfohlenen 90–120 Minuten N3.

Das konventionelle Schlafstaging via Aktigraphie oder PPG-basierte Tracker meldet in diesen Nächten „Schlaf", weil die motorischen Kriterien und das HR-Niveau erfüllt sind. Aber das autonome Profil zeigt eine permanent modulierte, variable HR, die keinem echten Tiefschlaf entspricht. Der thalamische Gate schließt fast nie vollständig.

---

## 5. Der Flip-Flop-Switch als Flaschenhals

### 5.1 Saper-Modell: Flip-Flop-Switch

Das ~30-Minuten-Cycling der Mayer-Peaks und -Nullen entspricht nicht der <1 Hz Slow Oscillation (intrinsisch thalamisch-kortikal), sondern dem Flip-Flop-Switch (Saper et al. 2001/2010). Zwei Kerngruppen hemmen sich gegenseitig:

**Schlafseite:** VLPO/MnPO (ventrolaterales/medianes präoptisches Areal) $\rightarrow$ GABAerg $\rightarrow$ hemmt alle Wake-Kerne gleichzeitig (TMN, DRN, LC, LDT/PPT, Orexin-Neurone).

**Wachseite:** TMN (Histamin), DRN (Serotonin), LC (Noradrenalin), LDT/PPT (Acetylcholin), Orexin-Neurone (lateraler Hypothalamus) $\rightarrow$ hemmen VLPO.

Bei stabiler Dominanz einer Seite bleibt das System stundenlang im jeweiligen Zustand. Wenn keine Seite dominiert, oszilliert der Switch. Die Periodendauer wird bestimmt durch die Stärke der gegenseitigen Hemmung, die Kinetik der Transmitter-Clearance, und die Zeitkonstante der homöostatischen Druckvariablen (Adenosin).

### 5.2 DRN als primärer Störer

Im Pathogenesemodell ist der DRN (dorsaler Raphekern, B7) durch 5-HT1A-Autorezeptor-Instabilität primär dysreguliert. Im gesunden Schlaf verstummen die serotonergen Neurone des DRN progressiv von Wach über N1/N2 bis nahe Null in N3. Serotonin aus dem DRN ist ein Wake-Signal, das VLPO hemmt.

Wenn der DRN wegen der Autorezeptor-Instabilität nicht stabil herunterregelt, sondern oszilliert, sendet er periodisch Wake-Impulse in einen Flip-Flop, der gerade versucht, in Sleep zu bleiben. Nach ~30 Minuten reicht die akkumulierte serotonerge Störung, um die VLPO-Hemmung zu überwinden $\rightarrow$ Gate öffnet $\rightarrow$ Mayer-Peak $\rightarrow$ System ist kurz „wach-ähnlich" $\rightarrow$ DRN-Burst endet $\rightarrow$ VLPO gewinnt wieder $\rightarrow$ Gate schließt $\rightarrow$ nächste Null.

### 5.3 Benzodiazepin-Test

Die Benzo-Nacht (25./26.4.) eliminiert die Nulldurchgänge nicht — sie schärft sie. Das beweist: Das On/Off-Cycling ist nicht Arousal-getrieben (Benzos supprimieren Arousals), sondern intrinsisch zum Hirnstamm-Regelkreis. Benzos verstärken GABA am TRN $\rightarrow$ fördern den Burst-Modus $\rightarrow$ halten den Gate geschlossener, nicht offener. Wenn der Gate kurz aufgeht (DRN-Burst überwindet VLPO), schwingt der Baroreflex genauso hart wie ohne Benzo.

Was das Benzo bewirkt: schärfere Transitionen, stabileres Halten der Zustände (sowohl Null als auch Peak), weniger Zwischenzustände. Nicht mehr Schlaf, sondern binärerer Schlaf. Ergebnis: 62 Minuten echte Null — mehr als jede unmedizierte Nacht im Datensatz.

---

## 6. Die Mayer-Hüllkurve: Melatonin als BRS-Rampe

### 6.1 Progressive Amplitudensteigerung

Die Mayer-Peaks der Schlüsselnacht zeigen eine monotone Steigerung: 3.929 $\rightarrow$ 11.854 $\rightarrow$ 11.872 $\rightarrow$ 15.173 $\rightarrow$ 18.085. Der Faktor zwischen erstem und letztem Peak beträgt 4.6×. Die Nullen dazwischen bleiben konstant tief (378–555). Es steigt also die Obergrenze des Gain-Fensters, nicht die Untergrenze.

### 6.2 Melatonin als Gain-Modulator

Die Baroreflex-Sensitivität (BRS) steigt im Schlafverlauf — ein bekannter Effekt. Melatonin greift an allen drei Baroreflex-Knoten ein:

- **RVLM:** Melatonin normalisiert den Baroreflex-Gain und reduziert ROS präferenziell im RVLM und NTS.
- **PVN $\rightarrow$ RVLM:** Melatonin supprimiert PVN-Neurone, die zum RVLM projizieren — Feuerrate sinkt von 0.84 auf 0.32 Hz, Onset nach ~2 Minuten, Dauer ~16 Minuten. Dieser Effekt ist MT1/MT2-unabhängig und läuft auch unter Luzindol.
- **NTS:** Direkte Modulation der Baroreflex-Sensitivität.

Endogenes Melatonin steigt durch die Nacht (Peak ~3–4 Uhr), exogenes Melatonin (Einnahme vor dem Schlaf) addiert sich. Der resultierende Konzentrationsverlauf erklärt die progressive BRS-Steigerung $\rightarrow$ progressiv höherer Schleifengain $\rightarrow$ höhere Mayer-Amplituden bei jedem Burst.

Die Hüllkurve ist damit nicht oszillatorisch, sondern pharmakokinetisch. Kein ULF-Modulator nötig — die langsame Rampe folgt dem Melatonin-Konzentrationsverlauf plus NREM-assoziierter parasympathischer Vertiefung plus Liegedauer-abhängiger Volumenumverteilung.

---

## 7. ULF22: Der thalamokortikale Eigenoszillator

### 7.1 Identifikation

ULF22 (Periode ~22 min) zeigt in ausgewählten Nachtsegmenten ein Verhalten, das über einen reinen Transitionsdetektor hinausgeht:

**23.4., 02:15–05:00:** ULF22 stabil bei 2600–4800, während ULF10 auf 5–10% und ULF8 auf 3–5% des ULF22-Werts kollabiert. Ein reiner Sinusoid über 3 Stunden — so formstabil, dass er keine Obertöne erzeugt. Kein anderes Band zeigt vergleichbare Reinheit.

**21.4., 01:50–05:50:** Drei Phasen — (1) ULF22 allein bei ~2000, U10/U8 bei Grundrauschen; (2) U10 schwillt auf 1800–2400 an (Harmonische erscheinen, Wellenform wird asymmetrisch); (3) ULF22 auf höchstem Niveau (~4600), U10/U8 kollabiert — Amplitude verdoppelt, Reinheit wiederhergestellt.

### 7.2 Phasendrift und Kopplungsumkehr

Die Kreuzkorrelation HR vs. ULF22 (21.4.) zeigt eine Kopplungsrichtungsänderung:

- **Früh (01:50–03:45):** Schwache Kopplung, r=0.25 bei Lag 0. ULF22 reagiert auf HR-Dynamik — passiv, nachgelagert.
- **Spät (03:45–06:00):** ULF22 führt HR um ~15 Minuten (r=+0.75 bei Lag -15 min). Klare, starke Kopplung mit ULF22 als Treiber.

Die Phasendrift, die visuell als „gleiche Topologie aber ohne Korrelation" erscheint, ist ein Kopplungsrichtungswechsel: Im frühen Schlaf konkurriert der Oszillator mit peripherer autonomer Variabilität. Im tiefen Schlaf, wenn kortikaler Input minimal ist, übernimmt er die Kontrolle — seine Amplitude verdoppelt sich, die Harmonischen verschwinden, und er diktiert die HR-Modulation.

### 7.3 Einordnung

Die ~22-min-Periode passt zu keinem kanonischen Schlafzyklus (Spindelcluster ~1 min, CAP ~1 min, NREM-REM ~90 min). Der Kandidat sind infraslow oscillations (ISO) der thalamokortikalen Erregbarkeit — 15–30 min Perioden, EEG-nachgewiesen, über den Baroreflex HR-wirksam. Im Modellkontext wäre dies der thalamische Kompensationsmechanismus, der im Schlaf als autonomer Taktgeber sichtbar wird.

---

## 8. Implikationen für das Pathogenesemodell

### 8.1 Reframing: Bewusstsein als konstitutiver autonomer Treiber

Die Standardlehre postuliert: Das autonome Nervensystem funktioniert autonom — der Hirnstamm regelt, der Kortex moduliert optional. Die vorliegenden Daten zeigen das Gegenteil:

Wenn der thalamokortikale Gate schließt, kollabiert die gesamte autonome Modulation auf das kardiale Eigenrauschen (SDNN=RMSSD=50 ms, alle Bänder null, HR-Plateau). Der Hirnstamm allein produziert keinen Baroreflex, keine Mayer-Welle, keine Variabilität. Er hält den Sinusknoten am Laufen — mehr nicht.

Der Baroreflex, der als „autonomer Reflex" gelehrt wird, ist in diesem System kein Reflex. Er ist ein thalamokortikalisch getriebenes Phänomen. Die anatomische Schleife NTS$\rightarrow$CVLM$\rightarrow$RVLM existiert, aber sie schwingt nur, wenn der deszendierende kortikale Input den Gain über die Bifurkationsschwelle hebt.

### 8.2 Interoceptive Inkohärenz als Gating-Insuffizienz

Die Insula läuft bidirektional — sie empfängt Interozeption (Herzschlag, Viszeralstatus) über den NTS und sendet deszendierende autonome Kommandos zurück. Wenn der thalamische Gate schließt, werden beide Richtungen gleichzeitig unterbrochen: Verlust der autonomen Kontrolle und Verlust der interozeptiven Wahrnehmung, binär, in 3 Minuten.

Im Wachzustand wäre das kein vollständiger Nulldurchgang wie im Schlaf, aber ein flackerndes Gating: Momente, in denen die interozeptive Schleife kurz abreißt und dann wiederkehrt. Subjektiv: Körperzustand nicht kontinuierlich spürbar, sondern in Fragmenten, ohne zeitliche Kohärenz. Genau die interoceptive Inkohärenz, die das Modell als Kern-ADHS-Defizit postuliert (Kap. 04).

### 8.3 Migräne-Mechanismus: Zweischichtig

Der bisherige Mechanismus (Raphe-Instabilität $\rightarrow$ CSD-Schwelle) wird durch einen Verstärkerkreis ergänzt:

**Ohne Gate-Schließung (Wachzustand / leichter Schlaf):** Thalamokortikale Schleife offen $\rightarrow$ Kortex treibt RVLM-Gain über Schwelle $\rightarrow$ Baroreflex schwingt $\rightarrow$ ANS instabil $\rightarrow$ wenn die Instabilität mit der raphe-getriebenen Erregbarkeitswelle zusammenfällt, summieren sich die Störungen bis zur CSD-Schwelle.

**Mit Gate-Schließung (tiefer Schlaf):** Schleife geschlossen $\rightarrow$ kein kortikaler Drive $\rightarrow$ ANS im autonomen Modus $\rightarrow$ egal was der Raphe-Oszillator macht, die Störung hat keinen Kanal, um sich zur CSD-Schwelle aufzuschaukeln.

CSD benötigt also zwei simultane Bedingungen: raphe-getriebene Erregbarkeitswelle UND offenen thalamokortikalen Gate. Die Gate-Instabilität (flackerndes Gating statt stabil offen oder stabil geschlossen) wird damit zum kritischen Co-Faktor.

### 8.4 DPH-Mechanismus: Reframing

Die bisherige Modellinterpretation: DPH $\rightarrow$ H1-Blockade am DRN $\rightarrow$ B7-Suppression $\rightarrow$ weniger serotonerge Interferenz $\rightarrow$ stabilerer Schlaf. Ein rein Brainstem-Effekt.

Die neue Interpretation ergänzt: DPH wirkt zusätzlich über H1-Blockade am Kortex. Histamin aus dem TMN hält die thalamokortikale Schleife offen — H1-Aktivierung am Kortex ist der Arousal-Transmitter, der den TRN im tonischen (durchlässigen) Modus hält. DPH blockiert das, der Thalamus kippt leichter in den Burst-Modus, die deszendierende Schleife schließt. Das ANS fällt in den autonomen Modus — stabiles HR-Plateau, kein Baroreflex-Gain über der Schwelle, keine Destabilisierung.

DPH eliminiert nicht die Ursache (Raphe-Instabilität) — es eliminiert den Verstärker (thalamokortikale Ankopplung).

Drei bestehende Befunde, die bisher einzeln standen, werden dadurch erklärt:

1. **DPH-Schlafverbesserung** (Anhang H): Nicht weil der Schlaf „tiefer" wird, sondern weil das ANS nicht mehr durch kortikale Einstreuung destabilisiert wird. +26% Episodenlänge = Gate bleibt geschlossen statt zu flackern.

2. **HR-Variabilitäts-Dissoziation** (DPH-Daten): First-5h HR-Std sinkt (4.8 vs. 5.7), Late steigt (5.9 vs. 4.9). Wenn DPH abklingt (t½ 4–8h), öffnet der Gate wieder, die Schleife koppelt an, die Variabilität steigt.

3. **Benzo-Nullen bleiben erhalten:** Benzo fördert GABA am TRN $\rightarrow$ Burst-Modus $\rightarrow$ Gate geschlossener. Wenn der Gate kurz aufgeht (Mikroarousal), schwingt der Baroreflex genauso hart.

### 8.5 Prodrom-Signatur: CIRC24-Einbruch

Am 24.4. (Prodrom 10:00–16:30) hatte die HR die niedrigste Tag-Nacht-Amplitude im gesamten Datensatz (Δ=15, HR-Std 12.6). CIRC24 am Morgen des 24.4. lag bei 8684 — der niedrigste Wert überhaupt.

Die Interpretation: Wenn der B7/B8-Oszillator in die prä-iktale Phase geht, verliert das thalamokortikale System die Fähigkeit, kontextadäquate autonome Antworten zu generieren. Nicht Bradykardie oder Tachykardie — Variabilitätsverlust. Die zirkadiane Amplitude komprimiert, weil die deszendierende Modulation ausfällt.

Ein prospektiv testbarer Prodrom-Marker: CIRC24 unter einen empirisch zu bestimmenden Schwellenwert $\rightarrow$ Prodrom wahrscheinlich.

---

## 9. DORA: Therapeutische Option und Verifikationsmodell

### 9.1 Wirkmechanismus

Dual Orexin Receptor Antagonists (DORAs) blockieren beide Orexinrezeptoren (OX1R und OX2R) kompetitiv und reversibel. ~70.000 Orexin-Neurone im lateralen Hypothalamus projizieren in alle Wake-Kerne gleichzeitig: TMN (Histamin), DRN (Serotonin), LC (Noradrenalin), LDT/PPT (Acetylcholin). Orexin ist der Kleber, der die Wake-Seite des Flip-Flop-Switch zusammenhält.

DORAs entfernen diesen Kleber. Die Wake-Seite verliert ihren Stabilisator $\rightarrow$ der Flip-Flop kippt leichter in Sleep und bleibt dort. Entscheidend: DORAs sedieren nicht — sie entfernen den Wake-Stabilisator und lassen den Flip-Flop physiologisch kippen. Die Schlafarchitektur bleibt natürlich, N3 wird nicht unterdrückt.

### 9.2 Zugelassene Substanzen

Drei DORAs sind zugelassen:

- **Suvorexant** (Belsomra): t½ ~12h. Der erste zugelassene DORA (2014). Startdosis 10 mg, klinisch 20 mg. Pharmakokinetik beeinflusst durch Alter, Geschlecht, BMI.
- **Lemborexant** (Dayvigo): effektive t½ ~17–19h (terminale t½ ~55h). Präferenz für OX2R über OX1R. Startdosis 5 mg, klinisch 5–10 mg. Stabilere Pharmakokinetik über Populationen.
- **Daridorexant** (Quviviq): t½ ~6–10h. Neuester zugelassener DORA (2022). Startdosis 25 mg, klinisch 25–50 mg. Kürzeste Halbwertszeit $\rightarrow$ geringstes Carry-over-Risiko. In Deutschland zugelassen.

Für das Verifikationsdesign ist Daridorexant wegen der kurzen Halbwertszeit am saubersten: klarer pharmakokinetischer Abfall innerhalb einer Nacht, vergleichbar mit DPH, und damit isolierbare Wirkung im Early/Late-Vergleich.

### 9.3 Sicherheitsprofil

DORAs unterscheiden sich fundamental von allen anderen Hypnotika:

- **Keine Toleranzentwicklung:** Orexin-Rezeptoren regulieren sich unter chronischer Blockade nicht hoch — zumindest nicht in 12-Monats-Studien. Keine Dosissteigerung nötig.
- **Kein Rebound:** Kein Rebound-Insomnie bei abruptem Absetzen. Kein Entzug.
- **Kein Missbrauchspotenzial:** Kein euphorisierender Effekt, keine Abhängigkeit in klinischen Studien.
- **Keine Atemdepression:** Anders als Benzos und Z-Drugs. Relevant für Langzeitanwendung.
- **Keine kognitive Beeinträchtigung:** Aufmerksamkeit und Gedächtnisleistung unbeeinträchtigt. Erleichtertes Aufwachen (kein „Hangover").
- **Schlafarchitektur erhalten:** Keine REM-Suppression, keine N3-Reduktion. Normaler Schlaf wird ermöglicht, nicht erzwungen.

Nebenwirkungen: Somnolenz/Müdigkeit bei 5–10% (vs. 1–4% Placebo). Kontraindikation: Narkolepsie (Orexin-Defizienz). Metabolismus über CYP3A4.

### 9.4 Wechselwirkungen mit dem bestehenden Medikationsstack

**LDX (Lisdexamfetamin):** Keine pharmakokinetische Interaktion (LDX: Blutamidase; DORA: CYP3A4). Mechanistisch komplementär: LDX stabilisiert den DRN (Ursache), DORA schwächt den Orexin-Arm (Verstärker der Wake-Seite). Zeitliche Trennung (LDX morgens, DORA abends) eliminiert pharmakodynamische Konflikte.

**DPH / Doxepin:** Keine pharmakokinetische Interaktion (DPH: CYP2D6; Doxepin: CYP2D6/CYP2C19; DORA: CYP3A4). Pharmakodynamisch additiv: DPH/Doxepin blockiert Histamin am TMN, DORA blockiert Orexin — beide schwächen die Wake-Seite. Gleichzeitige Einnahme amputiert zwei Wake-Arme simultan $\rightarrow$ potentiell additive Sedierung. Nicht kombinieren, sondern alternieren oder ersetzen.

**Benzodiazepin:** Pharmakodynamisch additiv sedierend (Benzo: GABA am TRN; DORA: Orexin an Wake-Kernen). Kombination in Zulassungsstudien nicht empfohlen. Im Verifikationsdesign: getrennte Nächte.

**Melatonin:** Keine relevante Interaktion. Verschiedene Angriffspunkte (MT1/MT2 am SCN vs. OX1/OX2 am lateralen Hypothalamus). Kombination unbedenklich.

### 9.5 Orexin $\rightarrow$ DRN: Der Upstream-Pfad

Orexin-Neurone projizieren direkt auf den DRN und aktivieren serotonerge Neurone über OX1R und OX2R. Im Wachzustand hält Orexin den DRN aktiv — Teil des normalen Wake-Promoting-Systems. Im Schlaf sinkt der Orexin-Output physiologisch, und der DRN verstummt.

In diesem System verstummt der DRN nicht stabil (5-HT1A-Autorezeptor-Instabilität). Ein DORA reduziert den exzitatorischen Orexin-Input auf den instabilen DRN im Schlaf. Dies ist keine direkte Raphe-Modulation (wie LDX über D2-Rezeptoren), sondern eine Reduktion des exzitatorischen Drives, der den DRN im Schlaf periodisch reaktiviert.

Die Implikation: Ein DORA adressiert nicht nur den Flip-Flop (Symptom: Gate-Instabilität), sondern partiell auch den DRN-Oszillator (Ursache: periodische 5-HT-Bursts), indem es den Orexin$\rightarrow$DRN-Pfad blockiert. Dies macht DORAs mechanistisch überlegen gegenüber reinen H1-Blockern (DPH/Doxepin), die den DRN-Input intakt lassen.

### 9.6 Verifikationsdesign

Ein DORA (Daridorexant 25 mg) ist der sauberste Test der Flip-Flop-Hypothese, weil es selektiv den Orexin-Arm adressiert — ohne Anticholinergika (DPH), ohne GABAerge Potenzierung (Benzo), ohne H1-Blockade (Doxepin).

**Design:** Vergleich von vier Nacht-Bedingungen am selben Endpunkt (Mayer-Nullphasen: Gesamtdauer, Schärfe der Transitionen, progressive Amplitudensteigerung):

| Bedingung | Mechanismus | Vorhersage |
|-----------|------------|------------|
| Unmediziert | Baseline | 0–15 min Null |
| Benzo | GABA am TRN $\rightarrow$ Gate-Schärfung | ~60 min Null (bestätigt) |
| DPH/Doxepin | H1-Blockade TMN $\rightarrow$ 1 Wake-Arm | Zu messen |
| DORA (Daridorexant) | OX1/OX2-Blockade $\rightarrow$ alle Wake-Arme + DRN-Input-Reduktion | Zu messen |

**Entscheidungsmatrix:**

- **DORA > Doxepin > Unmediziert:** Orexin ist der dominante Flip-Flop-Stabilisator. DORA als Langzeittherapeutikum vorzuziehen, insbesondere wegen des zusätzlichen Orexin$\rightarrow$DRN-Effekts.
- **DORA ≈ Doxepin > Unmediziert:** Wake-Seite ist der Flaschenhals, aber kein einzelner Arm dominant. Doxepin vorzuziehen (besseres Langzeitprofil, billiger, längere klinische Erfahrung).
- **DORA > Doxepin, aber beide << Benzo:** TRN-Switch ist der kritischere Hebel als Wake-Seiten-Input. GABAerge Intervention am Gate selbst ist effektiver als Input-Reduktion.
- **DORA ≈ Doxepin ≈ Unmediziert, nur Benzo wirkt:** Nur direkte TRN-Modulation reicht — alle Wake-Arm-Interventionen sind insuffizient. Problematisch für Langzeittherapie wegen Benzo-Toleranz.
- **Keine Substanz produziert >90 min Null:** Der DRN ist der Flaschenhals — er überwindet jede Wake-Seiten-Stabilisierung. Nur LDX (DRN-Stabilisierung) + Nachtmedikament (Wake-Seiten-Reduktion) gemeinsam können ausreichende Nullphasen produzieren.

### 9.7 Langzeitabwägung: DORA vs. Doxepin

**Doxepin 3 mg:** Jahrzehntelange Erfahrung, bei 3 mg rein H1-selektiv, keine anticholinerge Last, keine Toleranz, kein Rebound, generisch verfügbar, billig. Blockiert nur einen Wake-Arm (TMN-Histamin). Lässt den Orexin$\rightarrow$DRN-Pfad intakt.

**Daridorexant 25 mg:** Maximal 3 Jahre Langzeitdaten. Teurer. Blockiert alle Wake-Arme koordiniert und reduziert zusätzlich den exzitatorischen Orexin-Input auf den instabilen DRN. Keine Toleranz, kein Rebound, keine kognitive Beeinträchtigung in bisherigen Studien.

Die Entscheidung hängt vom Verifikationsergebnis ab. Wenn DORA signifikant mehr Nullphasen produziert als Doxepin, ist der Orexin$\rightarrow$DRN-Pfad klinisch relevant und DORA langfristig vorzuziehen. Wenn beide ähnlich wirken, ist Doxepin die konservativere Wahl bei gleichem Ergebnis.

Die optimale Langzeitkombination ist voraussichtlich: **LDX tagsüber** (Raphe-Stabilisierung am Oszillator) + **DORA oder Doxepin nachts** (Flip-Flop-Stabilisierung am Switch). Die Frage, welches Nachtmedikament den besseren Effekt auf die Nullphasen hat, nachdem LDX die Raphe-Grundaktivität bereits gedämpft hat, ist der eigentliche Langzeit-Comparator.

---

## 10. Offene Fragen und nächste Schritte

### 10.1 Empirisch zu klären

1. **DPH-Nacht (unmittelbar):** Nullphasen-Quantifizierung unter DPH. Vergleich mit Benzo-Nacht (62 min). Achten auf: Gesamtdauer, Schärfe der Transitionen, Erhalt der progressiven Amplitudensteigerung, und Effekt des DPH-Wirkverlusts im Late-Abschnitt.

2. **DORA-Testverordnung:** Daridorexant 25 mg über Hausarzt. Mindestens 3 Nächte für Baseline-Vergleich.

3. **LDX + Nachtmedikament:** Vergleich LDX+DORA vs. LDX+Doxepin als eigentlicher Langzeit-Comparator.

4. **Coospo-Validierung:** R-R-Intervall-basierte SDNN/RMSSD pro Minute als Echtzeit-Metrik für die Nullphasen. Validierung der Mayer-Band-Schwelle (<500) gegen Zeitdomänen-Kriterien.

5. **Schlafstaging-Overlay:** Xiaomi-Schlafstaging-Daten über Mayer-Zeitreihe legen. Korrelieren die Nullphasen mit als „Deep" klassifizierten Epochen?

### 10.2 Theoretisch zu klären

1. **Gain-Position relativ zur Bifurkationsschwelle:** Warum liegt der Baroreflex-Gain in diesem System so nahe an der Schwelle? Ist das eine Folge der thalamischen Fehlkalibrierung (Kap. 03), oder ein eigenständiger Defekt?

2. **ULF22 als ISO:** Falls der 22-min-Oszillator eine infraslow oscillation der thalamokortikalen Erregbarkeit ist — moduliert er den Flip-Flop-Zustand, die Baroreflex-Schwelle, oder beides?

3. **Orexin-Spiegel:** Gibt es Hinweise auf tonisch erhöhte Orexin-Aktivität in der Population A? Wenn ja, wäre ein DORA nicht nur Flip-Flop-Stabilisator, sondern korrigierende Therapie.

4. **CSD-Threshold im Kontext:** Wenn CSD den offenen thalamokortikalen Gate als Co-Faktor benötigt, dann wäre CSD im Tiefschlaf unmöglich — konsistent mit der klinischen Beobachtung, dass Migräneattacken typischerweise in REM oder beim Aufwachen beginnen, nicht in N3.

### 10.3 Modell-Revision

Eine formale Revision des Pathogenesemodells ist vorzeitig, bis die DORA-Verifikation Ergebnisse liefert. Die Kernelemente einer potentiellen Revision wären:

- **Kapitel 03 (Thalamische Kompensation):** Ergänzung um den thalamokortikalen Gate als aktiven autonomen Schalter, nicht nur als sensorischen Filter. Die Kompensationstiefe bestimmt nicht nur das kognitive Phänotyp-Spektrum, sondern auch die autonome Entkopplungsfähigkeit im Schlaf.

- **Kapitel 04/05 (Manifestation):** Interoceptive Inkohärenz als Gating-Insuffizienz im Wachzustand — dasselbe Mechanismus-Spektrum wie die Nullphasen im Schlaf, aber auf der subkritischen Seite.

- **Kapitel 08 (Zwei-Phasen-Protokoll):** DORA als dritte Substanzklasse neben DPH/Doxepin (Phase A) und LDX (Phase B). Verifikationsprotokoll als Anhang.

- **Neues Kapitel:** Autonomes Profil als diagnostisches Werkzeug — Mayer-Nullphasen als quantitativer Biomarker für Tiefschlafqualität, CIRC24-Einbruch als Prodrom-Marker, Flip-Flop-Stabilität als Therapie-Endpunkt.