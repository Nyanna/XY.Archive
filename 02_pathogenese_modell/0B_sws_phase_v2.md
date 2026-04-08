
***

## **Anhang B: Tracker-Datenanalyse — Kortikale Desynchronisation**

### **B.0 Zusammenfassung und Synthese**

Dieser Anhang dokumentiert die Tracker-Datenanalyse der kortikalen Desynchronisation. Die ursprüngliche Fassung (Anhang B v1) postulierte eine zeitliche Verschiebung der SWS-Phasenlage; die erste Reanalyse (März 2026) identifizierte räumliche Fragmentierung als das eigentliche Signal. Die hier vorliegende Synthese (April 2026) integriert beide Ebenen: **Die räumliche Fragmentierung (Episodenzahl pro Nacht) ist die Nacht-Manifestation. Die zeitliche Akkumulation (HR-Drop-Rhythmus, quasi-wöchentliche FFT-Periodizität) ist der Treiber über Tage.** Keine Revision der SWS-Shift-These, sondern Präzisierung: Der Shift ist real, aber seine Ursache ist nicht verzögerte serotonerge Entladung allein, sondern akkumulierte kortikale Desynchronisation, die sich über den Schwebungszyklus aufbaut.

**Kernthese:** Das SWS-Defizit manifestiert sich auf zwei komplementären Ebenen — **räumlich** (intra-Nacht): Der Kortex erreicht keinen globalen SWS-Zustand, sondern zeigt ein topologisch fragmentiertes Patchwork aus lokalen Off-States; der Tracker kodiert diese räumliche Fragmentierung als temporale Instabilität. **Zeitlich** (inter-Nacht): Der nächtliche HR-Drop oszilliert mit einer dominanten Periode von 7,5 Tagen (FFT, Power 102,5; Autokorrelation Lag 7 r=0,317), kongruent mit der vorhergesagten Schwebungsfrequenz bei τ ≈ 26 h. Die zirkadiane Schwebung akkumuliert kortikale Desynchronisation über ~7 Tage; pro Nacht manifestiert sich das als variable Fragmentierung.

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

![Episode per Nacht](<images/Metabase-Episodes per Day-6.4.2026, 10_04_43.png>){width=90%}

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

**Reformuliert:** Progressive kortikale Desynchronisation → Kompensation versagt → CSD als Notfall-Resynchronisation → Schmerz als metabolische Kosten → *kortikale* Kohärenz wiederhergestellt (der autonome Zyklus bleibt unbeeinflusst, vgl. B.13.3)

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

### **B.9 Nächtliche HR-Trajektorie: Pattern-Klassifikation**

79 Nächte wurden nach dem HR-Verlauf (Entry → Exit) klassifiziert:

| Pattern | n (%) | Entry HR | Exit HR | Drop |
|:--------|:------|:---------|:--------|:-----|
| LINEAR_STARK | 29 (37%) | 72 | 60 | 12 |
| LINEAR_MODERAT | 18 (23%) | 69 | 61 | 9 |
| FLAT | 18 (23%) | 63 | 62 | 1 |
| GEMISCHT | 10 (13%) | 66 | 61 | 5 |
| ANSTIEG | 3 (4%) | 68 | 74 | -6 |

**Kernbefund:** Alle Nächte konvergieren auf denselben HR-Boden (~60–62 bpm). Die Variation liegt ausschließlich im Einstiegspunkt. Der lineare Abfall über Stunden ist sympathischer Rundown — das System geht mit erhöhtem sympathischem Tonus ins Bett und braucht die halbe Nacht für die parasympathische Übernahme.

**Mechanistische Einordnung:** Kein normales zirkadianes HR-Dipping (geschieht in der ersten Stunde). Der lineare Abfall von ~14 bpm über 7 h reflektiert verzögerte B7-Suppression im Schlaf. DRN feuert maximal bei Wachheit, stellt im Schlaf ein — bei instabiler Abschaltkinetik persistiert der sympathische Tonus über die serotonerge Modulation von LC und autonomen Kernen. FLAT-Nächte: B7 bereits vor dem Einschlafen supprimiert → System startet im parasympathischen Modus → kein Rundown nötig.

**PRE/POST-Verteilung:** Nahezu identisch (61% vs. 56% linear) — kein Medikamenteneffekt. Dies ist ein stabiles autonomes Trait.

#### **B.9.1 Der Treppenmechanismus: Räumliche Fragmentierung als Ursache des Ganznacht-Slopes**

Bei gesundem Schlaf leistet der erste NREM-Zyklus den gesamten sympathischen Rundown. Der homöostatische Schlafdruck ist bei Einschlafen maximal; der erste SWS-Block ist der tiefste und längste der Nacht. Ein einziger konsolidierter SWS-Block synchronisiert den gesamten Kortex, der parasympathische Übergang ist nach 60–90 Minuten komplett. Danach folgt ein Plateau mit Deep/REM-Oszillationen und leichtem Morgenanstieg — die in der Schlafmedizin als „Hängematte" beschriebene U-förmige HR-Kurve.

Die vorliegenden Daten zeigen das Gegenbild: Der SWS ist über die gesamte Nacht verteilt und fragmentiert, ohne dominante erste Episode. Jede kurze Deep-Episode leistet einen Bruchteil des parasympathischen Drops. Die resultierende Treppe braucht 6–8 Zyklen für den Rundown, den ein gesunder Schläfer in einem Zyklus erledigt. Der lineare Ganznacht-Slope ist damit kein langsamer autonomer Prozess, sondern die temporale Ausschmierung eines räumlich fragmentierten SWS. **Der Slope *ist* die Fragmentierung, gemessen als autonome Projektion.**

#### **B.9.2 Literaturstützung**

Die Aussage stützt sich auf mehrere konvergierende Befunde:

