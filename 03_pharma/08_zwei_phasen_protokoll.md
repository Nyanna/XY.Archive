# Therapeutisches Zwei-Phasen-Protokoll
### LDX (Tag) + Diphenhydramin-HCl (Nacht)

> **Status:** Phase A aktiv — n=1-Experiment, nicht klinisch validiert. Initiale Beobachtungen richtungskonsistent mit der Modellvorhersage.  
> Grundlage: B7/B8-Interferenzmodell (Pathogenetisches Modell, Anhang F), differentielle afferente Regulation DRN vs. MRN (Anhang D.8).  
> Ziel: Experimentelle Überprüfung der Amplitudenmodulations-Hypothese.

---

## 1. Mechanistische Begründung

### 1.1 Was LDX adressiert

LDX stabilisiert den **Intra-Kern-Takt** über D2-Stabilisierung, kompensiert zirkadiane Drift in der SCN↔B8-Schleife, stützt PFC-Funktion dopaminerg und verbessert interozeptive Kohärenz (vgl. Titrationsleitlinie, Abschnitt 1.1).

### 1.2 Was LDX nicht adressiert

LDX hat keinen direkten Zugriff auf den **Inter-Kern-Phasenversatz** zwischen B7 (DRN) und B8 (MRN). Ebenso bleibt der ~4-Tage-CSD-Oszillator durch dopaminerge Intervention unberührt. LDX moduliert die Amplitude beider Raphe-Kerne nicht differentiell — es fehlt ein Hebel an der Interferenzquelle.

### 1.3 Diphenhydramin-HCl als selektiver B7-Suppressor

Diphenhydramin-HCl ist ein zentral gängiger H1-Antagonist. Histaminerge Afferenzen aus dem TMN (Tuberomammillärkern) innervieren den DRN (B7) dichter als den MRN (B8). H1-Blockade supprimiert daher **selektiv die B7-Aktivität**, ohne B8 substantiell zu beeinflussen (Crawford et al. 2013, vgl. Anhang D.8).

### 1.4 Interferenzprodukt und Amplitudenlogik

Die Interferenzstärke zwischen B7 und B8 ist proportional zum Produkt:

**Interferenz ∝ Amplitude_B7 × Amplitude_B8 × cos(Phasenversatz)**

Wenn der Phasenversatz pharmakologisch nicht direkt korrigierbar ist, bleibt die Amplitudenreduktion einer der beiden Kerne als Stellgröße. B7-Amplitudenreduktion über H1-Blockade senkt das Interferenzprodukt **unabhängig von der aktuellen Phasenrichtung**.

### 1.5 Komplementäres Zwei-Achsen-Design

LDX kompensiert exakt das, was DPH kostet: Die B7-Reduktion senkt serotonergen PFC-Input — LDX stützt die PFC-Funktion dopaminerg. DPH adressiert, was LDX nicht kann: die Inter-Kern-Interferenz. Beide Interventionen greifen an orthogonalen Achsen an.

---

## 2. Verbindungswahl

Die Wahl der Diphenhydramin-Verbindung ist nicht trivial. Begleitsubstanzen können das dopaminerge System perturbieren und die LDX-Titration konfundieren.

| Verbindung | Wirkstoff | Bewertung |
|---|---|---|
| **Diphenhydramin-HCl** | Rein | ✓ Empfohlen — keine aktiven Begleitsubstanzen, beste Dosiskontrolle |
| **Diphenhydramin-Citrat** | Rein, anderes Salz | ✗ Niedrigere molare Wirkstoffdichte, kein Vorteil |
| **Dimenhydrinat** | DPH + 8-Chlorotheophyllin | ✗ Kontraindiziert — Xanthinderivat (Adenosin-Antagonist) konfundiert D2High-Shift, unkontrollierter dopaminerger Perturbator |

**Begründung der Dimenhydrinat-Kontraindikation:** 8-Chlorotheophyllin ist ein Adenosin-Rezeptor-Antagonist. Adenosin-Antagonismus verschiebt das D2-Gleichgewicht in Richtung D2High und erzeugt einen unkontrollierten dopaminergen Push — exakt das Gegenteil der kontrollierten Titration, die LDX liefern soll (vgl. Titrationsleitlinie, Abschnitt 1.4 zur Koffein-Kohärenz-Dissoziation).

