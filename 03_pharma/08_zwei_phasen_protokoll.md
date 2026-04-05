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
| **Sekundär** | Transitionsdichte (Stadienwechsel/h) | Reduktion |
| **Sekundär** | Deep/REM-Ratio | Stabil (REM darf nicht einbrechen) |
| **Sicherheit** | REM-Episoden/Nacht | ≥ POST-Baseline |
| **Exploratorisch** | Autokorrelation Lag 4 | Abschwächung des Oszillationsmusters |

**Interpretation:** Wenn das IBI sich verlängert und gleichzeitig die Autokorrelation bei Lag 4 abschwächt, spricht das für eine echte Interferenzreduktion und nicht nur für eine sedierungsbedingte Schwellenanhebung. Wenn nur die Transitionsdichte sinkt bei gleichbleibendem IBI, dominiert der Sedierungseffekt — kein Evidenz für das Interferenzmodell.

---

## 5. Protokoll

### Phase A — Baseline-Vergleichsperiode (Woche 1)

- **25 mg DPH-HCl** abends, tägliche Tracker-Erfassung
- Vergleichsbasis: POST-Baseline (LDX-stabilisierte Werte ohne DPH)
- Monitoring: REM-Ratio, subjektive Schlafqualität, morgendliche Kohärenz

**Initiale Beobachtungen (Phase A, laufend):**
Erste Nächte zeigen eine Transitionsdichte deutlich unterhalb des POST-Means (2,4/h vs. POST 3,6/h, PRE 4,6/h), niedrigen HR-Einstieg und flachen HR-Verlauf über die Nacht. Das Hypnogramm erscheint subjektiv stabiler als unter LDX allein. Die Effektrichtung ist konsistent mit der Modellvorhersage (B7-Suppression → reduzierte Interferenz → verbesserte Schlafkonsolidierung). Die Effektstärke übersteigt den LDX-Durchschnitt, was bemerkenswert ist, da der Wirkmechanismus orthogonal angreift (H1→selektive B7-Suppression vs. DA→indirekte Raphe-Stabilisierung).

**Caveat:** Sehr frühe Daten, Placebo- und Neuheitseffekte nicht ausschließbar. Bewertung erst nach ≥2 vollständigen erwarteten Zyklen möglich.

### Phase B — Beobachtungsperiode (Woche 2–3)

- Falls tolerabel und REM intakt: Fortführung über **2–3 volle erwartete Zyklen** (~12–16 Tage)
- Fortlaufende Tracker-Erfassung aller definierten Endpunkte

### Auswertung

- Vergleich: Median IBI, Transitionsdichte, subjektive Anfallsschwere
- Statistische Einschränkung: n=1-Design erlaubt keine Inferenzstatistik; Effektgrößen werden deskriptiv gegen die intraindividuelle Varianz der POST-Baseline eingeordnet

---

## 6. Evidenzstatus

| Aussage | Evidenzniveau |
|---|---|
| H1-Blockade supprimiert selektiv DRN-5-HT | Gesichert (Crawford et al. 2013) |
| DPH passiert Blut-Hirn-Schranke | Gesichert |
| B7-Amplitudenreduktion senkt Interferenzprodukt | Hypothetisch, mechanistisch ableitbar; initiale Tracker-Daten richtungskonsistent |
| Zwei-Phasen-Design komplementär | Hypothetisch; initiale Beobachtungen zeigen Effekte jenseits LDX-Baseline |
| Gesamtprotokoll | Spekulativ, n=1-Experiment; Phase A aktiv, erste Daten richtungskonsistent |

---

## 7. Langzeitperspektive: Diphenhydramin vs. Doxepin

### 7.1 Diphenhydramin ist kein Langzeitkandidat

Diphenhydramin-HCl eignet sich als Proof-of-Concept, nicht als Dauertherapie. Zwei Limitationen sind disqualifizierend:

1. **Anticholinerge Last.** Diphenhydramin ist stark anticholinerg. Epidemiologische Daten (Gray et al. 2015, Indiana-Kohorte) zeigen dosisabhängig erhöhtes Demenzrisiko bei kumulativer Exposition. Die anticholinerge Begleitwirkung ist bei OTC-Dosen klinisch relevant und bei chronischem Einsatz nicht akzeptabel.

2. **H1-Toleranz.** H1-Rezeptor-Upregulation unter chronischer Blockade ist gut dokumentiert. Die Zeitkonstante bei Schlafmitteln liegt typischerweise im Bereich von Tagen bis wenigen Wochen. Die DRN-selektive Suppression würde abschwächen.

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

**Offene Frage:** Die DRN-Selektivität der H1-Blockade (Crawford et al. 2013) wurde unter akuter Gabe gezeigt. Ob die differentielle H1-Rezeptordichte am DRN vs. MRN unter chronischer Blockade erhalten bleibt, ist nicht untersucht. Falls die H1-Upregulation am DRN stärker ausfällt als am MRN, könnte die Selektivität unter Langzeitgabe paradoxerweise zunehmen — oder sich nivellieren.

### 7.3 Konsequenz für das Protokoll

Falls Phase A und B eine stabile Interferenzreduktion unter DPH bestätigen, ist der nächste Schritt der Wechsel auf Doxepin 3 mg als langzeitfähige Umsetzung desselben Mechanismus. Das DPH-Experiment validiert den Pathway; Doxepin wäre das klinisch vertretbare Vehikel für die chronische Anwendung.

---

> **Disclaimer:** Dieses Protokoll ist ein theoretisches Konstrukt im Rahmen eines individuellen Arbeitshypothesen-Archivs. Es handelt sich nicht um eine klinische Empfehlung. Die mechanistische Begründung ist plausibel, aber nicht validiert. Jede Umsetzung erfolgt als n=1-Selbstexperiment unter eigener Verantwortung und sollte idealerweise ärztlich begleitet werden.