**Normales HR-Muster (Hängematte):** Die optimale nächtliche HR-Kurve zeigt einen schnellen Abfall in den ersten Schlafstadien, ein Minimum um die Schlafmitte (Melatonin-Peak, Kerntemperatur-Nadir ~4 Uhr) und einen Morgenwiederanstieg. Ein anhaltender Abfall über die gesamte Nacht (Oura: „Downward Slope") wird als Zeichen metabolischer Überaktivierung klassifiziert — im Gegensatz zur gesunden Hängematte.

**Intra-Zyklen-Dynamik:** Brandenberger et al. (1994) zeigen bei gesunden Probanden, dass die HR innerhalb jedes Schlafzyklus im NREM niedriger ist als im nachfolgenden REM, wobei ein globaler abfallender Trend über aufeinanderfolgende NREM- und REM-Episoden besteht. Bei gesunden Schläfern ist dieser Trend moderat, weil der erste NREM-Zyklus den Großteil des Drops leistet.

**Erstes Deep-Stadium dominant:** Der kardiovaskuläre Rundown (HR −5–10%, Blutdruck ~−10%) ist im tiefsten NREM-Stadium am ausgeprägtesten. Der erste Deep-Zyklus tritt 30–60 Minuten nach Einschlafen auf; die meiste SWS-Zeit konzentriert sich auf die erste Nachthälfte.

**Zirkadiane Interaktion:** Die parasympathische Aktivierung während SWS ist am stärksten, wenn SWS in der ersten Nachthälfte auftritt (Akrophase RRI-SWS: 01:55 ± 00:50), zeitlich übereinstimmend mit der höchsten SWS-Wahrscheinlichkeit bei Tagesorientierten (Boudreau et al., 2013).

**Synthese:** Das gesunde Muster ist schneller Abfall im ersten Zyklus → Minimum in der ersten Nachthälfte → Hängematte → Morgenanstieg. Ein linearer Abfall über die gesamte Nacht ist in keiner dieser Quellen als Normvariante beschrieben. Das Ganznacht-Slope-Muster in den vorliegenden Daten (LINEAR_STARK und LINEAR_MODERAT, zusammen 60% der Nächte) ist demnach pathologisch und spiegelt direkt die in B.2–B.3 dokumentierte SWS-Fragmentierung wider: Das System kann den sympathischen Rundown nicht in einem Zyklus leisten.

**Konvergenz mit B.10:** Der Slope als autonome Projektion der Fragmentierung erklärt, warum der HR-Drop dieselbe quasi-wöchentliche Periodizität zeigt wie die Fragmentierungsmetriken — es ist dasselbe Signal in einem anderen Messkanal.

---

### **B.10 Periodizitätsanalyse: FFT und Autokorrelation**

#### **B.10.1 FFT-Analyse (PRE-Daten, n=60 Nächte)**

| Signal | Dominante Periode | Power |
|:-------|:-----------------|:------|
| Drop (Entry-Exit) | **7,5 Tage** | 102,5 (stärkste) |
| Drop | 6,7 Tage | 82,6 |
| Slope | 7,5 Tage | 14,5 (stärkste) |
| Entry HR | 7,5 Tage | 62,8 (Platz 3) |
| Exit HR | 7,5 Tage | 66,5 |

#### **B.10.2 Autokorrelation (Drop)**

| Lag | r | Signifikanz |
|:----|:--|:------------|
| 1 | +0,278 | ** |
| 7 | +0,317 | *** |
| 14 | +0,213 | ** |
| 15 | +0,387 | *** |

#### **B.10.3 Interpretation**

Die 7,5-Tage-Periodizität im nächtlichen HR-Drop entspricht der vorhergesagten Schwebungsfrequenz bei τ ≈ 26 h (T_beat = 26×24/(26-24) = 312 h ≈ 13 Tage Vollzyklus, ~6,5 Tage Halbzyklus). Der sympathische Rundown-Slope im Nachtschlaf oszilliert mit derselben Periodizität wie der Migränezyklus.

Dies ist kein separates Phänomen — der HR-Slope *ist* die autonome Manifestation der zirkadianen Schwebung. Der Drop verstärkt das Signal durch Differenzbildung (eliminiert gemeinsames Rauschen aus Entry und Exit).

#### **B.10.4 POST-Daten**

18 Nächte reichen nicht für eine belastbare FFT bei 7-Tage-Perioden. Mindestens 25, idealerweise 40+ Nächte nötig. Zwei Vorhersagen:
- Option A: Rhythmus taucht auf → LDX ändert nur Amplitude, nicht Frequenz
- Option B: Rhythmus gestört → τ komprimiert sich unter LDX, Schwebungsperiode verlängert sich massiv

---

### **B.11 Nap-Outcome-Analyse: Zustand bei Eintritt, nicht Dauer**

#### **B.11.1 Kernbefund**

34 Naps klassifiziert nach Outcome (late_elevation >2 bpm = KASKADE, ≤2 = OK):

| Metrik | OK (n=18) | KASKADE (n=15) |
|:-------|:----------|:---------------|
| Dauer mean | 50 min | 53 min |
| HR min (absolut) | 68 | 62 |
| Pre-60min HR mean | 88 | 73 |
| Post 1h elevation | -6,1 | +2,6 |
| Late 2-4h elevation | -9,5 | +8,2 |

Dauer ist **nicht** der Diskriminator. Der Zustand vor dem Nap bestimmt das Outcome.

#### **B.11.2 Pre-Nap HR als CSD-Risikoindikator**

Stärkster Diskriminator: Pre-60min HR mean.

| Threshold | PPV(safe) | Spezifität |
|:----------|:----------|:-----------|
| ≥75 bpm | 75% | 67% |
| ≥80 bpm | 85% | 87% |
| ≥85 bpm | 90% | 93% |

Praktische Regel: Puls ≥80 vor dem Nap → safe. Puls <75 → System bereits destabilisiert, Nap beschleunigt Kaskade.

#### **B.11.3 PRE vs. POST**

PRE: 10 OK / 14 KASKADE (58% Kaskade). POST: 8 OK / 1 KASKADE (11%). Unter LDX schlagen Naps fast nie durch — stabilere Raphe verhindert die Kaskade unabhängig von Nap-Parametern.

#### **B.11.4 Reinterpretation der Nap-Kaskade**

Bisherige Formulierung in Kapitel 4.3: Nap → patchy Sleep Inertia → trigeminale Sensitisierung → CSD (kausale Kette). Synthese: Desynchronisation → Nap (kompensatorisch) + Desynchronisation → CSD (parallel). Beides sind Downstream-Effekte desselben Zustands, nicht Ursache und Wirkung. Die Sleep Inertia nach dem Nap kann den Prozess beschleunigen, ist aber nicht notwendig.

---

### **B.12 Anfallstiming: Phasenmodell**

#### **B.12.1 Befund**

15 Anfälle (PRE) korrelieren nicht mit minimalem oder maximalem Slope, sondern mit der **ansteigenden Flanke** nach dem Drop-Minimum:

| Abstand zum letzten Drop-Minimum | Anfälle |
|:---------------------------------|:--------|
| 1 Tag | 4 |
| 2 Tage | 3 |
| 3–4 Tage | 3 |
| 5–7 Tage | 2 |

Median: 2 Tage nach dem Minimum.

#### **B.12.2 Mechanismus**

Am Minimum: Raphe-Tonus niedrigster, kortikale Fragmentierung maximal, aber System insgesamt gedämpft → kein Trigger. Beim Wiederanstieg: sympathischer Drive kommt zurück, aber kortikale Kohärenz noch nicht wiederhergestellt → Diskrepanz zwischen steigendem Arousal-Drive und fragmentiertem Kortex → CSD-Schwelle erreicht.

Der Anfall korreliert mit dDrop/dt (Änderungsrate), nicht mit Drop (Amplitude). **Phasenmodell**, nicht Schwellenmodell.

#### **B.12.3 Kompatibilität mit dem Stochastischen Fenstermodell**

Das stochastische Fenstermodell (2.5.2) bleibt gültig, wird aber präzisiert: Das Vulnerabilitätsfenster öffnet sich nicht am Tiefpunkt der Schwebung, sondern auf der ansteigenden Flanke. Die Triggerstärke bestimmt, wie weit auf der Flanke der Anfall ausgelöst wird.

---

### **B.13 HR_RESTING als unabhängiger Zyklusmarker**

#### **B.13.1 Befund**

Die proprietäre Metrik HR_RESTING des Xiaomi Smart Band 9 korreliert mit Anfallstagen. Der Algorithmus ist nicht dekomponierbar (proprietär, Berechnung on-device), aber sein Output zeigt ein konsistentes Muster um Anfallstage:

**Deviation vom 5-Tage-Median (Datenreferenz: `cortical_coherence_proxy_analysis - HR Resting.csv`):**

| Kategorie | n | REST mean (bpm) | Deviation |
|:----------|:--|:-----------------|:----------|
| d-2 (Vorvortag) | 9 | 57,8 | +1,1 |
| d-1 (Vortag) | 12 | 57,8 | +1,2 |
| **Anfallstag** | 15 | 55,7 | -0,9 |
| d+1 (Folgetag) | 17 | 57,4 | +0,4 |
| Normal | 34 | 60,1 | -0,1 |

Die Elevation beginnt d-2, hält d-1, und am Anfallstag fällt REST unter die Baseline. Der Anfall sitzt auf der absteigenden Flanke — konsistent mit dem Phasenmodell (B.12).

#### **B.13.2 Absolute Schwellenwerte (periodengetrennt)**

Die Anfalls-Obergrenze ist absolut scharf, verschiebt sich aber mit dem Medikamentenprofil:

| Periode | Anfall-Obergrenze | Safe-Zone (0 Anfälle) | Anfall-Mean | Kein-Anfall-Mean |
|:--------|:------------------|:----------------------|:------------|:-----------------|
| PRE (Betablocker) | ≤62 bpm | ≥63 bpm (n=4) | 54,6 | 57,4 |
| POST (LDX) | ≤60 bpm | ≥61 bpm (n=16) | 58,7 | 61,8 |

Die POST-Verteilung ist um ~4 bpm nach oben verschoben — Betablocker drückt die gesamte HR-Distribution. Die Anfalls-Obergrenze verschiebt sich proportional mit (62→60). Anfälle treten ausschließlich in der unteren ~60% der individuellen Range auf. Der absolute Wert ist medikamentenabhängig, die relative Position ist stabil.

**Höchste Anfallsdichte:**

| Periode | Range | Anfallsrate |
|:--------|:------|:------------|
| PRE | 50–54 bpm | 47% |
| POST | 55–59 bpm | 25% |

#### **B.13.3 Post-Anfall-Verlauf**

Die CSD beeinflusst den autonomen Zyklus nicht:

| Richtung | n |
|:---------|:--|
| ↓ weiter fallend | 6 |
| ↑ Rebound | 9 |
| = gleich | 2 |

Keine systematische Richtung. Der Beat zieht unbeeindruckt seine Bahn. Die CSD resynchronisiert den Kortex (Post-Migräne-Klarheit, konsolidierter REM), aber der autonome Zyklus kümmert sich nicht darum. Dies differenziert zwei bisher vermengte Ebenen:

- **Kortikale Kohärenz** — wird durch CSD resynchronisiert. Belegt durch Traumerinnerung und Schlafkonsolidierung post-iktal.
- **Autonomer Zyklus** — läuft unabhängig, getrieben von der B7/B8-Schwebung. CSD greift nicht ein.

#### **B.13.4 Nap-Kreuzvalidierung**

Der Pre-Nap-HR-Befund (vgl. B.5) bestätigt sich als Zykluspositions-Indikator, nicht als Kausalfaktor:

- Pre-Nap HR ≥80 bpm = safe (85% PPV) → System ist früh im Zyklus, stabil.
- Pre-Nap HR <75 bpm = Kaskade → System ist auf der absteigenden Flanke, Anfall kommt unabhängig vom Nap.

Der Nap verändert den Zyklusverlauf nicht, er ist eine Projektion der aktuellen Zyklusposition.

#### **B.13.5 Algorithmische Qualitätsmerkmale**

Der Xiaomi-Algorithmus zeigt ein Konfidenz-Gating: bei atypischen Nachtprofilen (Triptan-Intervention, Tracker-Artefakte, Randdaten) gibt er HR_RESTING=0 statt eines unzuverlässigen Werts aus. Die Nicht-Null-Werte sind dadurch als algorithmisch valide eingestuft — das erhöht die Zuverlässigkeit der Deviation-Analyse.

Der Algorithmus ist nicht rekonstruierbar. Versuche, HR_RESTING aus nächtlichen HR-Perzentilen, Rolling-Minima oder Zeitfenstern vor dem Aufwachen abzuleiten, scheitern (maximale Korrelation r=0,31 bei keinem Modell). Der Algorithmus integriert vermutlich mehrere Faktoren (HR-Level, Stabilität, Bewegung, Schlafstadiendauer) auf eine Weise, die für uns nicht dekomponierbar ist. Der Output korreliert mit dem Systemzustand, der Mechanismus bleibt proprietär.

#### **B.13.6 Einordnung**

Der HR_RESTING-Befund ist eine unabhängige Kreuzvalidierung des Phasenmodells (B.12) über einen anderen Messkanal. Beide Metriken — der selbst berechnete Drop/τ und der proprietäre HR_RESTING — sind unterschiedliche Projektionen desselben Signals: der sympathovagalen Zyklusposition. Beide enthalten das Signal, beide verzerren es auf eigene Weise (unser Algorithmus bei Nicht-Sättigungskurven, der Xiaomi-Algorithmus bei atypischen Profilen). Die Konvergenz beider Metriken auf dasselbe Anfallsmuster stärkt den Befund.

#### **B.13.7 Evidenztabelle**

| Aussage | Evidenzniveau | Quelle |
|:--------|:-------------|:-------|
| HR_RESTING-Elevation d-1/d-2 vor Anfall | Deskriptiv (dev +1,1/+1,2, n=9/12) | `cortical_coherence_proxy_analysis - HR Resting.csv` |
| Kein Anfall bei REST ≥63 (PRE) bzw. ≥61 (POST) | Deskriptiv, scharfe Grenze, n=4/16 | Dieselbe Datenquelle |
| Anfallsdichte 50–54 bpm (PRE): 47% | Deskriptiv | Dieselbe Datenquelle |
| CSD verändert autonomen Zyklus nicht (6↓ / 9↑ / 2=) | Deskriptiv | Post-Anfall-Verlaufsanalyse |
| HR_RESTING-Schwelle verschiebt sich mit Medikation | Deskriptiv (PRE ≤62, POST ≤60) | Periodengetrennte Analyse |
| Nap-Outcome ist Zykluspositions-Projektion | Modellinterpretation, konsistent mit Daten | Kreuzreferenz B.5 + B.13 |
| Kortikale vs. autonome Resynchronisation differenzierbar | Modellinterpretation | Abgeleitet aus Post-Anfall-Verlauf |

---

### **B.14 Traumerinnerung als Kohärenzmarker (erweitert)**

POST: bewussteres, intensiveres Träumen bei unverändertem REM-Anteil laut Tracker. Der Tracker misst nur, ob der motorische Kortex im REM-Profil ist, nicht ob der REM global konsolidiert ist. Traumerinnerung überlebt den Schlaf-Wach-Übergang nur bei konsolidiertem REM.

**PRE-Selektivität:** Intensives Träumen trat PRE selektiv nach Migräneanfällen auf (CSD-erzwungene Resynchronisation → konsolidierter post-iktaler REM). Unter LDX tritt es regulär auf — die pharmakologische Synchronisation ersetzt den CSD-Reset.

**Betablocker/Naratriptan-Gegenprobe:** Abnahme bewussten Träumens unter Betablocker/Naratriptan: antiproportional zum sub-CSD-Naratriptankonsum. Weniger Anfälle → weniger CSD-Resets → weniger REM-Konsolidierung → weniger Traumerinnerung.

**Dreifache Dissoziation:**

| Bedingung | Traumerinnerung | Mechanismus |
|:----------|:----------------|:------------|
| PRE (ohne Anfall) | Selten | Fragmentierter REM, keine Konsolidierung |
| PRE (nach CSD) | Intensiv | CSD-erzwungene Resynchronisation → konsolidierter REM |
| POST (LDX) | Regulär | Pharmakologische Synchronisation → konsolidierter REM ohne CSD |

---

### **B.15 Sonderanalyse: Migräne-Nacht 30./31.03.2026 mit Sumatriptan-Intervention**

Die Nacht vom 30./31.03.2026 liefert ein natürliches Experiment mit drei distinkten Phasen unter wechselnden pharmakologischen Bedingungen.

#### **B.15.1 Drei-Phasen-Verlauf**

| Phase | Zeitraum | Bedingung | Density (Ep./h) | Dauer |
|:------|:---------|:----------|:-----------------|:------|
| 1: Hauptschlaf | Nacht 30.03 | Migräne-Prodrom, kein Triptan | **2,8** | regulär |
| 2: Schlafversuch | Früh 31.03 | Schmerz, ohne Medikation | **5,3** | 57 min |
| 3: Post-Sumatriptan | Nach Einnahme | Sumatriptan, Schmerz blockiert | variabel | ~9 h |

Phase 1 zeigt eine vergleichsweise konsolidierte Nacht (2,8/h — niedriger als POST-Mean). Phase 2 dokumentiert einen Schlafversuch unter unbehandeltem Migräneschmerz: In nur 57 Minuten erreicht die Density 5,3/h — der Schmerz fragmentiert den Schlaf massiv. Phase 3 beginnt nach Sumatriptan-Einnahme.

#### **B.15.2 Post-Sumatriptan Drei-Drittel-Analyse**

Die Post-Sumatriptan-Phase wurde in Drittel unterteilt, um den zeitlichen Verlauf der Resynchronisation zu erfassen:

| Drittel | Density (Ep./h) | Interpretation |
|:--------|:-----------------|:---------------|
| Erstes Drittel | **6,1** | Residuale Fragmentierung, Schmerz blockiert aber CSD-Kaskade noch aktiv |
| Zweites Drittel | **7,5** | Maximum — paradoxe Verschlechterung, möglicherweise Rebound der Desynchronisation |
| Drittes Drittel | **5,8** | Beginn der Resynchronisation |

Das Muster zeigt keine monotone Konsolidierung, sondern eine invertierte U-Kurve mit einem Fragmentierungsmaximum im zweiten Drittel.

#### **B.15.3 HR-Verlauf als zweiter physiologischer Kanal**

| Phase | HR (bpm) | Interpretation |
|:------|:---------|:---------------|
| Hauptschlaf (Nacht) bis ~23:20 Uhr | 75,7 | Erhöht — sympathische Aktivierung durch Prodrom |
| Tiefster Punkt (Deep), 0-1 Uhr | 61,2 | Vagale Kapazität intakt, aber kurzzeitig |
| Post-Sumatriptan (früh), 1-4 Uhr | 70–73 | Schmerz blockiert, sympathische Restaktivierung |
| Post-Sumatriptan (spät) nach 4 Uhr | 63–65 | Autonome Beruhigung, Resynchronisation |

Die HR konvergiert erst 3–4 Stunden nach Sumatriptan-Einnahme auf normale Schlafwerte. Dies definiert ein Resynchronisationsfenster: Sumatriptan blockiert den Schmerz und ermöglicht Schlaf, aber die kortikale und autonome Resynchronisation benötigt 3–4 Stunden.

![HR und Schlafphasen der Nacht](<images/Metabase-HR + AVG-6.4.2026, 10_16_53.png>){width=66%}
*Schlafphasen: 4 = Wach, 2 = Leichtschlaf, 1 = REM, 0 = Tiefschlaf

#### **B.15.4 Interpretation**

Sumatriptan unterbricht die Schmerzkaskade (5-HT₁B/D-Agonismus → meningeale Vasokonstriktion → Schmerzblockade), adressiert aber nicht die kortikale Desynchronisation. Die CSD ist bereits gelaufen; das Sumatriptan ermöglicht lediglich Schlaf als Medium der Resynchronisation. Die 3–4 Stunden bis zur autonomen Normalisierung entsprechen der Dauer, die der Kortex benötigt, um post-CSD über SWS-Zyklen globale Kohärenz wiederherzustellen.

**Konsistenz mit B.6:** Der Hauptschlaf vor dem Anfall (Phase 1: 2,8/h) war konsolidiert — die Fragmentierung der Vornächte (vgl. B.6.5, t-1 Lag) hatte sich bereits in den Anfall entladen. Post-Sumatriptan beginnt die Resynchronisation von einem post-iktalen Ausgangszustand.

**Caveat:** Einzelereignis. Die Drei-Drittel-Analyse ist deskriptiv und nicht generalisierbar. Die HR-Verlaufsdaten sind durch die Sumatriptan-Pharmakokinetik (Halbwertszeit ~2h) konfundiert.

---

### **B.20 Sonderanalyse: Post-exertionaler Anfall 07.04.2026 — ANS-Kollaps als eigenständiger Prozess**

Der Anfall vom 07.04.2026 liefert eine zeitliche Dissoziation zwischen ANS-Kollaps und kortikaler CSD-Kaskade, die in früheren Anfällen nicht beobachtbar war. Die LDX-bedingte Verzögerung der CSD-Schwellenunterschreitung machte die ANS-Symptome als eigenständigen, vorgelagerten Prozess sichtbar.

#### **B.20.1 Zeitlicher Verlauf**

| Phase | Zeitraum (CEST) | HR (bpm) | Bedingung |
|:------|:----------------|:---------|:----------|
| 1: Baseline | 14:00–16:25 | 77–107 | Post-Arbeit, moderate Aktivität, LDX 15 mg morgens |
| 2: Exertion | 16:28–17:45 | 115–170 | Rasenmähen, sustained HR 155–170 |
| 3: Sympathikus-Entzug | 17:46–18:37 | 131→113 | Post-exertional, Autofahrt Werkstatt (aktives Fahren) |
| 4: ANS-Dekompensation | 18:39–19:00 | 113→108 | Beifahrersitz, kein aktiver Drive; vestibuläre Symptome, Stammhirn-Ziehen |
| 5: Erschöpfungskollaps | 19:01–20:50 | 83→74 | Hinlegen, Tracker klassifiziert als Tiefschlaf|
| 6: DPH-Fenster | 20:50–22:26 | 74–81 | DPH-Einnahme ~21:00; HR-Nadir 67 bpm um 22:20; PFC→NTS-Kompensation via Atemkontrolle|
| 7: Volle Kaskade | 22:26–23:11 | 67→104 | ANS-Eskalation, Erbrechen, Kopfschmerz setzt ein; HR-Spike auf 104 |
| 8: Sumatriptan | 23:10–23:40 | 104→69 | Sumatriptan-Nasal + Paracetamol 1000 mg rektal; initialer HR-Abfall |
| 9: Triptan-Plateau | 00:25–03:20 | 80–89 | Sumatriptan-Vasokonstriktion, HR-Plateau ~82 bpm, keine Konsolidierung |
| 10: Echtes Nadir | 04:45–06:45 | 58–67 | HR-Minimum 58 bpm (04:55), zweites Minimum 59 bpm (05:37) |
| 11: Morgen | 07:00–08:00 | 70–84 | Aufwachen, rechtsseitiger Nystagmus |

#### **B.20.2 Schlafarchitektur (Tracker-Klassifikation)**

Die Tracker-Klassifikation der Nacht ist diagnostisch für die Schwere der Destabilisierung:

| Metrik | Wert | Einordnung |
|:-------|:-----|:-----------|
| Schlaf-Onset (Tracker) | 19:29 | 2+ Stunden vor typischem Onset → Erschöpfungskollaps, kein Schlaf |
| Gesamtdauer | 641 min (10,7 h) | Überlang, inklusive Prä-Bett-Kollaps |
| Deep (Tracker) | 204 min | Absolut hoch, aber nicht konsolidiert |
| REM (Tracker) | 161 min | |
| Light (Tracker) | 276 min | |
| Awake (Tracker) | 72 min | |
| Deep-Episoden | Fragmentiert, kein zusammenhängender Block >30 min erkennbar | Konsistent mit B.3: räumliche Fragmentierung bei erhaltener Gesamtdauer |

Die Phase 5 (19:29–20:50) wurde als Deep/REM klassifiziert. Phänomenologisch war dies kein Schlaf, sondern ein autonomer Zusammenbruch mit Immobilität — der Tracker detektiert Bewegungslosigkeit + niedrigen HR und klassifiziert irrtümlich als Schlaf.

#### **B.20.3 Dreifach-Konvergenz als Trigger**

Der Anfall entstand durch die zeitliche Konvergenz dreier Kompensationsentzüge:

| Faktor | Zeitpunkt | Mechanismus |
|:-------|:----------|:------------|
| Post-exertionale B7-Depletion | ab 17:46 | Sympathischer Drive maskierte Raphe-Insuffizienz; Maskierung fällt mit Belastungsende weg |
| LDX-Abklingen | ab ~18:00 | Wirkdauer 10–12 h, Einnahme morgens → abends insuffizient |
| SCN-Abendsignal | ab ~19:00 | Normales Herunterfahrsignal via SCN→B8→B7; trifft auf bereits depletierten B7 |

Jeder einzelne Faktor wäre kompensierbar gewesen. Die Dreifach-Konvergenz war es nicht.

#### **B.20.4 Befund: ANS-Kollaps als eigenständiger Prozess**

Die zentrale Beobachtung: ANS-Symptome (vestibuläre Instabilität, Schwindel, Hitzewellen, Kältewellen, Zittern, Kreislaufinstabilität) traten ab 18:39 auf — **3,5 Stunden vor der vollen CSD-Kaskade** (22:26).

| Merkmal | ANS-Kollaps | Kortikale CSD-Kaskade |
|:--------|:------------|:---------------------|
| Onset | 18:39 (Beifahrersitz) | 22:26 (volle Eskalation) |
| Latenz nach Exertion | ~55 min | ~4,5 h |
| Architektonische Distanz zu B7 | Monosynaptisch (NTS, RVLM, Ncl. ambiguus) | Polysynaptisch (thalamokortikale Schleife) |
| Kompensierbarkeit | PFC→NTS-Atemkontrolle (temporär wirksam) | Keine willentliche Kompensation |
| Zeitkonstante | Schnell in der Auslösung, lang im Verlauf | Langsam in der Auslösung, schnell im Verlauf |

**Interpretation:** Was klinisch als „Stammhirnaura" beschrieben wird, ist kein CSD-Propagationsphänomen im Hirnstamm, sondern ein eigenständiger B7→ANS-Kern-Kollaps. Ohne LDX überlagern sich beide Prozesse zeitlich und sind klinisch nicht trennbar. LDX erzeugte unbeabsichtigt eine diagnostische Separation, indem es die CSD-Schwelle länger hielt, während der ANS-Kollaps ungehindert ablief.

#### **B.20.5 PFC→NTS-Kompensation und deren Erschöpfung**

Die bewusste Atemkontrolle (langsames Ausatmen gegen autonome Reflexe) war effektiv gegen:
- Vestibuläre Instabilität (Schwindel reduziert)
- Übelkeit (gebremst)
- Hitzewellen (unterdrückt)

Die Kompensation nutzt den PFC→NTS-Pfad — willentliche Top-down-Kontrolle über autonome Kerne. Dieser Pfad wird gleichzeitig durch dieselben Faktoren destabilisiert, die den ANS-Kollaps treiben (LDX-Abklingen, B7-Depletion). Die Kompensation verbraucht die Ressource, die sie zu ersetzen versucht.

Empirischer Beleg: Aktives Fahren (Phase 3, hoher PFC-Demand) → NTS-Suppression erfolgreich trotz extremer Triggerbelastung. Beifahrersitz (Phase 4, kein PFC-Demand) → Dekompensation innerhalb von Minuten.

#### **B.20.6 Triptan-Pharmakokinetik im HR**

| Phase | Zeitraum | HR (bpm) | Mechanismus |
|:------|:---------|:---------|:------------|
| Pre-Triptan Nadir | 22:20 | 67 | Maximaler vagaler Tonus bei ANS-Erschöpfung |
| ANS-Spike | 22:26–23:10 | 67→104 | Volle Kaskade: CSD + Erbrechen |
| Initialer Triptan-Effekt | 23:10–23:40 | 104→69 | Schmerzblockade → sympathische Deaktivierung |
| Triptan-Rebound | 00:25–03:20 | 80–89 | 5-HT1B/1D-Vasokonstriktion → sympathische Restaktivierung |
| Post-Triptan-Clearance | 04:45–06:45 | 58–67 | Sumatriptan-HWZ ~2h; erst nach Clearance echtes Nadir |

Das Triptan-Plateau (HR ~82 bpm über ~3 Stunden) ist konsistent mit B.15: Die Resynchronisationszeit beträgt 3–4 Stunden, und das Triptan konfundiert den HR-Verlauf über seine Halbwertszeit. Das echte Nadir (58 bpm) tritt erst nach Triptan-Clearance auf — ähnlich wie in B.15.3.

**Differenz zu B.15:** In B.15 lag der Post-Sumatriptan-HR bei 70–73 bpm (Phase 3), hier bei 80–89. Die Differenz erklärt sich durch die exertionale Vorbelastung: Die sympathische Restaktivierung durch die post-exertionale Depletion addiert sich zur Triptan-Vasokonstriktion.

#### **B.20.7 Konsistente Nystagmus-Lateralisierung**

Am Morgen nach dem Anfall: Nystagmus rechtsseitig. Konsistent mit früheren Anfällen (immer rechts). Zwei Hypothesen:

| Hypothese | Mechanismus | Vorhersage |
|:----------|:------------|:-----------|
| Architektonisch | Asymmetrische B7-Innervierung vestibulärer Kerne; eine Seite hat weniger Reservekapazität | Fixe Lateralisierung unabhängig von CSD-Hemisphäre |
| Funktionell | CSD-Propagation bevorzugt eine Hemisphäre; kontralaterale vestibuläre Manifestation | Lateralisierung könnte bei atypischen CSD-Pfaden wechseln |

Die Konsistenz über multiple Anfälle spricht für die architektonische Variante.

#### **B.20.8 Evidenztabelle**

| Aussage | Evidenzniveau | Quelle |
|:--------|:-------------|:-------|
| ANS-Symptome 3,5 h vor CSD-Kaskade | Einzelfallbeobachtung | Symptomprotokoll + HR-Daten |
| Tracker klassifiziert Erschöpfungskollaps als Tiefschlaf | Einzelfallbeobachtung | Tracker-Daten (HR 75–83 statt <65 bpm für echten Deep) |
| PFC→NTS-Kompensation temporär wirksam, dann erschöpft | Einzelfallbeobachtung | Symptomprotokoll (Fahren vs. Beifahrersitz) |
| Dreifach-Konvergenz (post-exertional + LDX-Abklingen + SCN-Signal) | Modellinterpretation, konsistent | Zeitlicher Verlauf + Modellarchitektur |
| Triptan-Plateau bei HR ~82 über 3 h | Einzelfallbeobachtung | HR-Daten |
| Echtes HR-Nadir erst nach Triptan-Clearance (58 bpm) | Einzelfallbeobachtung | HR-Daten |
| Nystagmus konsistent rechtsseitig | Deskriptiv, über multiple Anfälle | Symptomprotokoll |
| ANS-Kollaps ≠ Stammhirnaura (≠ Brainstem-CSD) | Modellinterpretation, gestützt durch temporale Dissoziation | B.20.4 |

#### **B.20.9 Modellimplikation**

Die temporale Dissoziation erzwingt eine Korrektur: Was als „Stammhirnaura" (MBA) klassifiziert wird, ist kein CSD-Propagationsphänomen, sondern ein eigenständiger B7→ANS-Kern-Kollaps. Die Implikationen:

1. **Architektonische Priorität:** ANS-Kerne liegen monosynaptisch an B7 — sie destabilisieren vor dem polysynaptischen thalamokortikalen Pfad. Die Sequenz ist architektonisch determiniert, nicht stochastisch.
2. **Maskierung ohne LDX:** Ohne LDX eskaliert CSD schneller → ANS-Kollaps und CSD überlagern sich zeitlich → klinisch als einheitliche „Aura" fehlinterpretiert.
3. **Brainstem-CSD beim Menschen:** Keine humane Evidenz. Die einzige Grundlage ist das Cacna1a-S218L-Mausmodell (van den Maagdenberg et al.). Die ANS-Kollaps-Reattribution eliminiert die Notwendigkeit dieser unbelegten Hilfshypothese.
4. **Parsimoniegewinn:** Sämtliche MBA-Symptome folgen aus der architektonischen Proximität der ANS-Kerne zum Raphe-System — ein Mechanismus, der aus dem B7/B8-Interferenzmodell direkt ableitbar ist.

**Caveat:** Einzelereignis. Die temporale Dissoziation war nur durch die spezifische Konstellation (exertionale Vorbelastung + LDX-Abklingen) beobachtbar. Reproduzierbarkeit nicht gesichert — allerdings spricht die konsistente Nystagmus-Lateralisierung über multiple Anfälle für ein architektonisch stabiles Muster.

![HR-Timeline Anfall 07.04.2026](<images/B20_hr_timeline_20260407.png>)
*HR-Minutenauflösung, CEST. Annotationen: Rasenmähen (rot), Interventionen (gestrichelt), Kaskade (rot), Triptan-Plateau (amber), echtes Nadir (grün).*

![HR-Timeline Tag 07.04.2026](<images/Metabase-HR + AVG - Day-4_8_2026, 11_24_18 AM.png>)

![HR-Sleep-Timeline Schlaf 07.04.2026](<images/Metabase-HR + AVG-4_8_2026, 11_23_07 AM.png>)

---

### **B.17 Evidenztabelle**

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
| Migräne-Nacht 30./31.03: Sumatriptan → 3–4h Resynchronisation (HR 75→63 bpm) | Einzelbeobachtung | HR-Daten, B.15 |
| Post-Sumatriptan Density: invertierte U-Kurve (6,1→7,5→5,8/h) | Deskriptiv, Einzelereignis | B.15.2 |
| HR-Drop-Periodizität 7,5 Tage (FFT, Power 102,5) | Statistisch signifikant (n=60 Nächte) | Tracker-Daten, FFT-Analyse (B.10) |
| Autokorrelation Lag 7 (r=0,317) und Lag 14 (r=0,213) | Statistisch signifikant | Tracker-Daten, Autokorrelation (B.10) |
| Nap-Outcome durch Pre-Nap-HR determiniert (PPV 85% bei ≥80 bpm) | Statistisch signifikant (n=33) | Tracker-Daten, HR-Analyse (B.11) |
| Anfall auf ansteigender Flanke, Median 2 Tage nach Minimum | Deskriptiv (n=15) | Tracker-Daten + Anfallskalender (B.12) |
| PRE/POST HR-Trajectory-Verteilung identisch (61% vs. 56% linear) | Deskriptiv | Tracker-Daten (B.9) |
| Ganznacht-Slope = temporale Ausschmierung räumlich fragmentierter SWS | Modellinterpretation, konvergent mit B.2–B.3 | Abgeleitet aus HR-Trajectory + Fragmentierungsdaten (B.9.1) |
| Gesundes Muster: erster NREM-Zyklus leistet gesamten sympathischen Rundown in 60–90 min | Literaturgestützt | Brandenberger et al. 1994, Boudreau et al. 2013 (B.9.2) |
| Linearer Ganznacht-Slope in keiner Quelle als Normvariante beschrieben | Literaturgestützt | Übersicht B.9.2 |
| POST-Nap-Kaskadenrate 11% vs. PRE 58% | Deskriptiv | Tracker-Daten (B.11) |
| SWS-Fragmentierung als Mediator orthographischer Engramm-Instabilität (LRS-Phänotyp) | Modellvorhersage | Abgeleitet aus Anhang D, D.7.3 — orthographische Konsolidierung SWS-abhängig |
| HR_RESTING als unabhängiger Zyklusmarker (Elevation d-1/d-2, Drop am Anfallstag) | Deskriptiv, kreuzvalidiert | B.13, `cortical_coherence_proxy_analysis - HR Resting.csv` |
| CSD resynchronisiert Kortex, nicht autonomen Zyklus | Modellinterpretation, konsistent mit Daten | B.13.3 |
| Anfalls-Schwelle relativ zur individuellen HR-Range, nicht absolut | Deskriptiv | B.13.2 |

### **B.18 Revisionstabelle**

| Kapitel | Revision | Priorität |
|:--------|:---------|:----------|
| **4.5** (CSD als Reset) | Differenzierung ergänzen: CSD resynchronisiert kortikale Kohärenz, aber nicht den autonomen Zyklus. Der Beat läuft unbeeindruckt weiter. Verweis auf B.13.3. | Mittel — Präzisierung, kein Widerspruch |

### **B.19 Limitationen**

- Consumer-Tracker, keine PSG-Validierung. Die Stadienklassifikation ist intern und nicht reproduzierbar.
- n=1, kein Kontrolldesign. Die Perioden-Trennung (PRE/POST) ist konfundiert mit Medikamentenwechsel, Jahreszeit und 13-monatiger Trageunterbrechung.
- POST-Stichprobe klein (18 Nächte). Deep-Fragmentierungsratio erreicht p=0,07 — Power-Problem bei klarer Effektrichtung.
- HR-Variabilität als Validierungsebene durch Betablocker-Confounder eliminiert.
- Die Interpretation des Trackers als „stochastischer Resonanz-Detektor" ist messtheoretisch konsistent, aber nicht extern validiert. Eine PSG-Parallelmessung wäre nötig, um die Tracker-Fragmentierung gegen globale SWA zu kalibrieren.
- Die CSD-als-Resynchronisation-These ist mechanistisch konsistent und erklärt den klinischen Verlauf, aber nicht direkt testbar ohne iktale EEG-Aufzeichnung mit post-iktaler Schlafarchitektur-Analyse.
- Die t-1 Lag-Korrelation (B.6.5) basiert auf n=14 Vornächten vor Anfällen. Drei hochfragmentierte Nächte (Density 13,12; 9,75; 8,54/h) könnten den Effekt dominieren. Multiple Vergleiche (Lag-Analyse + Schwellenwertsuche) ohne formale Korrektur.
- Die Migräne-Nacht-Sonderanalyse (B.15) ist ein Einzelereignis mit pharmakologischer Konfundierung (Sumatriptan-Halbwertszeit ~2h überlappt mit dem Beobachtungsfenster).
- Die Dreiersequenz (B.5.3) und Density-≥7,0-Schwelle (B.6.5) basieren auf n=6–8 Fällen. Diese Befunde sind hypothesengenerierend, nicht konfirmatorisch.
- POST-Stichprobe zu klein für belastbare FFT bei 7-Tage-Perioden (18 Nächte, mindestens 25 nötig). Die Periodizitätsanalyse (B.10) basiert ausschließlich auf PRE-Daten.
- Anfalls-Korrelation mit Phase (B.12): n=15, Abstände manuell annotiert. Konsistentes Muster, aber keine formale statistische Testung der Phasen-Hypothese.
- Nap-Outcome-Analyse (B.11): Kaskadenklassifikation über late_elevation >2 bpm. Schwellenwert empirisch gewählt, nicht extern validiert.
- Die Daten sind insgesamt robuster als erwartet für einen Consumer-Tracker, aber die Annahmen können bei längerer Erfassung noch kippen. Es wird mit zunehmender Datenmenge unwahrscheinlicher.

### **B.20 Diagnostische Implikation: Tracker-basiertes Screening**

Ein Consumer-Schlaftracker (30 €) + Open-Source-App (Gadgetbridge) liefert einen kontinuierlichen, nicht-invasiven Biomarker für die zirkadiane Schwebung — einen Prozess, den die klinische Forschung mit PET und PSG sucht.

**Methodik:** Standard-Data-Engineering: Gewinnung korrelativer Daten aus Rauschquellen durch geeignete Signalverarbeitung. Kein technologischer Durchbruch — der Tracker ist ein stochastischer Resonanz-Detektor (B.7), dessen Schaltfrequenz die Upstream-Instabilität kodiert. Die relevanten Metriken (Episodenzahl/h, HR-Drop-Periodizität, Pre-Nap-HR) erfordern keine Rohdaten-Zugänge, sondern nur das Standard-Hypnogramm und die HR-Timeline.

**Vorteile gegenüber klinischer Diagnostik:**
- Kontinuierlich über Monate (Nacht-zu-Nacht-Variabilität als eigentliches Signal)
- Natürliches Schlafumfeld (keine Laborartefakte)
- Erfassung der quasi-wöchentlichen Periodizität (erfordert mindestens 4–6 Wochen Daten)
- Kostenfaktor: ~30 € vs. mehrere Tausend für PSG

**Limitationen:**
- Keine räumliche Auflösung, keine SWA, keine direkte Validierung der Kohärenz-Interpretation
- Stadienklassifikation intern, nicht nachvollziehbar oder korrigierbar
- n=1-Validierung, keine externe Replikation

**Prospektiv testbar:** Systematische HR-Trajectory-Analyse über 4–6 Wochen als Screening-Tool für Raphe-Dysregulation bei ADHS-Migräne-Koinzidenz. Die Vorhersage: Patienten mit diesem Phänotyp zeigen (a) erhöhte Schlaffragmentierung (Deep-Episoden/h >1,3), (b) quasi-wöchentliche Periodizität im HR-Drop und (c) zustandsabhängige Nap-Outcomes.

---

### **B.21 Referenzen**

*Methodische Grundlagen:*
- Bellato, A. et al. (2019). Heart rate variability in ADHD. *ADHD Attention Deficit and Hyperactivity Disorders*.
- Vyazovskiy, V. V. et al. (2011). Local sleep in awake rats. *Nature*, 472, 443–447.

*Schlafarchitektur und ADHD:*
- Bijlenga, D. et al. (2019). The role of the circadian system in ADHD. *ADHD Attention Deficit and Hyperactivity Disorders*, 11, 5–26.
- Korman, M. et al. (2025). ADHD as a circadian rhythm disorder. *Frontiers in Psychiatry*.
- Wehrle, F. et al. (2019). Reduced SWA in children with ADHD.
- Biancardi, C. et al. (2021). Sleep microstructure in ADHD.

*Kardiovaskuläre Schlafphysiologie:*
- Brandenberger, G. et al. (1994). Ultradian rhythms in heart rate and cardiac vagal tone during sleep. *Journal of Biological Rhythms*, 9(2), 165–178.
- Boudreau, P. et al. (2013). Circadian variation of heart rate variability across sleep stages. *Sleep*, 36(12), 1919–1928.

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