---

## 3. Dosislogik

### 3.1 Startdosis

**25 mg Diphenhydramin-HCl** abends, circa 60 Minuten vor geplantem Schlafbeginn.

### 3.2 Rationale

Ziel ist B7-Suppression ohne Vollsedierung. Die Dosis soll den histaminergen DRN-Input reduzieren, nicht das gesamte Arousal-System abschalten. 25 mg liegt am unteren Ende der OTC-Schlafhilfe-Dosierung und dürfte ausreichen, um die H1-vermittelte DRN-Fazilitierung signifikant zu dämpfen.

### 3.3 REM als Dosislimit

Diphenhydramin ist nicht nur ein H1-Antagonist, sondern auch anticholinerg. Acetylcholin ist essenziell für die REM-Generierung (pedunkulopontine und laterodorsale tegmentale Kerne). Zu hohe Dosen supprimieren REM.

**Operationalisierung:** Die REM-Ratio im Schlaftracker dient als Sicherheitsmetrik.

- Bei **intakter REM-Ratio** (stabil relativ zur POST-Baseline): Dosis fortsetzen.
- Bei **REM-Einbruch** (absolute oder relative Reduktion gegenüber POST-Baseline): Dosis ist zu hoch — Reduktion oder Absetzung.

---

## 4. Tracker-Endpunkte

| Endpunkt | Metrik | Erwartung |
|---|---|---|
| **Primär** | Median Inter-Anfall-Intervall (IBI) | Verlängerung (>4.0 d) |
| **Primär** | Transitionsdichte ON vs. OFF-Blöcke | Signifikante Trennung |
| **Sekundär** | Transitionsdichte (Stadienwechsel/h) | Reduktion (gesamt) |
| **Sekundär** | Deep/REM-Ratio | Stabil (REM darf nicht einbrechen) |
| **Sicherheit** | REM-Episoden/Nacht | ≥ POST-Baseline |
| **Diskriminanz** | IBI-Verlängerung relativ zum ON-Anteil | Überproportional = Interferenz; proportional = Sedierung |
| **Diskriminanz** | Carry-over: Transitionsdichte OFF-Nacht 1 vs. OFF-Nacht 3–5 | Gradient = partieller Carry-over |
| **Exploratorisch** | Autokorrelation Lag 4 | Abschwächung des Oszillationsmusters |

**Interpretation:** Das alternierende Design erlaubt eine Dreifach-Diskriminierung: (1) Wenn das IBI sich verlängert und gleichzeitig die Autokorrelation bei Lag 4 abschwächt, spricht das für echte Interferenzreduktion. (2) Wenn nur die ON-Nächte besser aussehen bei gleichbleibendem IBI und Oszillator, dominiert der Sedierungseffekt. (3) Wenn ON-Nächte besser sind und ein Carry-over in frühe OFF-Nächte sichtbar ist, liegt ein partieller Interferenzeffekt mit abklingender Zeitkonstante vor.

---

## 5. Protokoll

### Phase A — Baseline-Vergleichsperiode (Woche 1)

- **25 mg DPH-HCl** abends, tägliche Tracker-Erfassung
- Vergleichsbasis: POST-Baseline (LDX-stabilisierte Werte ohne DPH)
- Monitoring: REM-Ratio, subjektive Schlafqualität, morgendliche Kohärenz

**Initiale Beobachtungen (Phase A, laufend):**
Erste Nächte zeigen eine Transitionsdichte deutlich unterhalb des POST-Means (2,4/h vs. POST 3,6/h, PRE 4,6/h), niedrigen HR-Einstieg und flachen HR-Verlauf über die Nacht. Das Hypnogramm erscheint subjektiv stabiler als unter LDX allein. Die Effektrichtung ist konsistent mit der Modellvorhersage (B7-Suppression → reduzierte Interferenz → verbesserte Schlafkonsolidierung). Die Effektstärke übersteigt den LDX-Durchschnitt, was bemerkenswert ist, da der Wirkmechanismus orthogonal angreift (H1→selektive B7-Suppression vs. DA→indirekte Raphe-Stabilisierung).

