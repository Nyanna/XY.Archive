
---

## **Anhang B: Tracker-Datenanalyse — Kortikale Desynchronisation**

### **B.0 Zusammenfassung und Revision**

Dieser Anhang ersetzt die frühere Fassung (Anhang B v1: „SWS-Phasenlage als Marker für Raphe-Dysregulation"). Die ursprüngliche Interpretation — SWS-Quantum erhalten, Phasenlage in ungünstige Druckgradienten verschoben — wird durch die hier dokumentierte Reanalyse der Tracker-Rohdaten revidiert.

**Revidierte Kernthese:** Das Defizit liegt nicht in der zeitlichen Lage des SWS, sondern in seiner räumlichen Kohärenz. Der Kortex erreicht keinen globalen SWS-Zustand, sondern zeigt ein topologisch fragmentiertes Patchwork aus lokalen Off-States. Der Tracker-Output — eine 1D-Projektion eines räumlich inhomogenen Prozesses — kodiert diese Fragmentierung als temporale Instabilität: häufige Stadienwechsel, kurze Deep-Fragmente und hohe Nacht-zu-Nacht-Variabilität.

**Konsequenzen für das Modell:**

- Kapitel 2.5.5 (Schlafarchitektur als zirkadianer Marker): Mechanismus revidieren — nicht verzögerte Entladung, sondern fehlende globale Synchronisation.
- Kapitel 4.3 (Nap-Kaskade): Die Nap-Kaskade beschreibt denselben Mechanismus (patchy Off-States) unter Wachbedingungen. Der Nachtschlaf zeigt denselben Defekt, nur mit anderem Label.
- Kapitel 4.5 (CSD als Reset): Erhält neue Bedeutung — CSD ist nicht pathologisch, sondern kompensatorische Resynchronisation (siehe B.5).
- Kapitel 8 (Interozeptive Inkohärenz): Schlafkonsolidierung unter LDX als Spezialfall der allgemeinen Synchronisierung.
- Kapitel 9 (Evidenz): Evidenztabelle aktualisieren, Einzelfallbeobachtungen mit statistischen Befunden ersetzen.

---

### **B.1 Datengrundlage**

**Gerät:** Xiaomi Smart Band 9 (Gadgetbridge, SQLite-Export)

**Zeitraum:** 07.12.2024 – 31.03.2026

**Pharmakobedingte Periodisierung:**

| Periode | Zeitraum | Medikation | Nächte (≥60 min) |
|:--------|:---------|:-----------|:-----------------|
| PRE | Dez 2024 – Feb 2025 | Metoprolol (Betablocker) | 61 |
| *Lücke* | *Mär 2025 – Feb 2026* | *Tracker nicht getragen* | — |
| POST | Mär 2026 | Lisdexamfetamin (LDX) | 18 |

**Datentabellen (beiliegend):**

| Datei | Inhalt | Zeilen |
|:------|:-------|:-------|
| `sleep_sessions_with_hr.csv` | Nacht-Übersichten: Schlafphasen, HR-Statistiken, Effizienz | 97 |
| `sleep_stages_hypnogram.csv` | Einzelne Stadienwechsel mit Timestamps. Codes: 2=REM, 3=Light, 4=Deep, 5=Awake | 2630 |
| `hr_timeline_all.csv` | Sämtliche HR-Samples über die gesamte Timeline | 105.481 |
| `cortical_coherence_proxy.csv` | Abgeleitete Kohärenzmetriken pro Nacht | 79 |
| `deep_latency_epoch_filtered.csv` | Deep-Latenz (roh und 5-min-gefiltert), Noise-Fragmente pro Nacht | 79 |

**Tracker-Limitationen:** Der Tracker klassifiziert Schlafstadien intern über ein Fusionsmodell aus Accelerometer (Bewegung) und PPG (Herzrate). Die Rohdaten des Accelerometers sind nicht exportierbar — nur das fertige Hypnogramm und die HR-Samples stehen zur Analyse bereit. Die Stadienklassifikation kann nicht nachvollzogen oder korrigiert werden.

---

### **B.2 Fragmentierung als Desynchronisationssignal**

#### **B.2.1 Ausgangsbefund: SWS-Latenz instabil**

Die ursprüngliche Analyse ermittelte die Zeit vom Einschlafen bis zum ersten Deep-Sleep-Eintrag. Zwischen den Perioden zeigte sich eine scheinbare Verschiebung:

| Metrik | PRE | POST |
|:-------|:----|:-----|
| Deep-Latenz Median | 33 min | 43 min |
| P25 | 18 min | 30 min |
| P75 | 46 min | 50 min |
| **SD** | **26,95 min** | **15,30 min** |

Die Medianverschiebung (+10 min) deutete initial auf eine Verschlechterung. Die Halbierung der Standardabweichung (27 → 15) zeigt das Gegenteil: Der PRE-Wert streut massiv, weil er von Rauschartefakten getrieben ist, nicht von einer stabilen früheren Phasenlage.

#### **B.2.2 Epochen-basierte Reanalyse**

Um Tracker-Rauschen von echtem Signal zu trennen, wurde ein 5-Minuten-Epochen-Filter angewendet: Deep-Episoden <5 min werden als Noise-Fragmente klassifiziert. Die erste Deep-Episode ≥5 min definiert den gefilterten SWS-Onset.

**Ergebnis:** 35 von 79 Nächten enthielten Noise-Fragmente — fast ausschließlich im PRE-Zeitraum. POST zeigte kaum Fragmente (3 von 18 Nächten betroffen).

Nach Filterung:

| Metrik | PRE | POST |
|:-------|:----|:-----|
| Deep-Latenz Median (gefiltert) | 37 min | 46 min |
| P25 | 25 min | 29 min |
| P75 | 47 min | 51 min |

Die PRE-Werte stiegen durch den Filter (P25: 18→25), die POST-Werte blieben stabil — die PRE-„Frühverschiebung" war ein Artefakt der Noise-Fragmente.

#### **B.2.3 Reinterpretation: Noise ist Signal**

Die entscheidende Einsicht: Wenn der Tracker ein Single-Point-Probe des motorischen Kortex ist und der Schlafzustand räumlich inhomogen (topologisch fragmentiert), dann sind die kurzen Deep-Fragmente keine Fehlklassifikationen, sondern korrekte Momentaufnahmen eines lokalen Off-States, der den motorischen Kortex kurzzeitig erfasst.

Die temporale Fragmentierung im 1D-Tracker-Output kodiert die räumliche Fragmentierung des Kortex. Mehr Kurzfragmente = mehr Patchwork = weniger globale Kohärenz.

---

### **B.3 Quantifizierung der kortikalen Kohärenz**

#### **B.3.1 Episodenzahl pro Nacht als Kohärenzproxy**

Die einfachste und trennschärfste Metrik ist die Anzahl der Stadienepisoden pro Nacht. Der Tracker-Klassifikator fungiert als Komparator mit Schwelle: bei stabilem physiologischem Signal bleibt er in einem Zustand; bei instabilem Signal oszilliert er um die Detektionsschwelle und zählt jeden Übertritt als Stadienwechsel.

Dieser Mechanismus wirkt als nichtlinearer Verstärker: kleine Instabilität unter der Schwelle erzeugt null Übergänge, Instabilität an der Schwelle erzeugt maximale Übergänge. Die Episodenzahl ist deshalb ein sensitiveres Maß als die Episodendauer — die Dauer mittelt über das Signal, die Anzahl zählt Schwellenübertritte.

| Metrik | PRE (mean ± SD) | POST (mean ± SD) | p (Mann-Whitney) |
|:-------|:-----------------|:------------------|:-----------------|
| **Deep Episoden/Nacht** | 12,7 ± 13,0 | 7,2 ± 4,0 | **0,011** |
| **REM Episoden/Nacht** | 9,2 ± 4,7 | 6,3 ± 1,8 | **0,011** |
| Light Episoden/Nacht | 13,5 ± 10,9 | 10,1 ± 5,1 | 0,172 |
| Total Episoden/Nacht | 36,1 ± 28,9 | 23,8 ± 11,0 | **0,022** |

Normiert auf Schlafdauer:

| Metrik | PRE | POST | p |
|:-------|:----|:-----|:--|
| **Deep Episoden/Stunde** | 1,6 | 1,1 | **0,005** |
| **REM Episoden/Stunde** | 1,2 | 0,9 | **0,005** |
| Light Episoden/Stunde | 1,7 | 1,5 | 0,288 |
| Total Episoden/Stunde | 4,6 | 3,6 | **0,013** |

#### **B.3.2 Hierarchie folgt Synchronisationsanforderung**

Die Trennschärfe folgt der Hierarchie der erforderlichen kortikalen Synchronisationstiefe:

1. **Deep/SWS** (p=0,005): Erfordert maximale globale Synchronisation — langsame Oszillationen müssen den gesamten Kortex durchlaufen. Am stärksten betroffen.
2. **REM** (p=0,005): Erfordert ebenfalls globale Koordination (Muskelatonie, PGO-Wellen). Stark betroffen.
3. **Light** (p=0,288): Geringste Synchronisationsanforderung. Nicht signifikant betroffen.

Diese Hierarchie ist eine Modellvorhersage: Wenn der Upstream-Defekt (instabile Raphe → insuffiziente thalamische Modulation) die Fähigkeit zur globalen kortikalen Zustandsübergänge beeinträchtigt, müssen die Zustände mit den höchsten Kohärenzanforderungen am stärksten fragmentiert sein.

#### **B.3.3 Globale Kohärenzmetriken**

| Metrik | PRE | POST | p |
|:-------|:----|:-----|:--|
| Transitions/Stunde | 4,4 | 3,4 | **0,011** |
| Mean Episodendauer (min) | 15,2 | 18,8 | — |
| Median Episodendauer (min) | 12,9 | 16,4 | — |

Die Transitionsdichte (Stadienwechsel pro Stunde Schlaf) ist ein aggregiertes Kohärenzmaß. Die Reduktion um ~23% (4,4 → 3,4) zeigt, dass der Kortex unter LDX Zustände länger stabil hält.

#### **B.3.4 Nacht-zu-Nacht-Stabilität**

Die PRE-Standardabweichungen sind systematisch höher als die POST-Werte:

| Metrik | PRE SD | POST SD | Verhältnis |
|:-------|:-------|:--------|:-----------|
| Deep Episoden/Nacht | 13,0 | 4,0 | 3,3× |
| REM Episoden/Nacht | 4,7 | 1,8 | 2,6× |
| Deep-Latenz (ungefiltert) | 26,95 | 15,30 | 1,8× |

Die PRE-SD der Deep-Episodenzahl (13,0 bei Mean 12,7) zeigt, dass einzelne PRE-Nächte zwischen ~0 und ~40+ Deep-Episoden schwanken — massive Nacht-zu-Nacht-Instabilität der kortikalen Kohärenz. POST ist die Varianz um den Faktor 3 reduziert.

#### **B.3.5 POST-Ausreißer 28.03.2026: PRE-Nacht unter POST-Bedingungen**

| Metrik | 28.03.2026 | POST-Mean (übrige) | PRE-Mean |
|:-------|:-----------|:-------------------|:---------|
| Density (Episoden/h) | **8,99** | ~3,5 | 4,6 |
| Transitionen (total) | **61** | ~24 | 36 |
| Deep-Episoden | **21** | 3–6 | 12,7 |
| REM-Episoden | **11** | 4–6 | 9,2 |

Die Nacht vom 28.03.2026 ist das POST-Maximum und der einzige POST-Datenpunkt, der in PRE-Territorium liegt. Alle anderen Nächte mit ≥50 Transitionen sind PRE-Nächte.

**Kontext der Vornächte:** Die vier vorherigen Nächte zeigten eine monoton steigende, aber niedrige Density: 1,78 → 2,69 → 3,00 → 3,26 Episoden/h. Der Sprung auf 8,99/h ist ein Faktor-2,7-Anstieg innerhalb von 24 Stunden. Deep-Episoden springen von 3–6 auf 21, REM-Episoden von 4–6 auf 11.

**Interpretation:** Dieser Datenpunkt ist der stärkste empirische Hinweis auf einen von der Medikation unabhängigen endogenen Oszillator mit ~4-Tage-Periodizität. Die LDX-Wirkung dämpft die mittlere Fragmentierung (POST-Mean < PRE-Mean), aber der zugrundeliegende Desynchronisationszyklus durchbricht die pharmakologische Stabilisierung periodisch. Das Muster entspricht einer PRE-typischen Nacht unter POST-Bedingungen — der Upstream-Treiber ist nicht eliminiert, sondern moduliert.

**Caveat:** Einzelne Nacht, kein statistischer Test möglich. Die Interpretation stützt sich auf die Konvergenz von Effektgröße und zeitlichem Muster.

---

### **B.4 HR-Variabilität: Confounder-Analyse**

Der Versuch, die Fragmentierung über HR-Variabilität während der Deep-Phasen zu validieren, scheitert am pharmakologischen Confounder:

| Metrik | PRE (Betablocker) | POST (LDX) |
|:-------|:-------------------|:------------|
| Deep HR Mean | 62,8 | 65,4 |
| Deep HR SD (mean of nightly) | 4,8 | 5,3 |
| Deep HR CV% | 7,7 | 8,1 |

PRE ist niedriger — aber Betablocker dämpfen HR-Variabilität pharmakologisch. Die Differenz ist nicht von der Betablocker-Wirkung zu trennen. Befund: **nicht interpretierbar (confounded)**.

Die intakte vagale Kapazität ist davon unberührt: HR-Floor median 50 bpm (PRE) vs. 52 bpm (POST), absolutes Minimum 44 bpm — konsistent mit dem im Autonomen Profil dokumentierten Befund, dass die vagale Kapazität strukturell intakt, aber zustandsabhängig supprimiert ist.

---

### **B.5 Nap-Korrelation: Kompensatorischer SWS**

#### **B.5.1 Fragmentierung und Folge-Naps (PRE)**

| Metrik | Nächte mit Folge-Nap | Nächte ohne Nap |
|:-------|:---------------------|:----------------|
| Noise-Fragmente/Nacht (mean) | 11,6 | 3,3 |
| Noise-Minuten (mean) | 26,6 | 8,7 |
| Deep-Total (mean) | 129 min | 106 min |

Point-biserial r (Noise-Fragmente ~ Nap): **r=0,276, p=0,019**

Der Befund ist bemerkenswert: Nächte mit Folge-Nap zeigen 3,5× mehr Noise-Fragmente, aber *höhere* Deep-Gesamtdauer (129 vs. 106 min). Das Band klassifiziert genug Minuten als Deep — die Quantität stimmt, die Qualität nicht. Das Gehirn registriert korrekt: kein restaurativer SWS trotz ausreichender Tracker-Minuten → kompensatorischer Nap.

#### **B.5.2 POST-Naps haben anderen Treiber**

POST-Nap-Rate (26%) ist nahezu identisch mit PRE (24%), aber POST-Nap-Nächte zeigen null Noise-Fragmente. Die POST-Naps sind nicht kompensatorisch für fragmentierten SWS, sondern durch andere Faktoren motiviert (zu spät ins Bett, verkürzte Schlafzeit).

#### **B.5.3 Nap als prodromales Signal und Reset-Erfolgsrate**

Die Nap-Analyse zeigt eine doppelte Dissoziation: Naps sind prodromal für Anfälle, aber ihre Reset-Funktion unterscheidet sich fundamental zwischen PRE und POST.

**Nap als Prodrom:**

| Bedingung | P(Nap am Folgetag) |
|:----------|:-------------------|
| Nach Anfall | 19% |
| Ohne Anfall | 41% |

Naps treten *vor* Anfällen gehäuft auf, nicht danach — sie sind prodromal, nicht postdromal.

**Reset-Erfolgsrate PRE vs. POST:**

| Metrik | PRE | POST |
|:-------|:----|:-----|
| Nap-Rate | 24% | 50% |
| Nap-Reset erfolgreich (kein Anfall ≤24h) | **38%** | **78%** |
| Mean Density in Nap-Nächten | 3,75/h | 3,06/h |

POST-Naps haben einen komplett anderen Charakter: Die Nap-Rate ist doppelt so hoch (50% vs. 24%), die Naps korrelieren aber mit *niedrigerer* Density (3,06 vs. 3,75/h) und resetten in 78% erfolgreich. PRE-Naps resetten nur in 38% — sie signalisieren eine Desynchronisation, die der Nap allein nicht kompensieren kann.

**Dreiersequenz: Fragmentierte Nacht → Nap → Anfall:**

Wenn einer fragmentierten Nacht (Density ≥5/h) ein Nap folgt, münden 75% (6/8) in einen Anfall: 5/8 am selben Tag, 1/8 am Folgetag. Die Dreiersequenz identifiziert ein Hochrisiko-Fenster, in dem die kompensatorische Kapazität erschöpft ist.

**Caveat:** Kleine Stichproben (n=8 für Dreiersequenz). Die Prozentwerte sind Punktschätzer ohne Konfidenzintervall.

---

### **B.6 CSD als kompensatorische Resynchronisation**

#### **B.6.1 Reformulierung**

Die Standardinterpretation der CSD (Cortical Spreading Depression) ist pathologisch: ein Fehlereignis, das Schmerz verursacht. Die vorliegende Analyse legt eine funktionelle Reformulierung nahe:

**Konventionell:** Trigger → Schwelle überschritten → CSD → Schmerz → Dysfunktion

**Reformuliert:** Progressive kortikale Desynchronisation → Kompensation versagt → CSD als Notfall-Resynchronisation → Schmerz als metabolische Kosten → Kohärenz wiederhergestellt

Die CSD ist eine erzwungene globale kortikale Depolarisationswelle — sie durchläuft den gesamten Kortex und erzwingt einen synchronisierten Neustart. Post-CSD ist das Patchwork aufgelöst, der Kortex startet aus einem synchronisierten Zustand.

#### **B.6.2 Evidenz aus dem Verlauf**

Drei konvergierende Beobachtungslinien stützen diese Reformulierung:

**1. Post-Migräne-Klarheit und konsolidierter REM**

Schlaf nach einem Migräneanfall zeigt intensives, erinnerbares Träumen — konsolidierter REM. Die Traumerinnerung ist nicht Folge der längeren Schlafdauer (überproportionaler REM-Anteil bei langem Schlaf wäre eine alternative Erklärung), sondern der CSD-erzwungenen Resynchronisation: Der REM ist konsolidiert, weil der Kortex post-CSD global kohärent ist.

**2. Naratriptan-Gegenprobe**

Sub-CSD-Intervention durch Naratriptan verhindert den vollen Anfall → verhindert den Reset → verhindert die REM-Konsolidierung → Traumerinnerung nimmt ab. Die Abnahme bewussten Träumens ist antiproportional zum Naratriptan-Konsum — kausal konsistent.

**3. Betablocker-Paradox (revidiert)**

Unter Metoprolol: weniger Anfälle → weniger CSD-Resets → chronische Subkonsolidierung. Der „Dauerzustand von fast-Migräne, fast-Instabilität" (dokumentiert in Anhang C) ist der Zustand permanenter Fragmentierung ohne periodischen Reset. Die Betablocker entfernen den Kompensationsmechanismus, ohne den Upstream-Defekt zu adressieren.

#### **B.6.3 Evolutionäre Implikation**

Migräne betrifft ~15% der Population — eine Prävalenz, die gegen reine Dysfunktion spricht. Wenn CSD ein Notfall-Resynchronisationsmechanismus ist, selektiert die Evolution *für* die Fähigkeit zur CSD, nicht gegen sie. Der Schmerz ist die metabolische Rechnung, nicht die Funktion.

Die ~6,5-Tage-Periodizität (im vorliegenden Fall) ist dann kein Anfallszyklus, sondern ein Wartungszyklus: Die Desynchronisation akkumuliert, bis der Funktionsverlust gefährlicher ist als die CSD-Kosten.

#### **B.6.4 Therapeutische Konsequenz**

Reine Migräneprophylaxe ohne Upstream-Adressierung (Betablocker, Triptane, CGRP-Antikörper) unterdrückt den Schutzmechanismus, ohne das Synchronisationsproblem zu lösen. Der Patient wird symptomfrei bei progredient fragmentiertem Kortex.

LDX erreicht die Konsolidierung upstream: stabilisierte Raphe → kohärente thalamische Modulation → globale Zustandsübergänge → konsolidierter SWS und REM ohne CSD-Notwendigkeit.

#### **B.6.5 Vornacht-Fragmentierung als Anfallsprädiktor (t-1 Lag-Korrelation)**

Die CSD-als-Resynchronisation-These macht eine testbare Vorhersage: Wenn Desynchronisation den Anfall triggert, muss die Fragmentierung *vor* dem Anfall maximal sein und *danach* abfallen.

**Lag-Korrelation Density → Anfälle (n=56 Nacht-Folgetag-Paare):**

| Lag | Korrelation | t-Wert | p |
|:----|:------------|:-------|:--|
| t-1 (Vornacht → Folgetag-Anfall) | **r = +0,392** | **t = 3,14** | **≈ 0,003** |
| t0 (Anfall-Nacht selbst) | r = −0,065 | — | n.s. |

**Mittlere Density nach Anfallsstatus:**

| Nachttyp | Mean Density (Episoden/h) |
|:----------|:-------------------------|
| Vornächte vor Anfällen (n=14) | **5,96** |
| Anfall-Nacht selbst | **4,32** |
| Nächte ohne Anfalltag | ~3,8 |

Das Muster ist bidirektional: Fragmentierung baut sich auf (5,96/h in der Vornacht), der Anfall löst sie auf (4,32/h in der Anfall-Nacht). Die CSD-als-Resynchronisation ist damit direkt in den Density-Daten sichtbar.

**Schwellenwert-Analyse — Density ≥7,0/h als Warnsignal:**

| Density-Schwelle | Nächte | Anfall am Folgetag | Rate |
|:-----------------|:-------|:-------------------|:-----|
| ≥7,0/h | 6 | 5 | **83%** |
| <7,0/h | 50 | 9 | 18% |

5 von 6 Nächten mit einer Density ≥7,0 Episoden/h → Anfall am Folgetag. Die Effektrichtung ist eindeutig und klinisch als Warnsignal brauchbar. Die absolute Fallzahl (n=6) limitiert die Belastbarkeit des Schwellenwerts.

**Caveats:**
- n=14 Vornächte vor Anfällen. Drei Ausreißer (13,12; 9,75; 8,54/h) könnten den Korrelationseffekt treiben.
- Multiples Testen (t-1, t0 sowie Schwellenwertanalyse) ohne formale Korrektur. Der p-Wert von 0,003 überlebt eine Bonferroni-Korrektur für 2 Tests, nicht aber für explorative Schwellenwertsuche.
- Kausale Richtung (Fragmentierung → Anfall vs. gemeinsamer Upstream-Treiber → beides) ist aus Korrelationsdaten nicht trennbar.

---

### **B.7 Das Tracker-Signal: Ein stochastischer Resonanz-Detektor**

#### **B.7.1 Messtheorie**

Der Tracker ist kein Schlafstadien-Messgerät, sondern ein Single-Point-Probe des motorischen Kortex (über Accelerometer und PPG). Sein Klassifikator ist ein Komparator mit Schwelle. Die Kombination aus physiologischem Rauschen und Detektionsschwelle erzeugt ein binäres, quantisiertes Output, dessen Schaltfrequenz die Amplitude des Upstream-Rauschens kodiert.

Formal: Der Tracker digitalisiert ein kontinuierliches, räumlich inhomogenes Signal an einem festen Messpunkt. Die temporalen Fluktuationen am Messpunkt sind die 1D-Projektion der räumlichen Fragmentierung. Dies ist ein Stochastic-Resonance-Detektor: das Zusammenwirken von Signal, Rauschen und Schwelle erzeugt ein Output, das Information über das Rauschen selbst enthält.

#### **B.7.2 Informationsgehalt**

Was der Tracker misst:

- **Episodenzahl:** Anzahl der Schwellenübertritte → Proxy für autonome/kortikale Instabilität. Stärkstes Signal (p=0,005 für Deep und REM).
- **Fragmentverhältnis:** Anteil kurzer Episoden → Proxy für Patchwork-Anteil.
- **Nacht-zu-Nacht-SD:** Reproduzierbarkeit des Schlafmusters → Proxy für systemische Stabilität.

Was der Tracker *nicht* misst:

- Globale kortikale Synchronisation (dafür wäre EEG/PSG nötig)
- Räumliche Verteilung der Off-States
- Funktionelle SWS-Qualität (SWA, Slow-Wave-Slopes)

#### **B.7.3 Vergleich mit fMRT**

Der Tracker liefert für die vorliegende Fragestellung ein in einem Aspekt überlegenes Signal: Er misst kontinuierlich über die gesamte Nacht, über Monate, im natürlichen Schlafumfeld, ohne Messartefakte durch die Laborumgebung. Ein fMRT liefert höhere räumliche Auflösung, aber nur für eine einzelne Nacht unter Laborbedingungen — und misst nicht die Nacht-zu-Nacht-Variabilität, die das eigentliche Signal ist.

---

### **B.8 Konsolidierung der Traumerinnerung als subjektiver Kohärenzmarker**

POST-Beobachtung: Bewussteres, intensiveres Träumen bei gleichzeitig unverändertem REM-Anteil laut Tracker.

**Interpretation:** Der Tracker misst, ob der motorische Kortex sich im REM-typischen Profil befindet. Er misst nicht, ob der REM global konsolidiert ist. Die Traumerinnerung ist das sensitivere Instrument: Sie überlebt den Schlaf-Wach-Übergang nur, wenn die letzte REM-Phase konsolidiert genug war. Fragmentierter REM (PRE) → Traumerinnerung überlebt die Transitionen nicht. Konsolidierter REM (POST) → Erinnerung bleibt erhalten.

Konsistenzprüfung: Intensives Träumen trat PRE selektiv nach Migräneanfällen auf (CSD-erzwungene Resynchronisation → konsolidierter post-iktaler REM). Unter LDX tritt es regulär auf — die pharmakologische Synchronisation ersetzt den CSD-Reset.

---

### **B.9 Sonderanalyse: Migräne-Nacht 30./31.03.2026 mit Sumatriptan-Intervention**

Die Nacht vom 30./31.03.2026 liefert ein natürliches Experiment mit drei distinkten Phasen unter wechselnden pharmakologischen Bedingungen.

#### **B.9.1 Drei-Phasen-Verlauf**

| Phase | Zeitraum | Bedingung | Density (Ep./h) | Dauer |
|:------|:---------|:----------|:-----------------|:------|
| 1: Hauptschlaf | Nacht 30.03 | Migräne-Prodrom, kein Triptan | **2,8** | regulär |
| 2: Schlafversuch | Früh 31.03 | Schmerz, ohne Medikation | **5,3** | 57 min |
| 3: Post-Sumatriptan | Nach Einnahme | Sumatriptan, Schmerz blockiert | variabel | ~9 h |

Phase 1 zeigt eine vergleichsweise konsolidierte Nacht (2,8/h — niedriger als POST-Mean). Phase 2 dokumentiert einen Schlafversuch unter unbehandeltem Migräneschmerz: In nur 57 Minuten erreicht die Density 5,3/h — der Schmerz fragmentiert den Schlaf massiv. Phase 3 beginnt nach Sumatriptan-Einnahme.

#### **B.9.2 Post-Sumatriptan Drei-Drittel-Analyse**

Die Post-Sumatriptan-Phase wurde in Drittel unterteilt, um den zeitlichen Verlauf der Resynchronisation zu erfassen:

| Drittel | Density (Ep./h) | Interpretation |
|:--------|:-----------------|:---------------|
| Erstes Drittel | **6,1** | Residuale Fragmentierung, Schmerz blockiert aber CSD-Kaskade noch aktiv |
| Zweites Drittel | **7,5** | Maximum — paradoxe Verschlechterung, möglicherweise Rebound der Desynchronisation |
| Drittes Drittel | **5,8** | Beginn der Resynchronisation |

Das Muster zeigt keine monotone Konsolidierung, sondern eine invertierte U-Kurve mit einem Fragmentierungsmaximum im zweiten Drittel.

#### **B.9.3 HR-Verlauf als zweiter physiologischer Kanal**

| Phase | HR (bpm) | Interpretation |
|:------|:---------|:---------------|
| Hauptschlaf (Nacht) | 75,7 | Erhöht — sympathische Aktivierung durch Prodrom |
| Tiefster Punkt (Deep) | 61,2 | Vagale Kapazität intakt, aber kurzzeitig |
| Post-Sumatriptan (früh) | 70–73 | Schmerz blockiert, sympathische Restaktivierung |
| Post-Sumatriptan (spät) | 63–65 | Autonome Beruhigung, Resynchronisation |

Die HR konvergiert erst 3–4 Stunden nach Sumatriptan-Einnahme auf normale Schlafwerte. Dies definiert ein Resynchronisationsfenster: Sumatriptan blockiert den Schmerz und ermöglicht Schlaf, aber die kortikale und autonome Resynchronisation benötigt 3–4 Stunden.

#### **B.9.4 Interpretation**

Sumatriptan unterbricht die Schmerzkaskade (5-HT₁B/D-Agonismus → meningeale Vasokonstriktion → Schmerzblockade), adressiert aber nicht die kortikale Desynchronisation. Die CSD ist bereits gelaufen; das Sumatriptan ermöglicht lediglich Schlaf als Medium der Resynchronisation. Die 3–4 Stunden bis zur autonomen Normalisierung entsprechen der Dauer, die der Kortex benötigt, um post-CSD über SWS-Zyklen globale Kohärenz wiederherzustellen.

**Konsistenz mit B.6:** Der Hauptschlaf vor dem Anfall (Phase 1: 2,8/h) war konsolidiert — die Fragmentierung der Vornächte (vgl. B.6.5, t-1 Lag) hatte sich bereits in den Anfall entladen. Post-Sumatriptan beginnt die Resynchronisation von einem post-iktalen Ausgangszustand.

**Caveat:** Einzelereignis. Die Drei-Drittel-Analyse ist deskriptiv und nicht generalisierbar. Die HR-Verlaufsdaten sind durch die Sumatriptan-Pharmakokinetik (Halbwertszeit ~2h) konfundiert.

---

### **B.10 Evidenztabelle**

| Aussage | Evidenzniveau | Quelle |
|:--------|:-------------|:-------|
| Deep-Episodenzahl PRE > POST (12,7 vs. 7,2) | Statistisch signifikant (p=0,011, n=61+18) | Tracker-Daten, `cortical_coherence_proxy.csv` |
| Deep-Episoden/Stunde PRE > POST (1,6 vs. 1,1) | Statistisch signifikant (p=0,005) | Tracker-Daten, normiert auf Schlafdauer |
| REM-Episodenzahl PRE > POST (9,2 vs. 6,3) | Statistisch signifikant (p=0,011) | Tracker-Daten |
| REM-Episoden/Stunde PRE > POST (1,2 vs. 0,9) | Statistisch signifikant (p=0,005) | Tracker-Daten |
| Light-Episodenzahl: kein signifikanter Unterschied | Nicht signifikant (p=0,172) | Tracker-Daten (Kontrollsignal) |
| Transitionsdichte PRE > POST (4,4 vs. 3,4/h) | Statistisch signifikant (p=0,011) | Tracker-Daten |
| Fragmentierung korreliert mit Folge-Naps (PRE) | Signifikant (r=0,276, p=0,019) | Tracker-Daten |
| Fragmentierte Nächte zeigen höhere Deep-Gesamtdauer | Deskriptiv (129 vs. 106 min) | Tracker-Daten (Quantität ≠ Qualität) |
| Deep-Latenz SD PRE > POST (27 vs. 15 min) | Deskriptiv, große Effektstärke | Tracker-Daten |
| Deep-Latenz SD Halbierung = Kohärenzgewinn | Modellinterpretation | Abgeleitet aus B.2–B.3 |
| HR-Variabilität im Deep Sleep: nicht interpretierbar | Confounded (Betablocker) | HR-Daten, siehe B.4 |
| Hierarchie Deep > REM > Light folgt Synchronisationsanforderung | Modellvorhersage, konsistent mit Daten | Abgeleitet, keine externe Validierung |
| Tracker als stochastischer Resonanz-Detektor | Messtheoretische Interpretation | Abgeleitet aus Tracker-Architektur |
| CSD als kompensatorische Resynchronisation | Hypothetisch, konsistent mit Verlaufsdaten | Klinische Beobachtung + Modellableitung |
| Naratriptan-Konsum antiproportional zu Traumerinnerung | Einzelfallbeobachtung | Klinische Selbstbeobachtung |
| Migräneprophylaxe ohne Upstream-Adressierung = Unterdrückung des Schutzmechanismus | Modellvorhersage | Abgeleitet aus B.6, konsistent mit Betablocker-Phänomenologie |
| POST-Naps nicht kompensatorisch (null Fragmente in Nap-Nächten) | Deskriptiv | Tracker-Daten |
| POST-Ausreißer 28.03: 8,99/h Density, 61 Transitionen (POST-Maximum in PRE-Territorium) | Einzelbeobachtung, große Effektstärke | Tracker-Daten, B.3.5 |
| ~4-Tage-Oszillator unabhängig von Medikation | Hypothetisch, konsistent mit 28.03-Muster | B.3.5, Longitudinaldaten |
| Vornacht-Density → Folgetag-Anfall: r=+0,392, p≈0,003 (n=56) | Statistisch signifikant | Tracker-Daten + Anfallskalender, B.6.5 |
| Anfall-Nacht selbst: r=−0,065 (kein Signal) | Nicht signifikant | B.6.5 (Kontrollbedingung) |
| Density ≥7,0/h → Anfall am Folgetag in 83% (5/6) | Deskriptiv, kleine Stichprobe (n=6) | B.6.5 |
| POST-Nap-Reset erfolgreicher als PRE (78% vs. 38%) | Deskriptiv | Tracker-Daten, B.5.3 |
| Dreiersequenz (Fragm. Nacht → Nap → Anfall): 75% | Deskriptiv, n=8 | B.5.3 |
| Migräne-Nacht 30./31.03: Sumatriptan → 3–4h Resynchronisation (HR 75→63 bpm) | Einzelbeobachtung | HR-Daten, B.9 |
| Post-Sumatriptan Density: invertierte U-Kurve (6,1→7,5→5,8/h) | Deskriptiv, Einzelereignis | B.9.2 |

### **B.11 Limitationen**

- Consumer-Tracker, keine PSG-Validierung. Die Stadienklassifikation ist intern und nicht reproduzierbar.
- n=1, kein Kontrolldesign. Die Perioden-Trennung (PRE/POST) ist konfundiert mit Medikamentenwechsel, Jahreszeit und 13-monatiger Trageunterbrechung.
- POST-Stichprobe klein (18 Nächte). Deep-Fragmentierungsratio erreicht p=0,07 — Power-Problem bei klarer Effektrichtung.
- HR-Variabilität als Validierungsebene durch Betablocker-Confounder eliminiert.
- Die Interpretation des Trackers als „stochastischer Resonanz-Detektor" ist messtheoretisch konsistent, aber nicht extern validiert. Eine PSG-Parallelmessung wäre nötig, um die Tracker-Fragmentierung gegen globale SWA zu kalibrieren.
- Die CSD-als-Resynchronisation-These ist mechanistisch konsistent und erklärt den klinischen Verlauf, aber nicht direkt testbar ohne iktale EEG-Aufzeichnung mit post-iktaler Schlafarchitektur-Analyse.
- Die t-1 Lag-Korrelation (B.6.5) basiert auf n=14 Vornächten vor Anfällen. Drei hochfragmentierte Nächte (Density 13,12; 9,75; 8,54/h) könnten den Effekt dominieren. Multiple Vergleiche (Lag-Analyse + Schwellenwertsuche) ohne formale Korrektur.
- Die Migräne-Nacht-Sonderanalyse (B.9) ist ein Einzelereignis mit pharmakologischer Konfundierung (Sumatriptan-Halbwertszeit ~2h überlappt mit dem Beobachtungsfenster).
- Die Dreiersequenz (B.5.3) und Density-≥7,0-Schwelle (B.6.5) basieren auf n=6–8 Fällen. Diese Befunde sind hypothesengenerierend, nicht konfirmatorisch.

### **B.12 Referenzen**

*Methodische Grundlagen:*
- Bellato, A. et al. (2019). Heart rate variability in ADHD. *ADHD Attention Deficit and Hyperactivity Disorders*.
- Vyazovskiy, V. V. et al. (2011). Local sleep in awake rats. *Nature*, 472, 443–447.

*Schlafarchitektur und ADHD:*
- Bijlenga, D. et al. (2019). The role of the circadian system in ADHD. *ADHD Attention Deficit and Hyperactivity Disorders*, 11, 5–26.
- Korman, M. et al. (2025). ADHD as a circadian rhythm disorder. *Frontiers in Psychiatry*.
- Wehrle, F. et al. (2019). Reduced SWA in children with ADHD.
- Biancardi, C. et al. (2021). Sleep microstructure in ADHD.

*Migräne und Schlaf:*
- Nallet, A. et al. (2012). Sleep-related migraine occurrence. *Acta Neurologica Belgica*.
- Smitherman, T. A. & Kolivas, E. D. (2013). Migraine and sleep.

*CSD-Mechanismus:*
- Somjen, G. G. (2001). Mechanisms of spreading depression. *Physiological Reviews*.

*Raphe-Physiologie:*
- Monti, J. M. (2008). Roles of dopamine and serotonin in sleep regulation. *Progress in Brain Research*.
- Glass, J. D. et al. (2000). Dorsal raphe nuclear stimulation of SCN serotonin release. *Brain Research*.

*SWS-Initiation:*
- Oishi, Y. et al. (2017). NAcc core D2/A2A neurons and SWS induction.