**Caveat:** Sehr frühe Daten, Placebo- und Neuheitseffekte nicht ausschließbar. Bewertung erst nach ≥2 vollständigen erwarteten Zyklen möglich.

### Phase B — Alternierendes ON/OFF-Design (ab Woche 2)

Statt kontinuierlicher DPH-Gabe: **3 Nächte ON / 3–5 Nächte OFF**, wiederholt über 6–8 Wochen.

**Rationale:**

1. **Toleranzvermeidung.** DPH-Halbwertszeit ~4–8h, nach 24h vollständig ausgewaschen. 3–5 Tage OFF reichen für H1-Rezeptor-Renormalisierung. Die DRN-Selektivität bleibt über die gesamte Beobachtungsperiode erhalten.
2. **Anticholinerge Kumulation entfällt.** Das kumulative Demenzrisiko (Gray et al. 2015) skaliert mit Gesamtexposition. Intermittierende Gabe (~3 von 8 Nächten) reduziert die Gesamtexposition auf unter 40%.
3. **Within-subject ON/OFF-Vergleich.** Repeated-measures innerhalb derselben Person unter identischen Kontextbedingungen (LDX, Schlafumgebung, Tagesrhythmus). Über 6–8 Wochen entstehen 6+ ON/OFF-Zyklen — genug für deskriptive Verteilungstrennung.

**Ablauf:**

| Block | Nächte | DPH | Monitoring |
|---|---|---|---|
| ON | 3 konsekutiv | 25 mg DPH-HCl abends | Transitionsdichte, HR-Profil, REM-Ratio |
| OFF | 3–5 konsekutiv | Kein DPH | Identische Tracker-Erfassung |
| *Wiederholen* | *6–8 Wochen* | | |

Die OFF-Länge (3–5 Nächte) kann an den individuellen Zyklusverlauf angepasst werden, sollte aber innerhalb der Beobachtungsperiode konsistent gehalten werden.

### Phase B — Diskriminanztest: Sedierung vs. Interferenz

Das alternierende Design ermöglicht eine Schlüsselunterscheidung, die bei Dauereinnahme nicht möglich wäre:

| Beobachtung | Interpretation |
|---|---|
| Transitionsdichte sinkt **nur in ON-Nächten**, Oszillator und IBI unverändert | **Sedierungseffekt** — DPH verbessert lokale Schlafqualität, ohne die Upstream-Interferenz zu adressieren |
| IBI verlängert sich **überproportional** zum ON-Anteil, Oszillator-Amplitude gedämpft | **Interferenzreduktion** — B7-Suppression während ansteigender Phase verschiebt CSD-Schwelle für den gesamten Zyklus |
| Transitionsdichte sinkt in ON-Nächten **und Carry-over in erste OFF-Nächte** | **Gemischter Effekt** — partielle Interferenzreduktion mit abklingendem Profil |

Der zweite Fall wäre die stärkste Bestätigung des Interferenzmodells: Wenn 3 DPH-Nächte den IBI-Effekt über den gesamten ~8-Tage-Zyklus verschieben, ist der Mechanismus nicht Sedierung (die mit der Pharmakokinetik ausgewaschen wäre), sondern tatsächlich Amplitudenmodulation am Interferenz-Produkt.

### Auswertung

**Primäre Analyse:**
- Vergleich Transitionsdichte ON vs. OFF-Blöcke (Median, IQR)
- IBI-Verlängerung relativ zum ON/OFF-Anteil (Proportionalitätstest)
- Carry-over-Analyse: Transitionsdichte OFF-Nacht 1 vs. OFF-Nacht 3–5

**Sekundäre Analyse:**
- Vergleich: Median IBI, Transitionsdichte, subjektive Anfallsschwere gegen POST-Baseline
- Autokorrelation Lag 4 der Nacht-zu-Nacht-Density: Abschwächung als Interferenzreduktions-Marker

- Statistische Einschränkung: n=1-Design erlaubt keine Inferenzstatistik; Effektgrößen werden deskriptiv gegen die intraindividuelle Varianz der POST-Baseline eingeordnet

---

## 6. Evidenzstatus

| Aussage | Evidenzniveau |
|---|---|
| H1-Blockade supprimiert selektiv DRN-5-HT | Gesichert (Crawford et al. 2013) |
| DPH passiert Blut-Hirn-Schranke | Gesichert |
| B7-Amplitudenreduktion senkt Interferenzprodukt | Hypothetisch, mechanistisch ableitbar; initiale Tracker-Daten richtungskonsistent |
| Zwei-Phasen-Design komplementär | Hypothetisch; initiale Beobachtungen zeigen Effekte jenseits LDX-Baseline |
| Alternierendes ON/OFF diskriminiert Sedierung von Interferenz | Methodisch begründet, nicht getestet |
| Doxepin 3 mg als langzeitfähige H1-Alternative | Pharmakologisch plausibel, DRN-Selektivität unter Chronizität nicht untersucht |
| Gesamtprotokoll | Spekulativ, n=1-Experiment; Phase A aktiv, erste Daten richtungskonsistent |

---

## 7. Langzeitperspektive: Diphenhydramin vs. Doxepin

### 7.1 Diphenhydramin ist kein Langzeitkandidat

Diphenhydramin-HCl eignet sich als Proof-of-Concept, nicht als Dauertherapie. Zwei Limitationen sind disqualifizierend:

1. **Anticholinerge Last.** Diphenhydramin ist stark anticholinerg. Epidemiologische Daten (Gray et al. 2015, Indiana-Kohorte) zeigen dosisabhängig erhöhtes Demenzrisiko bei kumulativer Exposition. Die anticholinerge Begleitwirkung ist bei OTC-Dosen klinisch relevant und bei chronischem Einsatz nicht akzeptabel.

2. **H1-Toleranz.** H1-Rezeptor-Upregulation unter chronischer Blockade ist gut dokumentiert. Die Zeitkonstante bei Schlafmitteln liegt typischerweise im Bereich von Tagen bis wenigen Wochen. Die DRN-selektive Suppression würde abschwächen.

3. **NTS-Tonuspfad-Entzug (akut).** DPH suppressiert B7 via H1-Blockade (Crawford et al. 2013). Dies entzieht dem NTS den serotonergen 5-HT2A-Input, der die tonische RVLM-Hemmung steuert (Sévoz-Couche et al. 2004/2006). Konsequenz: Verlust der neuralen sympathischen Grundsteuerung am Folgetag. Empirisch bestätigt am 29.04.2026 — Spitzenwert-Nullphase bei gleichzeitigem Totalausfall der sympathischen Morgenumschaltung (Dominanz -0.43 bis -0.66 über den gesamten Tag, RMSSD 12–19ms, ULF2 bis 4597 als HPA-Kompensation). Dieser Effekt tritt bei jeder Einzeldosis auf, nicht erst bei chronischer Anwendung, und erzeugt ein NTS-Tonusinsuffizienz (adrenale HR-Kompensation, Flushing, Erschöpfung bei erhaltener Kognition; keine orthostatische Tachykardie). Siehe Pathogenesemodell §5.7.

### 7.2 Niedrigdosiertes Doxepin als chronisch einsetzbare Alternative

**Doxepin 3 mg** (Silenor) ist FDA-zugelassen für Kurz- und Langzeit-Insomnie und funktioniert in diesem Dosisbereich als nahezu reiner H1-Antagonist:

| Eigenschaft | Diphenhydramin 25 mg | Doxepin 3 mg |
|---|---|---|
| H1-Selektivität | Mäßig | Hoch (bei ≤6 mg) |
| Anticholinerge Last | Hoch | Nicht nachweisbar (placebovergleichbar) |
| Gedächtnisbeeinträchtigung | Möglich | Nicht nachweisbar |
| Rebound bei Absetzen | Möglich | Nicht berichtet |
| Studiendauer | — | Bis 3 Monate (3 mg) |
| Toleranzentwicklung | Tage–Wochen | Nicht systematisch untersucht |
| NTS-5-HT2A-Entzug | Vollständig (kein SERT-Effekt) | Partiell kompensiert (SERT-Blockade hält 5-HT im Spalt) |

**NTS-Kompensation via SERT:** Doxepin besitzt SERT-Affinität (Ki ~68nM), DPH nicht. Bei H1-vermittelter B7-Suppression reduziert sich der Raphe-Output zum NTS. DPH: weniger Output + normale Clearance = doppelter Verlust am 5-HT2A. Doxepin: weniger Output + verlangsamte synaptische Clearance = partielle Kompensation. Bei 3mg Doxepin (Silenor-Bereich) dominiert H1 (Ki ~0.24nM) stark über SERT; ob die SERT-Besetzung für eine funktional relevante NTS-Kompensation ausreicht, ist nicht gesichert. Bei 10–25mg wäre die SERT-Komponente stärker, aber anticholinerge Effekte steigen. Die optimale Dosis liegt möglicherweise bei 3–6mg — maximale H1-Selektivität bei gerade ausreichender SERT-Kompensation.

**Offene Frage:** Die DRN-Selektivität der H1-Blockade (Crawford et al. 2013) wurde unter akuter Gabe gezeigt. Ob die differentielle H1-Rezeptordichte am DRN vs. MRN unter chronischer Blockade erhalten bleibt, ist nicht untersucht. Falls die H1-Upregulation am DRN stärker ausfällt als am MRN, könnte die Selektivität unter Langzeitgabe paradoxerweise zunehmen — oder sich nivellieren.

### 7.3 Konsequenz für das Protokoll

Falls das alternierende ON/OFF-Design eine stabile Interferenzreduktion bestätigt — insbesondere den überproportionalen IBI-Effekt (Abschnitt 5, Diskriminanztest) — ist der nächste Schritt der Wechsel auf Doxepin 3 mg. Das DPH-Experiment validiert den Pathway; Doxepin wäre das klinisch vertretbare Vehikel für die chronische Anwendung.

Das alternierende Design hat den zusätzlichen Vorteil, dass es die Toleranzfrage vorab klärt: Wenn der DPH-Effekt über 6–8 Wochen ON/OFF stabil bleibt, spricht das für erhaltene H1-Sensitivität bei intermittierender Gabe — und liefert gleichzeitig eine Entscheidungsgrundlage, ob die chronische Variante (Doxepin) überhaupt intermittierend dosiert werden muss oder ob die niedrigere anticholinerge Last eine Dauergabe rechtfertigt.

---

## 8. CYP2D6-Konfundierung der DPH-Daten

### 8.1 Befund

Die HR-Plateau-Analyse zeigt unter DPH-Nächten eine veränderte Plateau-Signatur: gleichmäßigere Level-Abstände (spacing_cv ↓, z=−1.41), steileren nadir_slope und stabilere Hierarchie. Diese Effekte wurden initial als H1-vermittelte B7-Suppression interpretiert.

Eine pharmakokinetische Analyse deckt einen Confounder auf: **DPH ist ein CYP2D6-Inhibitor.** CYP2D6-vermittelte Hydroxylierung ist der Hauptabbauweg von d-Amphetamin (dem aktiven Metaboliten von LDX). Die abendliche DPH-Einnahme verlangsamt die d-Amphetamin-Elimination und verlängert damit den LDX-Effekt pharmakologisch in die Nacht.

### 8.2 Implikation

Die DPH-Nacht-Signatur hat zwei nicht trennbare Ursachen:

1. **H1-Mechanismus (Intertakt):** DPH suppressiert B7 über H1-Blockade → reduzierte B7/B8-Interferenz → sauberere Plateau-Architektur
2. **CYP2D6-Mechanismus (Intratakt):** DPH verlängert d-AMP-Exposition → D2-Stabilisierung hält über die Nacht → Intratakt-Kompensation stabilisiert die Architektur downstream

Im D2High-Kontext (1–2 mg LDX klinisch wirksam) könnte bereits eine minimale Spiegelverlängerung funktional sein. Die DPH-Daten belegen damit den Pathway, erlauben aber keine Zuordnung zum Wirkmechanismus.

### 8.3 Konsequenz

Die Konfundierung macht eine Dreifach-Diskrimination notwendig, bevor die kombinierte Nacht-Einnahme evaluiert werden kann (→ Abschnitt 9).

---

## 9. Dreifach-Diskriminationsprotokoll

### 9.1 Design

Drei sequentielle Experimente isolieren die Wirkmechanismen:

| Experiment | D2-Nacht | H1-Blockade | CYP2D6-Konfund | Isoliert |
|---|---|---|---|---|
| DPH 25 mg (gelaufen) | Indirekt via CYP2D6 | Ja | Ja | Nichts sauber |
| **LDX Nacht-Mikrodosis** | **Direkt** | **Nein** | **Nein** | **Intratakt** |
| **Doxepin 3 mg** | **Nein** | **Ja** | **Nein** | **Intertakt** |

Doxepin 3 mg erzeugt **keine CYP2D6-Hemmung** bei therapeutischen Konzentrationen (Silenor-Fachinformation: Plasmaspiegel ~0.9 ng/mL bei 6 mg, keine CYP-Inhibition nachweisbar). Die CYP2D6-Interaktion mit LDX entfällt vollständig. Gleichzeitig wird Doxepin selbst über CYP2D6 metabolisiert, aber LDX zeigt keine klinisch relevante CYP2D6-Hemmung — die Interaktion ist in beiden Richtungen neutral.

### 9.2 Experiment 1: LDX Nacht-Mikrodosis (isoliert Intratakt)

**Rationale:** LDX-Mikrodosis (1–2 mg) abends testet, ob die D2-Stabilisierung allein — ohne H1-Blockade — die Plateau-Signatur erzeugt. Im D2High-Kontext liegt die wirksame Dosis unter der Arousal-Schwelle; Schlafstörung ist nicht zu erwarten.

**Durchführung:**

| Parameter | Wert |
|---|---|
| Substanz | LDX (Elvanse), Kapselinhalt gewichtsdosiert |
| Dosis | 1–2 mg, identisch zur etablierten Tagesdosis-Untergrenze |
| Zeitpunkt | 60–90 min vor Schlafbeginn |
| Dauer | 4–6 konsekutive Nächte |
| Monitoring | HR-Plateau-Analyse, Einschlaflatenz, Tracker-Hypnogramm |
| Abbruchkriterium | Einschlaflatenz >45 min oder subjektive Schlafstörung an 2+ Nächten |

**Erwartete Ergebnisse:**

| Beobachtung | Interpretation |
|---|---|
| Plateau-Signatur tritt auf (spacing_cv ↓, nadir_slope ↓) | D2-Effekt ist der Träger → Intratakt-Kompensation wirkt über die Nacht |
| Keine Signatur, keine Schlafstörung | D2-Dosis ist zu niedrig oder der Effekt braucht H1-Achse |
| Keine Signatur, Schlafstörung | Dosis überschreitet Arousal-Schwelle → Dosisreduktion |

**Sicherheit:** Die LDX-Mikrodosis liegt bei ~2–3% der therapeutischen Standarddosis. Die Prodrug-Konversion über RBC-Peptidasen ist nicht CYP-abhängig; keine Interaktion mit laufender Morgen-LDX-Dosis. Die d-Amphetamin-Halbwertszeit (9–13h) bedeutet, dass bei morgendlicher Einnahme (z.B. 8:00) und abendlicher Mikrodosis (z.B. 22:00) die Spiegel sich nicht klinisch relevant addieren. Urin-pH beeinflusst die Elimination — konsistente Ernährung und Hydration halten diesen Faktor konstant.

### 9.3 Experiment 2: Doxepin 3 mg (isoliert Intertakt)

**Rationale:** Doxepin 3 mg testet die reine H1-vermittelte B7-Suppression ohne CYP2D6-Konfundierung. Im Vergleich zu DPH bietet Doxepin:

- Keine CYP2D6-Hemmung → kein LDX-Carry-over
- Keine anticholinerge Last bei 3 mg → keine REM-Suppression
- Längere Halbwertszeit (t½ ~15h, Nordoxepin ~31h) → stabile Nacht-Abdeckung ohne Late-Night-Wirkverlust

**Durchführung:**

| Parameter | Wert |
|---|---|
| Substanz | Doxepin 3 mg (Silenor-Äquivalent) |
| Zeitpunkt | 30 min vor Schlafbeginn, nicht innerhalb von 3h nach Mahlzeit |
| Dauer | 5–7 konsekutive Nächte |
| Monitoring | HR-Plateau-Analyse, REM-Ratio, Transitionsdichte |

**Erwartete Ergebnisse:**

| Beobachtung | Interpretation |
|---|---|
| Plateau-Signatur wie unter DPH | H1-Mechanismus bestätigt → Intertakt-Effekt real |
| Schwächere Signatur als DPH | H1-Effekt real, aber DPH-CYP2D6-Carry-over trug bei |
| Keine Signatur | DPH-Effekt war primär CYP2D6-vermittelt → H1-Achse unzureichend |

**Pharmakokinetische Besonderheit:** Der aktive Metabolit Nordoxepin (t½ ~31h) akkumuliert bei täglicher Gabe. Steady-State wird nach ~5 Tagen erreicht. Die erste Nacht ist daher nicht direkt mit DPH-Nacht-1 vergleichbar; die Bewertung sollte auf Nacht 3–7 fokussieren.

### 9.4 Interpretationsmatrix

| LDX-Nacht | Doxepin | Schlussfolgerung | Konsequenz |
|---|---|---|---|
| Signatur ✓ | Signatur ✓ | Beide Achsen wirksam, orthogonal | Kombinierte Gabe maximal wirksam |
| Signatur ✓ | Signatur ✗ | Intratakt dominiert | LDX-Nacht allein ausreichend |
| Signatur ✗ | Signatur ✓ | Intertakt dominiert | Doxepin allein ausreichend |
| Signatur ✗ | Signatur ✗ | DPH-Effekt war CYP2D6-Artefakt | Gesamtansatz überdenken |

---

## 10. Kombinierte Nacht-Einnahme: LDX-Mikrodosis + Doxepin 3 mg

### 10.1 Rationale

Wenn beide Einzelexperimente (9.2, 9.3) jeweils einen Teil der Plateau-Signatur erzeugen, adressiert die Kombination beide Achsen gleichzeitig:

- **LDX-Mikrodosis:** D2-Stabilisierung → Intratakt-Kompensation
- **Doxepin 3 mg:** H1-Blockade → B7-Amplitudenreduktion → Intertakt-Interferenzreduktion

Das entspricht dem ursprünglichen Zwei-Achsen-Design (Abschnitt 1.5), aber mit sauberer Pharmakologie: keine CYP2D6-Konfundierung, keine anticholinerge Last, keine Toleranzentwicklung bei Niedrigdosis-Doxepin.

### 10.2 Interaktionsprofil LDX + Doxepin 3 mg

| Parameter | Bewertung |
|---|---|
| CYP2D6 | Doxepin 3 mg: keine Inhibition. LDX: keine klinisch relevante Inhibition. Neutral in beide Richtungen. |
| Serotonin-Syndrom | Doxepin 3 mg: keine relevante 5-HT-Reuptake-Hemmung. LDX-Mikrodosis: minimale monoaminerge Wirkung. Risiko nicht über Baseline. |
| NE-Reuptake | Doxepin 3 mg: nicht nachweisbar (erst ab ~25 mg relevant). Keine Potenzierung der sympathomimetischen LDX-Wirkung. |
| Anticholinerg | Doxepin 3 mg: placebovergleichbar. Keine REM-Suppression. |
| QTc-Verlängerung | Doxepin 3 mg: nicht berichtet. LDX: nicht berichtet. Kein additives Risiko. |
| Sedierung | Doxepin: sedierend (H1). LDX-Mikrodosis: unter Arousal-Schwelle. Kein Antagonismus erwartet. |

**Formale Warnkategorie:** Medscape listet TCA + Amphetamin als "Avoid or Use Alternate Drug". Diese Klassifikation ist dosisblind und bezieht sich auf antidepressive TCA-Dosen (75–300 mg), bei denen NE-Reuptake-Hemmung die sympathomimetische Amphetamin-Wirkung potenziert. Bei Doxepin 3 mg (Silenor-Dosierung) ist die NE-Reuptake-Hemmung pharmakologisch nicht nachweisbar — die Warnung ist für diese Kombination nicht valide, muss aber bei ärztlicher Kommunikation transparent gemacht werden.

### 10.3 Durchführung

| Parameter | Wert |
|---|---|
| Substanzen | LDX 1–2 mg + Doxepin 3 mg |
| Zeitpunkt | Gemeinsam 30–60 min vor Schlafbeginn |
| Voraussetzung | Beide Einzelexperimente (9.2, 9.3) abgeschlossen |
| Dauer | 7–10 konsekutive Nächte |
| Monitoring | HR-Plateau-Analyse, Transitionsdichte, IBI |

**Bewertung:** Vergleich der Plateau-Signatur gegen die drei Referenzen:

| Referenz | Erwartung bei Additivität |
|---|---|
| POST-Baseline (LDX Tag, kein Nacht-Supplement) | Signatur stärker |
| LDX-Nacht allein (Experiment 9.2) | Signatur stärker oder gleich |
| Doxepin allein (Experiment 9.3) | Signatur stärker oder gleich |

Überadditivität (Signatur stärker als Summe der Einzeleffekte) wäre ein Hinweis auf synergistische Mechanismen. Subadditivität (schwächer als erwartet) könnte auf kompetitive Interaktion auf Ebene der Raphe-Modulation hindeuten.

### 10.4 Pharmakokinetische Überlegungen

**LDX-Mikrodosis bei abendlicher Einnahme:** Die Prodrug-Konversion (RBC-Peptidasen, t½ < 1h) ist CYP-unabhängig. d-Amphetamin erreicht t_max nach ~3.5h, also um ~01:30 bei Einnahme um 22:00. Die d-Amphetamin-Elimination (t½ 9–13h) ist bei Doxepin 3 mg nicht verlängert (keine CYP2D6-Hemmung). Verbleibende d-AMP-Konzentration am Morgen: ~50% der Nacht-Mikrodosis + Rest der Morgen-Standarddosis.

**Doxepin-Akkumulation:** Nordoxepin (t½ ~31h) akkumuliert bei täglicher Gabe. Steady-State nach ~5 Tagen. Die H1-Blockade wird mit jeder Nacht stärker bis zum Plateau. Bewertung der Kombination sollte auf Nacht 5–10 fokussieren.

**Morgen-LDX-Interaktion:** Die morgendliche LDX-Standarddosis wird durch die nächtliche Mikrodosis nicht klinisch relevant beeinflusst. Bei 1–2 mg Nacht + z.B. 30 mg Morgen ist der Nacht-Anteil <7% der Gesamtexposition. Doxepin 3 mg hat keinen Einfluss auf die LDX-Kinetik.

---

## 11. Evidenzstatus (aktualisiert)

| Aussage | Evidenzniveau |
|---|---|
| H1-Blockade supprimiert selektiv DRN-5-HT | Gesichert (Crawford et al. 2013) |
| DPH passiert Blut-Hirn-Schranke | Gesichert |
| DPH hemmt CYP2D6 | Gesichert |
| CYP2D6 ist Hauptabbauweg von d-Amphetamin | Gesichert |
| DPH-Nacht-Signatur ist CYP2D6-konfundiert | Mechanistisch zwingend, Effektgröße unbekannt |
| Doxepin 3 mg hemmt CYP2D6 nicht | Gesichert (Silenor-Fachinformation) |
| Doxepin 3 mg hat keine anticholinerge Wirkung | Gesichert (placebovergleichbar in RCTs) |
| LDX-Mikrodosis unter Arousal-Schwelle | Einzelfallbeobachtung (D2High-Kontext), nicht generalisierbar |
| Dreifach-Diskrimination trennt Intra-/Intertakt | Methodisch begründet, nicht getestet |
| Kombinierte Nacht-Einnahme LDX + Doxepin 3 mg sicher | Pharmakologisch plausibel bei Mikrodosierung, keine klinischen Daten |
| Gesamtprotokoll | Spekulativ, n=1-Experiment |

> **Disclaimer:** Dieses Protokoll ist ein theoretisches Konstrukt im Rahmen eines individuellen Arbeitshypothesen-Archivs. Es handelt sich nicht um eine klinische Empfehlung. Die mechanistische Begründung ist plausibel, aber nicht validiert. Jede Umsetzung erfolgt als n=1-Selbstexperiment unter eigener Verantwortung und sollte idealerweise ärztlich begleitet werden.