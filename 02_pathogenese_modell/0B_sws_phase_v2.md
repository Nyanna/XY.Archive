
***

## **Anhang B: Tracker-Datenanalyse — Kortikale Desynchronisation**

**Zusammenfassung und Synthese**

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

**Ausgangsbefund: SWS-Latenz instabil**

Die ursprüngliche Analyse ermittelte die Zeit vom Einschlafen bis zum ersten Deep-Sleep-Eintrag. Zwischen den Perioden zeigte sich eine scheinbare Verschiebung:

| Metrik | PRE | POST |
|:-------|:----|:-----|
| Deep-Latenz Median | 33 min | 43 min |
| P25 | 18 min | 30 min |
| P75 | 46 min | 50 min |
| **SD** | **26,95 min** | **15,30 min** |

Die Medianverschiebung (+10 min) deutete initial auf eine Verschlechterung. Die Halbierung der Standardabweichung (27 → 15) zeigt das Gegenteil: Der PRE-Wert streut massiv, weil er von Rauschartefakten getrieben ist, nicht von einer stabilen früheren Phasenlage.

**Epochen-basierte Reanalyse**

Um Tracker-Rauschen von echtem Signal zu trennen, wurde ein 5-Minuten-Epochen-Filter angewendet: Deep-Episoden <5 min werden als Noise-Fragmente klassifiziert. Die erste Deep-Episode ≥5 min definiert den gefilterten SWS-Onset.

**Ergebnis:** 35 von 79 Nächten enthielten Noise-Fragmente — fast ausschließlich im PRE-Zeitraum. POST zeigte kaum Fragmente (3 von 18 Nächten betroffen).

Nach Filterung:

| Metrik | PRE | POST |
|:-------|:----|:-----|
| Deep-Latenz Median (gefiltert) | 37 min | 46 min |
| P25 | 25 min | 29 min |
| P75 | 47 min | 51 min |

Die PRE-Werte stiegen durch den Filter (P25: 18→25), die POST-Werte blieben stabil — die PRE-„Frühverschiebung" war ein Artefakt der Noise-Fragmente.

**Reinterpretation: Noise ist Signal**

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

**Hierarchie folgt Synchronisationsanforderung**

Die Trennschärfe folgt der Hierarchie der erforderlichen kortikalen Synchronisationstiefe:

1. **Deep/SWS** (p=0,005): Erfordert maximale globale Synchronisation — langsame Oszillationen müssen den gesamten Kortex durchlaufen. Am stärksten betroffen.
2. **REM** (p=0,005): Erfordert ebenfalls globale Koordination (Muskelatonie, PGO-Wellen). Stark betroffen.
3. **Light** (p=0,288): Geringste Synchronisationsanforderung. Nicht signifikant betroffen.

Diese Hierarchie ist eine Modellvorhersage: Wenn der Upstream-Defekt (instabile Raphe → insuffiziente thalamische Modulation) die Fähigkeit zur globalen kortikalen Zustandsübergänge beeinträchtigt, müssen die Zustände mit den höchsten Kohärenzanforderungen am stärksten fragmentiert sein.

**Globale Kohärenzmetriken**

| Metrik | PRE | POST | p |
|:-------|:----|:-----|:--|
| Transitions/Stunde | 4,4 | 3,4 | **0,011** |
| Mean Episodendauer (min) | 15,2 | 18,8 | — |
| Median Episodendauer (min) | 12,9 | 16,4 | — |

Die Transitionsdichte (Stadienwechsel pro Stunde Schlaf) ist ein aggregiertes Kohärenzmaß. Die Reduktion um ~23% (4,4 → 3,4) zeigt, dass der Kortex unter LDX Zustände länger stabil hält.

**Nacht-zu-Nacht-Stabilität**

Die PRE-Standardabweichungen sind systematisch höher als die POST-Werte:

| Metrik | PRE SD | POST SD | Verhältnis |
|:-------|:-------|:--------|:-----------|
| Deep Episoden/Nacht | 13,0 | 4,0 | 3,3× |
| REM Episoden/Nacht | 4,7 | 1,8 | 2,6× |
| Deep-Latenz (ungefiltert) | 26,95 | 15,30 | 1,8× |

Die PRE-SD der Deep-Episodenzahl (13,0 bei Mean 12,7) zeigt, dass einzelne PRE-Nächte zwischen ~0 und ~40+ Deep-Episoden schwanken — massive Nacht-zu-Nacht-Instabilität der kortikalen Kohärenz. POST ist die Varianz um den Faktor 3 reduziert.

#### **B.3.2 POST-Ausreißer 28.03.2026: PRE-Nacht unter POST-Bedingungen**

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

**Fragmentierung und Folge-Naps (PRE)**

| Metrik | Nächte mit Folge-Nap | Nächte ohne Nap |
|:-------|:---------------------|:----------------|
| Noise-Fragmente/Nacht (mean) | 11,6 | 3,3 |
| Noise-Minuten (mean) | 26,6 | 8,7 |
| Deep-Total (mean) | 129 min | 106 min |

Point-biserial r (Noise-Fragmente ~ Nap): **r=0,276, p=0,019**

Der Befund ist bemerkenswert: Nächte mit Folge-Nap zeigen 3,5× mehr Noise-Fragmente, aber *höhere* Deep-Gesamtdauer (129 vs. 106 min). Das Band klassifiziert genug Minuten als Deep — die Quantität stimmt, die Qualität nicht. Das Gehirn registriert korrekt: kein restaurativer SWS trotz ausreichender Tracker-Minuten → kompensatorischer Nap.

**POST-Naps haben anderen Treiber**

POST-Nap-Rate (26%) ist nahezu identisch mit PRE (24%), aber POST-Nap-Nächte zeigen null Noise-Fragmente. Die POST-Naps sind nicht kompensatorisch für fragmentierten SWS, sondern durch andere Faktoren motiviert (zu spät ins Bett, verkürzte Schlafzeit).

#### **B.5.1 Nap als prodromales Signal und Reset-Erfolgsrate**

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

**Reformulierung**

Die Standardinterpretation der CSD (Cortical Spreading Depression) ist pathologisch: ein Fehlereignis, das Schmerz verursacht. Die vorliegende Analyse legt eine funktionelle Reformulierung nahe:

**Konventionell:** Trigger → Schwelle überschritten → CSD → Schmerz → Dysfunktion

**Reformuliert:** Progressive kortikale Desynchronisation → Kompensation versagt → CSD als Notfall-Resynchronisation → Schmerz als metabolische Kosten → *kortikale* Kohärenz wiederhergestellt (der autonome Zyklus bleibt unbeeinflusst, vgl. B.13.2)

Die CSD ist eine erzwungene globale kortikale Depolarisationswelle — sie durchläuft den gesamten Kortex und erzwingt einen synchronisierten Neustart. Post-CSD ist das Patchwork aufgelöst, der Kortex startet aus einem synchronisierten Zustand.

#### **B.6.1 Evidenz aus dem Verlauf**

Drei konvergierende Beobachtungslinien stützen diese Reformulierung:

**1. Post-Migräne-Klarheit und konsolidierter REM**

Schlaf nach einem Migräneanfall zeigt intensives, erinnerbares Träumen — konsolidierter REM. Die Traumerinnerung ist nicht Folge der längeren Schlafdauer (überproportionaler REM-Anteil bei langem Schlaf wäre eine alternative Erklärung), sondern der CSD-erzwungenen Resynchronisation: Der REM ist konsolidiert, weil der Kortex post-CSD global kohärent ist.

**2. Naratriptan-Gegenprobe**

Sub-CSD-Intervention durch Naratriptan verhindert den vollen Anfall → verhindert den Reset → verhindert die REM-Konsolidierung → Traumerinnerung nimmt ab. Die Abnahme bewussten Träumens ist antiproportional zum Naratriptan-Konsum — kausal konsistent.

**3. Betablocker-Paradox (revidiert)**

Unter Metoprolol: weniger Anfälle → weniger CSD-Resets → chronische Subkonsolidierung. Der „Dauerzustand von fast-Migräne, fast-Instabilität" (dokumentiert in Anhang C) ist der Zustand permanenter Fragmentierung ohne periodischen Reset. Die Betablocker entfernen den Kompensationsmechanismus, ohne den Upstream-Defekt zu adressieren.

**Evolutionäre Implikation**

Migräne betrifft ~15% der Population — eine Prävalenz, die gegen reine Dysfunktion spricht. Wenn CSD ein Notfall-Resynchronisationsmechanismus ist, selektiert die Evolution *für* die Fähigkeit zur CSD, nicht gegen sie. Der Schmerz ist die metabolische Rechnung, nicht die Funktion.

Die ~6,5-Tage-Periodizität (im vorliegenden Fall) ist dann kein Anfallszyklus, sondern ein Wartungszyklus: Die Desynchronisation akkumuliert, bis der Funktionsverlust gefährlicher ist als die CSD-Kosten.

**Therapeutische Konsequenz**

Reine Migräneprophylaxe ohne Upstream-Adressierung (Betablocker, Triptane, CGRP-Antikörper) unterdrückt den Schutzmechanismus, ohne das Synchronisationsproblem zu lösen. Der Patient wird symptomfrei bei progredient fragmentiertem Kortex.

LDX erreicht die Konsolidierung upstream: stabilisierte Raphe → kohärente thalamische Modulation → globale Zustandsübergänge → konsolidierter SWS und REM ohne CSD-Notwendigkeit.

#### **B.6.2 Vornacht-Fragmentierung als Anfallsprädiktor (t-1 Lag-Korrelation)**

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

**Messtheorie**

Der Tracker ist kein Schlafstadien-Messgerät, sondern ein Single-Point-Probe des motorischen Kortex (über Accelerometer und PPG). Sein Klassifikator ist ein Komparator mit Schwelle. Die Kombination aus physiologischem Rauschen und Detektionsschwelle erzeugt ein binäres, quantisiertes Output, dessen Schaltfrequenz die Amplitude des Upstream-Rauschens kodiert.

Formal: Der Tracker digitalisiert ein kontinuierliches, räumlich inhomogenes Signal an einem festen Messpunkt. Die temporalen Fluktuationen am Messpunkt sind die 1D-Projektion der räumlichen Fragmentierung. Dies ist ein Stochastic-Resonance-Detektor: das Zusammenwirken von Signal, Rauschen und Schwelle erzeugt ein Output, das Information über das Rauschen selbst enthält.

**Informationsgehalt**

Was der Tracker misst:

- **Episodenzahl:** Anzahl der Schwellenübertritte → Proxy für autonome/kortikale Instabilität. Stärkstes Signal (p=0,005 für Deep und REM).
- **Fragmentverhältnis:** Anteil kurzer Episoden → Proxy für Patchwork-Anteil.
- **Nacht-zu-Nacht-SD:** Reproduzierbarkeit des Schlafmusters → Proxy für systemische Stabilität.

Was der Tracker *nicht* misst:

- Globale kortikale Synchronisation (dafür wäre EEG/PSG nötig)
- Räumliche Verteilung der Off-States
- Funktionelle SWS-Qualität (SWA, Slow-Wave-Slopes)

**Vergleich mit fMRT**

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

**FFT-Analyse (PRE-Daten, n=60 Nächte)**

| Signal | Dominante Periode | Power |
|:-------|:-----------------|:------|
| Drop (Entry-Exit) | **7,5 Tage** | 102,5 (stärkste) |
| Drop | 6,7 Tage | 82,6 |
| Slope | 7,5 Tage | 14,5 (stärkste) |
| Entry HR | 7,5 Tage | 62,8 (Platz 3) |
| Exit HR | 7,5 Tage | 66,5 |

**Autokorrelation (Drop)**

| Lag | r | Signifikanz |
|:----|:--|:------------|
| 1 | +0,278 | ** |
| 7 | +0,317 | *** |
| 14 | +0,213 | ** |
| 15 | +0,387 | *** |

**Interpretation**

Die 7,5-Tage-Periodizität im nächtlichen HR-Drop entspricht der vorhergesagten Schwebungsfrequenz bei τ ≈ 26 h (T_beat = 26×24/(26-24) = 312 h ≈ 13 Tage Vollzyklus, ~6,5 Tage Halbzyklus). Der sympathische Rundown-Slope im Nachtschlaf oszilliert mit derselben Periodizität wie der Migränezyklus.

Dies ist kein separates Phänomen — der HR-Slope *ist* die autonome Manifestation der zirkadianen Schwebung. Der Drop verstärkt das Signal durch Differenzbildung (eliminiert gemeinsames Rauschen aus Entry und Exit).

Die 7,5-Tage-Periodizität ist strukturell die PRE-Projektion der Intertakt-Drift von B7 gegen B8-SCN-Lock, superponiert mit der zirkadianen Schwebung (τ ≈ 26 h). Unter LDX POST wird die zirkadiane Schwebung eliminiert (r = −0,831 Einschlafzeit ~ Schlafdauer); was bleibt, ist die ~4-Tage-Eigenperiode der reinen B7-Intertakt-Drift (Autokorrelation Lag 4 r = −0,692, §2.5.1). Die Differenz zwischen PRE (~7,5 d) und POST (~4 d) ist damit nicht Hinweis auf einen anderen Mechanismus, sondern das Auftrennen einer Superposition.

**POST-Daten**

18 Nächte reichen nicht für eine belastbare FFT bei 7-Tage-Perioden. Mindestens 25, idealerweise 40+ Nächte nötig. Zwei Vorhersagen:
- Option A: Rhythmus taucht auf → LDX ändert nur Amplitude, nicht Frequenz
- Option B: Rhythmus gestört → τ komprimiert sich unter LDX, Schwebungsperiode verlängert sich massiv

---

### **B.11 Nap-Outcome-Analyse: Zustand bei Eintritt, nicht Dauer**

**Kernbefund**

34 Naps klassifiziert nach Outcome (late_elevation >2 bpm = KASKADE, ≤2 = OK):

| Metrik | OK (n=18) | KASKADE (n=15) |
|:-------|:----------|:---------------|
| Dauer mean | 50 min | 53 min |
| HR min (absolut) | 68 | 62 |
| Pre-60min HR mean | 88 | 73 |
| Post 1h elevation | -6,1 | +2,6 |
| Late 2-4h elevation | -9,5 | +8,2 |

Dauer ist **nicht** der Diskriminator. Der Zustand vor dem Nap bestimmt das Outcome.

**Pre-Nap HR als CSD-Risikoindikator**

Stärkster Diskriminator: Pre-60min HR mean.

| Threshold | PPV(safe) | Spezifität |
|:----------|:----------|:-----------|
| ≥75 bpm | 75% | 67% |
| ≥80 bpm | 85% | 87% |
| ≥85 bpm | 90% | 93% |

Praktische Regel: Puls ≥80 vor dem Nap → safe. Puls <75 → System bereits destabilisiert, Nap beschleunigt Kaskade.

**PRE vs. POST**

PRE: 10 OK / 14 KASKADE (58% Kaskade). POST: 8 OK / 1 KASKADE (11%). Unter LDX schlagen Naps fast nie durch — stabilere Raphe verhindert die Kaskade unabhängig von Nap-Parametern.

**Reinterpretation der Nap-Kaskade**

Bisherige Formulierung in Kapitel 4.3: Nap → patchy Sleep Inertia → trigeminale Sensitisierung → CSD (kausale Kette). Synthese: Desynchronisation → Nap (kompensatorisch) + Desynchronisation → CSD (parallel). Beides sind Downstream-Effekte desselben Zustands, nicht Ursache und Wirkung. Die Sleep Inertia nach dem Nap kann den Prozess beschleunigen, ist aber nicht notwendig.

#### **B.11.1 Mechanistischer Pfad der Nap-Kaskade**

Der Nap regeneriert B7-Potential partiell. Das Outcome hängt davon ab, ob der regenerierte B7 sich mit B8 synchronisieren kann oder im aphasischen Fenster verbleibt (vgl. 4.7.1):

| Pre-Nap-Zustand | B7 nach Regeneration | B7-B8-Verhältnis | Outcome |
|:----------------|:--------------------|:-----------------|:--------|
| HR <75 (B7 depleted) | Aphasisch (feuert, aber inkohärent) | B7 stört B8-Takt, kann sich nicht synchronisieren | **Interferenz → CSD** (75% PPV bei <75, B.11) |
| HR ≥80 (B7 kohärent) | Kohärent (ausreichende Amplitude) | Resynchronisation mit B8 gelingt | **Kein CSD** (85% PPV bei ≥80, B.11) |

Der mechanistische Schlüssel ist die Qualität der Regeneration: Bei pre-Nap HR <75 ist B7 bereits so weit depleted (vesikulär, TPH2-limitiert, ATP-grenzwertig — vgl. 2.2.1), dass die partielle Regeneration im Nap nicht für Kohärenz reicht — der regenerierte B7 hat genug Kapazität um B8 zu stören, aber nicht genug um sich zu synchronisieren. Die Vesikelfreisetzung pro Spike ist stochastisch degradiert: Feuermuster erhalten, Transmitteroutput inkonsistent. Das ist das CSD-Fenster (4.7.1).

**LDX-Effekt:** LDX hält B7 intranukleär stabil → der regenerierte B7 nach dem Nap hat höhere Kohärenz → Resynchronisation mit B8 gelingt häufiger → Kaskadenrate sinkt von 58% (PRE) auf 11% (POST, B.11). LDX verschiebt nicht die HR-Schwelle, sondern die Regenerationsqualität.

#### **B.11.2 Post-exertionale Migräne als Nap-Kaskade mit autonomem Einstiegspfad**

Der Mechanismus der Nap-Kaskade ist identisch mit post-exertionaler Migräne — nur der Einstiegspfad unterscheidet sich:

| Einstiegspfad | Trigger für Ruhe | B7-Regeneration | Outcome |
|:--------------|:----------------|:----------------|:--------|
| **Schlafintrusion (normal)** | Kortikaler Off-State → Nap | Partiell | Aphasischer B7 gegen stabileren B8 → CSD |
| **ANS-Kollaps (post-exertional)** | Autonome Dekompensation → erzwungene Ruhe | Partiell | Identisch |

Post-exertionale Migräne ist kein eigener Triggerpfad — sie ist eine Nap-Kaskade mit autonomem statt kortikalem Einstieg. Der sympathische Maximaltakt während Sport verbraucht B7-Reserven; die anschließende Pause regeneriert B7 partiell; der aphasische B7 interferiert mit stabilem(erem) B8 → CSD. Nicht der Sport ist der Trigger, sondern die Transition danach.

**Einzelfallbeleg (07.04.2026, Anhang B.20):** Exertion (75 min, HR 155–170) → B7-Depletion → erzwungene Ruhephase (19:31–20:38, fixierte HR, SD <2, RMSSD <2) → partielle B7-Regeneration (21:00–22:26, B7 online aber instabil) → Kaskade (22:26–23:14, SD progressiv steigend auf 12.3, RMSSD auf 7.5 → aktive Interferenz). Die Pause hat gleichzeitig den ANS-Kollaps temporär gebremst UND die Voraussetzung für CSD geschaffen (B7-Potential wiederhergestellt → Interferenz mit B8 wieder möglich).

**Epidemiologische Stützung:** Koppen et al. (2013, J Headache Pain): 38% Lebenszeitprävalenz exercise-triggered Migräne, Onset durchschnittlich 160 min nach Belastungsende — konsistent mit dem Regenerations-Interferenz-Fenster.

---

### **B.12 Anfallstiming: Phasenmodell**

**Befund**

15 Anfälle (PRE) korrelieren nicht mit minimalem oder maximalem Slope, sondern mit der **ansteigenden Flanke** nach dem Drop-Minimum:

| Abstand zum letzten Drop-Minimum | Anfälle |
|:---------------------------------|:--------|
| 1 Tag | 4 |
| 2 Tage | 3 |
| 3–4 Tage | 3 |
| 5–7 Tage | 2 |

Median: 2 Tage nach dem Minimum.

**Mechanismus**

Am Minimum: Raphe-Tonus niedrigster, kortikale Fragmentierung maximal, aber System insgesamt gedämpft → kein Trigger. Beim Wiederanstieg: sympathischer Drive kommt zurück, aber kortikale Kohärenz noch nicht wiederhergestellt → Diskrepanz zwischen steigendem Arousal-Drive und fragmentiertem Kortex → CSD-Schwelle erreicht.

Der Anfall korreliert mit dDrop/dt (Änderungsrate), nicht mit Drop (Amplitude). **Phasenmodell**, nicht Schwellenmodell.

**Kompatibilität mit dem Stochastischen Fenstermodell**

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

**Absolute Schwellenwerte (periodengetrennt)**

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

#### **B.13.2 Post-Anfall-Verlauf**

Die CSD beeinflusst den autonomen Zyklus nicht:

| Richtung | n |
|:---------|:--|
| ↓ weiter fallend | 6 |
| ↑ Rebound | 9 |
| = gleich | 2 |

Keine systematische Richtung. Der Beat zieht unbeeindruckt seine Bahn. Die CSD resynchronisiert den Kortex (Post-Migräne-Klarheit, konsolidierter REM), aber der autonome Zyklus kümmert sich nicht darum. Dies differenziert zwei bisher vermengte Ebenen:

- **Kortikale Kohärenz** — wird durch CSD resynchronisiert. Belegt durch Traumerinnerung und Schlafkonsolidierung post-iktal.
- **Autonomer Zyklus** — läuft unabhängig, getrieben von der B7/B8-Schwebung. CSD greift nicht ein.

**Nap-Kreuzvalidierung**

Der Pre-Nap-HR-Befund (vgl. B.5) bestätigt sich als Zykluspositions-Indikator, nicht als Kausalfaktor:

- Pre-Nap HR ≥80 bpm = safe (85% PPV) → System ist früh im Zyklus, stabil.
- Pre-Nap HR <75 bpm = Kaskade → System ist auf der absteigenden Flanke, Anfall kommt unabhängig vom Nap.

Der Nap verändert den Zyklusverlauf nicht, er ist eine Projektion der aktuellen Zyklusposition.

**Algorithmische Qualitätsmerkmale**

Der Xiaomi-Algorithmus zeigt ein Konfidenz-Gating: bei atypischen Nachtprofilen (Triptan-Intervention, Tracker-Artefakte, Randdaten) gibt er HR_RESTING=0 statt eines unzuverlässigen Werts aus. Die Nicht-Null-Werte sind dadurch als algorithmisch valide eingestuft — das erhöht die Zuverlässigkeit der Deviation-Analyse.

Der Algorithmus ist nicht rekonstruierbar. Versuche, HR_RESTING aus nächtlichen HR-Perzentilen, Rolling-Minima oder Zeitfenstern vor dem Aufwachen abzuleiten, scheitern (maximale Korrelation r=0,31 bei keinem Modell). Der Algorithmus integriert vermutlich mehrere Faktoren (HR-Level, Stabilität, Bewegung, Schlafstadiendauer) auf eine Weise, die für uns nicht dekomponierbar ist. Der Output korreliert mit dem Systemzustand, der Mechanismus bleibt proprietär.

**Einordnung**

Der HR_RESTING-Befund ist eine unabhängige Kreuzvalidierung des Phasenmodells (B.12) über einen anderen Messkanal. Beide Metriken — der selbst berechnete Drop/τ und der proprietäre HR_RESTING — sind unterschiedliche Projektionen desselben Signals: der sympathovagalen Zyklusposition. Beide enthalten das Signal, beide verzerren es auf eigene Weise (unser Algorithmus bei Nicht-Sättigungskurven, der Xiaomi-Algorithmus bei atypischen Profilen). Die Konvergenz beider Metriken auf dasselbe Anfallsmuster stärkt den Befund.

Die Invarianz des autonomen Zyklus gegenüber der CSD ergibt sich direkt aus der Intertakt-Architektur: Die CSD adressiert den kortikalen Notfall (Resynchronisation über Zwangsdepolarisation) und kappt temporär den peripheren sympathischen Clamp (§2.5.1.1), aber die defekte 5-HT1A-Resensitisierungskinetik am B7 bleibt unverändert. Der B7-Intertakt-Drift beginnt unmittelbar postiktal wieder von der neuen Ausgangslage aus — der Beat zieht unbeeindruckt seine Bahn, weil sein Treiber nicht adressiert wurde.

#### **B.13.3 Evidenztabelle**

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

**Drei-Phasen-Verlauf**

| Phase | Zeitraum | Bedingung | Density (Ep./h) | Dauer |
|:------|:---------|:----------|:-----------------|:------|
| 1: Hauptschlaf | Nacht 30.03 | Migräne-Prodrom, kein Triptan | **2,8** | regulär |
| 2: Schlafversuch | Früh 31.03 | Schmerz, ohne Medikation | **5,3** | 57 min |
| 3: Post-Sumatriptan | Nach Einnahme | Sumatriptan, Schmerz blockiert | variabel | ~9 h |

Phase 1 zeigt eine vergleichsweise konsolidierte Nacht (2,8/h — niedriger als POST-Mean). Phase 2 dokumentiert einen Schlafversuch unter unbehandeltem Migräneschmerz: In nur 57 Minuten erreicht die Density 5,3/h — der Schmerz fragmentiert den Schlaf massiv. Phase 3 beginnt nach Sumatriptan-Einnahme.

**Post-Sumatriptan Drei-Drittel-Analyse**

Die Post-Sumatriptan-Phase wurde in Drittel unterteilt, um den zeitlichen Verlauf der Resynchronisation zu erfassen:

| Drittel | Density (Ep./h) | Interpretation |
|:--------|:-----------------|:---------------|
| Erstes Drittel | **6,1** | Residuale Fragmentierung, Schmerz blockiert aber CSD-Kaskade noch aktiv |
| Zweites Drittel | **7,5** | Maximum — paradoxe Verschlechterung, möglicherweise Rebound der Desynchronisation |
| Drittes Drittel | **5,8** | Beginn der Resynchronisation |

Das Muster zeigt keine monotone Konsolidierung, sondern eine invertierte U-Kurve mit einem Fragmentierungsmaximum im zweiten Drittel.

**HR-Verlauf als zweiter physiologischer Kanal**

| Phase | HR (bpm) | Interpretation |
|:------|:---------|:---------------|
| Hauptschlaf (Nacht) bis ~23:20 Uhr | 75,7 | Erhöht — sympathische Aktivierung durch Prodrom |
| Tiefster Punkt (Deep), 0-1 Uhr | 61,2 | Vagale Kapazität intakt, aber kurzzeitig |
| Post-Sumatriptan (früh), 1-4 Uhr | 70–73 | Schmerz blockiert, sympathische Restaktivierung |
| Post-Sumatriptan (spät) nach 4 Uhr | 63–65 | Autonome Beruhigung, Resynchronisation |

Die HR konvergiert erst 3–4 Stunden nach Sumatriptan-Einnahme auf normale Schlafwerte. Dies definiert ein Resynchronisationsfenster: Sumatriptan blockiert den Schmerz und ermöglicht Schlaf, aber die kortikale und autonome Resynchronisation benötigt 3–4 Stunden.

![HR und Schlafphasen der Nacht](<images/Metabase-HR + AVG-6.4.2026, 10_16_53.png>){width=66%}
*Schlafphasen: 4 = Wach, 2 = Leichtschlaf, 1 = REM, 0 = Tiefschlaf

#### **B.15.1 Interpretation**

Sumatriptan unterbricht die Schmerzkaskade (5-HT₁B/D-Agonismus → präsynaptische Hemmung der trigeminalen Transmitterfreisetzung → Schmerzblockade; vgl. 4.4.3), adressiert aber nicht die kortikale Desynchronisation. Die CSD ist bereits gelaufen; das Sumatriptan ermöglicht lediglich Schlaf als Medium der Resynchronisation. Die 3–4 Stunden bis zur autonomen Normalisierung entsprechen der Dauer, die der Kortex benötigt, um post-CSD über SWS-Zyklen globale Kohärenz wiederherzustellen.

**Konsistenz mit B.6:** Der Hauptschlaf vor dem Anfall (Phase 1: 2,8/h) war konsolidiert — die Fragmentierung der Vornächte (vgl. B.6.2, t-1 Lag) hatte sich bereits in den Anfall entladen. Post-Sumatriptan beginnt die Resynchronisation von einem post-iktalen Ausgangszustand.

**Caveat:** Einzelereignis. Die Drei-Drittel-Analyse ist deskriptiv und nicht generalisierbar. Die HR-Verlaufsdaten sind durch die Sumatriptan-Pharmakokinetik (Halbwertszeit ~2h) konfundiert.

---

### **B.16 Sonderanalyse: Post-exertionaler Anfall 07.04.2026 — ANS-Kollaps als eigenständiger Prozess**

Der Anfall vom 07.04.2026 liefert eine zeitliche Dissoziation zwischen ANS-Kollaps und kortikaler CSD-Kaskade, die in früheren Anfällen nicht beobachtbar war. Die LDX-bedingte Verzögerung der CSD-Schwellenunterschreitung machte die ANS-Symptome als eigenständigen, vorgelagerten Prozess sichtbar.

**Zeitlicher Verlauf**

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
| 9: Triptan-Plateau | 00:25–03:20 | 80–89 | Sumatriptan-Wirkplateau (trigeminale Transmitterhemmung + sekundäre Vasokonstriktion), HR-Plateau ~82 bpm, keine Konsolidierung |
| 10: Echtes Nadir | 04:45–06:45 | 58–67 | HR-Minimum 58 bpm (04:55), zweites Minimum 59 bpm (05:37) |
| 11: Morgen | 07:00–08:00 | 70–84 | Aufwachen, rechtsseitiger Nystagmus |

**Schlafarchitektur (Tracker-Klassifikation)**

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

**Dreifach-Konvergenz als Trigger**

Der Anfall entstand durch die zeitliche Konvergenz dreier Kompensationsentzüge:

| Faktor | Zeitpunkt | Mechanismus |
|:-------|:----------|:------------|
| Post-exertionale B7-Depletion (vesikulär + TPH2-limitiert, vgl. 2.2.1) | ab 17:46 | Sympathischer Drive maskierte Raphe-Insuffizienz; Maskierung fällt mit Belastungsende weg |
| LDX-Abklingen | ab ~18:00 | Wirkdauer 10–12 h, Einnahme morgens → abends insuffizient |
| SCN-Abendsignal | ab ~19:00 | Normales Herunterfahrsignal via SCN→B8→B7; trifft auf bereits depletierten B7 |

Jeder einzelne Faktor wäre kompensierbar gewesen. Die Dreifach-Konvergenz war es nicht.

**Befund: ANS-Kollaps als eigenständiger Prozess**

Die zentrale Beobachtung: ANS-Symptome (vestibuläre Instabilität, Schwindel, Hitzewellen, Kältewellen, Zittern, Kreislaufinstabilität) traten ab 18:39 auf — **3,5 Stunden vor der vollen CSD-Kaskade** (22:26).

| Merkmal | ANS-Kollaps | Kortikale CSD-Kaskade |
|:--------|:------------|:---------------------|
| Onset | 18:39 (Beifahrersitz) | 22:26 (volle Eskalation) |
| Latenz nach Exertion | ~55 min | ~4,5 h |
| Architektonische Distanz zu B7 | Monosynaptisch (NTS, RVLM, Ncl. ambiguus) | Polysynaptisch (thalamokortikale Schleife) |
| Kompensierbarkeit | PFC→NTS-Atemkontrolle (temporär wirksam) | Keine willentliche Kompensation |
| Zeitkonstante | Schnell in der Auslösung, lang im Verlauf | Langsam in der Auslösung, schnell im Verlauf |

**Interpretation:** Was klinisch als „Stammhirnaura" beschrieben wird, ist kein CSD-Propagationsphänomen im Hirnstamm, sondern ein eigenständiger B7→ANS-Kern-Kollaps. Ohne LDX überlagern sich beide Prozesse zeitlich und sind klinisch nicht trennbar. LDX erzeugte unbeabsichtigt eine diagnostische Separation, indem es die CSD-Schwelle länger hielt, während der ANS-Kollaps ungehindert ablief.

**PFC→NTS-Kompensation und deren Erschöpfung**

Die bewusste Atemkontrolle (langsames Ausatmen gegen autonome Reflexe) war effektiv gegen:
- Vestibuläre Instabilität (Schwindel reduziert)
- Übelkeit (gebremst)
- Hitzewellen (unterdrückt)

Die Kompensation nutzt den PFC→NTS-Pfad — willentliche Top-down-Kontrolle über autonome Kerne. Dieser Pfad wird gleichzeitig durch dieselben Faktoren destabilisiert, die den ANS-Kollaps treiben (LDX-Abklingen, B7-Depletion). Die Kompensation verbraucht die Ressource, die sie zu ersetzen versucht.

Empirischer Beleg: Aktives Fahren (Phase 3, hoher PFC-Demand) → NTS-Suppression erfolgreich trotz extremer Triggerbelastung. Beifahrersitz (Phase 4, kein PFC-Demand) → Dekompensation innerhalb von Minuten.

**Triptan-Pharmakokinetik im HR**

| Phase | Zeitraum | HR (bpm) | Mechanismus |
|:------|:---------|:---------|:------------|
| Pre-Triptan Nadir | 22:20 | 67 | Maximaler vagaler Tonus bei ANS-Erschöpfung |
| ANS-Spike | 22:26–23:10 | 67→104 | Volle Kaskade: CSD + Erbrechen |
| Initialer Triptan-Effekt | 23:10–23:40 | 104→69 | Schmerzblockade → sympathische Deaktivierung |
| Triptan-Rebound | 00:25–03:20 | 80–89 | 5-HT1B/1D-Wirkplateau (Transmitterhemmung + sekundäre Vasokonstriktion) → sympathische Restaktivierung |
| Post-Triptan-Clearance | 04:45–06:45 | 58–67 | Sumatriptan-HWZ ~2h; erst nach Clearance echtes Nadir |

Das Triptan-Plateau (HR ~82 bpm über ~3 Stunden) ist konsistent mit B.15: Die Resynchronisationszeit beträgt 3–4 Stunden, und das Triptan konfundiert den HR-Verlauf über seine Halbwertszeit. Das echte Nadir (58 bpm) tritt erst nach Triptan-Clearance auf — ähnlich wie in B.15.

**Differenz zu B.15:** In B.15 lag der Post-Sumatriptan-HR bei 70–73 bpm (Phase 3), hier bei 80–89. Die Differenz erklärt sich durch die exertionale Vorbelastung: Die sympathische Restaktivierung durch die post-exertionale Depletion addiert sich zum Triptan-Wirkplateau (Transmitterhemmung + sekundäre Vasokonstriktion).

**Konsistente Nystagmus-Lateralisierung**

Am Morgen nach dem Anfall: Nystagmus rechtsseitig. Konsistent mit früheren Anfällen (immer rechts). Zwei Hypothesen:

| Hypothese | Mechanismus | Vorhersage |
|:----------|:------------|:-----------|
| Architektonisch | Asymmetrische B7-Innervierung vestibulärer Kerne; eine Seite hat weniger Reservekapazität | Fixe Lateralisierung unabhängig von CSD-Hemisphäre |
| Funktionell | CSD-Propagation bevorzugt eine Hemisphäre; kontralaterale vestibuläre Manifestation | Lateralisierung könnte bei atypischen CSD-Pfaden wechseln |

Die Konsistenz über multiple Anfälle spricht für die architektonische Variante.

**Evidenztabelle**

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

**Modellimplikation**

Die temporale Dissoziation erzwingt eine Korrektur: Was als „Stammhirnaura" (MBA) klassifiziert wird, ist kein CSD-Propagationsphänomen, sondern ein eigenständiger B7→ANS-Kern-Kollaps. Die Implikationen:

1. **Architektonische Priorität:** ANS-Kerne liegen monosynaptisch an B7 — sie destabilisieren vor dem polysynaptischen thalamokortikalen Pfad. Die Sequenz ist architektonisch determiniert, nicht stochastisch.
2. **Maskierung ohne LDX:** Ohne LDX eskaliert CSD schneller → ANS-Kollaps und CSD überlagern sich zeitlich → klinisch als einheitliche „Aura" fehlinterpretiert.
3. **Brainstem-CSD beim Menschen:** Keine humane Evidenz. Die einzige Grundlage ist das Cacna1a-S218L-Mausmodell (van den Maagdenberg et al.). Die ANS-Kollaps-Reattribution eliminiert die Notwendigkeit dieser unbelegten Hilfshypothese.
4. **Parsimoniegewinn:** Sämtliche MBA-Symptome folgen aus der architektonischen Proximität der ANS-Kerne zum Raphe-System — ein Mechanismus, der aus dem B7/B8-Interferenzmodell direkt ableitbar ist.

**Caveat:** Einzelereignis. Die temporale Dissoziation war nur durch die spezifische Konstellation (exertionale Vorbelastung + LDX-Abklingen) beobachtbar. Reproduzierbarkeit nicht gesichert — allerdings spricht die konsistente Nystagmus-Lateralisierung über multiple Anfälle für ein architektonisch stabiles Muster.

![HR-Timeline Anfall 07.04.2026](<images/B20_hr_timeline_20260407.png>)
*HR-Minutenauflösung, CEST. Annotationen: Rasenmähen (rot), Interventionen (gestrichelt), Kaskade (rot), Triptan-Plateau (amber), echtes Nadir (grün).*

![HR-Sleep-Timeline Schlaf 07.04.2026](<images/Metabase-HR + AVG-4_8_2026, 11_23_07 AM.png>)

---

### Einzeltaganalyse: 11./12. April 2026 — B8-Haltemodus und paradoxe LDX-Schlafvertiefung

**Tagesablauf**
- **13:40–20:40**: Mäßige Gartenarbeit. HR-Durchschnitt 109 bpm (77–143), physiologisch unauffällig.
- **20:40–22:28**: Vor dem Fernseher eingeschlafen. HR sinkt auf MHR10 ~77 (TV-Nap). Dies ist eine ungeplante Schlafphase — möglicherweise der Punkt, an dem der B7 kurz regeneriert.
- **22:28–22:48**: Kurz wach, Geschirr aus dem Garten geholt.
- **22:48**: Ins Bett gelegt. Einseitiges Ziehen im Kopf bemerkt, linksseitig. Kein vollständiges CSD-Bild, eher ein Druckgefühl, vergleichbar mit früheren Prä-CSD-Episoden. Vergleichbar mit retrobulbärem Schmerz, keine ANS-Symptome (kein Schwitzen, keine Übelkeit, keine kardiovaskuläre Dysregulation).
- **23:50**: 3 mg LDX vorsorglich eingenommen — Hypothese: B8-Instabilität als CSD-Vorstufe, LDX zur Stabilisierung.
- **23:50–07:20**: Gesamte Nacht mit einseitigem Kopfschmerz durchgeschlafen. Der Schmerz persistierte konstant, eskalierte aber nicht und ging auch nicht weg. Schlaf war möglich, aber nicht erholsam.
- **07:20**: Regulär aufgestanden.
- **07:30**: 7,5 mg LDX + Riboflavin (B2) + 300 mg Ibuprofen eingenommen. Anschließend in den Garten gelegt.
- **07:40–10:00**: 2,5 Stunden tiefer, klarer Schlaf im Garten. Aufgewacht mit deutlich reduziertem Kopfschmerz und subjektivem Erholungsgefühl. Kein groggy Aufwachen, sondern klares, natürliches Ende.

**Phänomenologie**
- Einseitiger Druck links, kein Vollbild-CSD, keine Aura, keine ANS-Beteiligung.
- Persistenz über die gesamte Nacht: weder Eskalation noch Remission.
- Clearance erst im Morgenschlaf unter höherer LDX-Dosis + IBU.
- Subjektiv: Der Nachtschlaf war „durchgehalten", der Morgenschlaf war „regenerativ".

**HR-Daten**

**Nacht (23:50–07:20)**
- MHR10-Range: 57,1–79,0 bpm, Mittel 64,4
- HR-Std: 5,8 bpm
- ~20 Nadirs detektiert, Modulation vorhanden
- **Nadir-Slope flach**: Die physiologische nächtliche HR-Absenkung bleibt aus. Die Nadirs sinken nicht progressiv über die Nacht.
- **Baseline relativ hoch**: MHR10-Mittel 64,4 liegt über dem typischen Tiefschlafbereich.

**Morgen-Schlaf unter LDX (07:40–10:00)**
- MHR10 sinkt auf **49,2 bpm** — der tiefste Wert der gesamten Aufzeichnung.
- Ab ~08:15 stabilisiert sich ein extrem flaches Plateau bei ~52 bpm über 90 Minuten.
- Dies geschieht **unter Einfluss von 7,5 mg LDX**, das normalerweise sympathikoton wirkt und die HR erhöht.
- Klares, natürliches Aufwachen nach 2,5 Stunden.

**Kontrast Nacht vs. Morgen**
| Parameter | Nacht | Morgen-Schlaf |
|-----------|-------|---------------|
| MHR10 Minimum | 57,1 | 49,2 |
| MHR10 Mittel | 64,4 | 58,2 |
| Dauer | 447 min | ~140 min |
| Subjektiv | nicht erholsam | klar, erholsam |
| Kopfschmerz | persistierend | rückläufig |
| LDX-Dosis | 3 mg | 7,5 mg |
| Zusätzlich | — | 300 mg IBU |

**Hypothesen**

**Ausgangsvermutung am Abend**
Nach dem TV-Nap entsteht das Ziehen — Verdacht auf CSD-Vorstufe im Okzipitallappen, verwandt mit retrobulbärem Schmerz. Hypothese: B7 hat sich im Nap regeneriert, aber B8 nicht. Die CSD-Vorstufe ist ein B8-Problem, nicht ein B7-Problem. Daher LDX als B8-Stabilisierung.

**Rekonstruktion am Morgen danach**
- Der B7 war über die Nacht funktional — Modulation (Nadirs, Phasen) war vorhanden. Die ANS-Seite war stabil, keine ANS-Symptome.
- Der B8 war das isolierte Problem: CSD-Aktivität ohne ANS-Beteiligung.
- Die 3 mg LDX haben den B7-Arm bedient (ANS-Eskalation verhindert), aber den B8-getriebenen Schmerz nicht durchbrochen.
- Erst 7,5 mg LDX + IBU am Morgen hatten genug Wirkbreite für die B8-Seite.

**Datenanalyse und Schlussfolgerungen**

**B7/B8-Differenzierung über HR**
Die HR-Daten ermöglichen eine Trennung der beiden Systeme:

- **B7-Marker**: Nadir-Modulation (Existenz, Regelmäßigkeit, Slope). In dieser Nacht: B7 aktiv, aber ohne Konsolidierungstrend.
- **B8-Marker (indirekt)**: Hohe, nicht absinkende Baseline trotz funktionalem B7. Die Differenz zwischen „Modulation vorhanden" und „Baseline sinkt nicht" deutet auf einen externen Override — der B8 hält das System oben.

**B8-Haltemodus als Schutzreaktion**
Der CSD-Schmerzreiz erzeugt einen Feedback-Loop:

1. CSD → Schmerzreiz → Kortex meldet Aktivität
2. B8/MRN bleibt aktiv als Schutzreaktion (serotonerge Versorgung des betroffenen Areals)
3. B8-Aktivität verhindert Clearance (System kommt nicht tief genug)
4. CSD persistiert → Schmerz bleibt → zurück zu Schritt 2

Dieser Loop erklärt die Persistenz des Schmerzes über die gesamte Nacht: Er eskaliert nicht (B7 ist stabil, LDX verhindert ANS-Kaskade), aber er geht auch nicht weg (B8 lässt nicht los, solange der Reiz besteht).

**Clearance-Bedingungen**
Die Auflösung am Morgen erforderte das Durchbrechen des Loops an zwei Stellen gleichzeitig:

- **IBU**: Reduziert den Schmerzreiz (Entzündungskomponente der CSD) → B8 verliert seinen Grund, im Haltemodus zu bleiben.
- **7,5 mg LDX**: Stabilisiert den B8 direkt → ermöglicht kontrollierten Rückzug statt Haltemodus.
- **Ergebnis**: B8 kann abschalten → B7 übernimmt → parasympathische Konsolidierung → MHR10 sinkt auf 49,2 bpm → Clearance.

**Paradoxe Medikamentenreaktion**
Die MHR10 von 49,2 bpm unter 7,5 mg LDX ist pharmakologisch paradox: LDX (Lisdexamfetamin) ist ein Sympathomimetikum, das über Dopamin- und Noradrenalin-Freisetzung die HR typischerweise erhöht.

Die Auflösung liegt im Modell:
- LDX stabilisiert den B8 → B8 lässt los → B7 kann ungehindert konsolidieren.
- Die 5-HT-vermittelte parasympathische Dominanz des B7 überschreibt die sympathomimetische Wirkung des LDX vollständig.
- Das ist kein Versagen der Medikamentenwirkung, sondern eine **Entlarvung der eigentlichen Achse**: Die sympathomimetische Wirkung von LDX ist schwächer als die serotonerge Konsolidierungskraft eines funktionalen B7, der endlich freie Bahn hat.

Dies erklärt auch die generelle Beobachtung, dass LDX den Schlaf nicht stört: Wenn der B8-Arm stabilisiert wird und der B7 konsolidieren kann, *verbessert* LDX den Schlaf — nicht trotz, sondern wegen seiner Wirkung.

**Koffein-Parallele**
In seltenen, nie reproduzierbaren Fällen hat Koffein denselben paradoxen Effekt gezeigt: tiefer, erholsamer Schlaf nach Koffein-Einnahme. Der Mechanismus wäre analog — Koffein stabilisiert in diesen Fällen den B8 (Adenosin-Antagonismus an serotonergen Neuronen), der B8 kann loslassen, B7 konsolidiert.

Die fehlende Reproduzierbarkeit bei Koffein gegenüber der relativen Zuverlässigkeit bei LDX erklärt sich durch die Wirkmechanismen: Koffein wirkt über Adenosin-Rezeptoren unspezifisch an vielen Systemen gleichzeitig, LDX über die Dopamin/Noradrenalin-Achse gezielter am B8. Koffein trifft den B8 nur manchmal (abhängig vom Ausgangszustand), LDX zuverlässiger.

**Implikationen**

**Therapeutische Umkehr: Abend-LDX statt Morgen-LDX**
Die Daten legen eine Inversion des bisherigen Dosierungsschemas nahe:

- **Bisher**: LDX morgens für den Tag, DPH abends für die Nacht (B7-Suppression).
- **Neu**: LDX abends zur B8-Stabilisierung in der Nacht, Morgendosis als Erhaltung.

Die Nacht ist nicht der Zeitraum, in dem der B7 supprimiert werden muss, sondern der Zeitraum, in dem der B8 loslassen muss. LDX ermöglicht beides: B8-Stabilisierung (direkter Effekt) → B7-Konsolidierung (indirekter Effekt durch Wegfall des B8-Override).

**Testbares Vorhersagemodell**
Abend-LDX an alternierenden Nächten im ON/OFF-Design. Messbare Endpunkte:

- **Clearance-Marker**: MHR10-Minimum im letzten Schlafdrittel (tiefer = bessere Konsolidierung)
- **Nadir-Slope**: Sollte unter Abend-LDX steiler negativ werden (B7 kann progressiv absenken)
- **Morgen-Baseline**: Sollte tiefer liegen als ohne Abend-LDX

**Abgrenzung zum DPH-Protokoll**
DPH supprimiert den B7 direkt → die Instabilität wird ausgeschaltet, aber auch die Konsolidierung. LDX stabilisiert den B8 → der B7 wird nicht ausgeschaltet, sondern *befreit*. Das ist der Unterschied zwischen Suppression und Ermöglichung.

**Einordnung**

Dieser Tag zeigt erstmals eine klare phänomenologische und datengestützte Trennung von B7- und B8-Beiträgen innerhalb einer einzelnen Episode:

- B7 funktional (Modulation vorhanden, keine ANS-Symptome)
- B8 im Haltemodus (CSD-Persistenz ohne Eskalation)
- Clearance erst nach B8-Freigabe (IBU + höheres LDX)
- HR-Signatur der Clearance: paradoxer Tiefschlaf unter Sympathomimetikum

Die bisherigen Einzeltaganalysen in Anhang B zeigen überwiegend kombinierte B7/B8-Ausfälle. Dieser Fall ist insofern ein Sonderfall, als die beiden Systeme dissoziiert auftreten — und genau diese Dissoziation macht die jeweiligen Beiträge sichtbar.

####Antagonistische Kopplung und zirkadiane Konsequenzen

**Zwei-Pfad-Konvergenz des Anfalls**

Aus der B7/B8-Differenzierung dieser Episode ergibt sich eine erweiterte Anfallsarchitektur: Der Anfall hat zwei unabhängige Eskalationspfade — B7 (DRN→Sympathikus→thalamische Afferenz) und B8 (MRN→Kortex→thalamische Efferenz) — die im Vollbild konvergieren, aber in der Prodromalphase getrennt auftreten können.

Die Episode vom 11./12. April zeigt ein B8-dominantes Prodrom: CSD-Vorstufe (einseitiger Druck) ohne ANS-Beteiligung. Die Symptome, die im Verlauf zusammenfallen, sind in der Frühphase differenzierbar. Diese Differenzierung ist therapeutisch entscheidend — eine reine B7-Intervention (3 mg LDX) reicht bei B8-dominantem Prodrom nicht aus.

**Destabilisierungskaskade über gemeinsame Downstream-Komponenten**

Die bisherige Modellannahme war: B7 und B8 desynchronisieren als phasengekoppelte Oszillatoren, ihre direkte Phasenverschiebung treibt den Anfall. Die Korrektur: Sie wirken nicht direkt aufeinander, sondern destabilisieren jeweils eine gemeinsame Komponente ihrer Feedback-Schleifen.

- **B7-Pfad**: DRN-Instabilität → Sympathikus-Destabilisierung → thalamische Afferenz gestört (der Thalamus braucht stabile autonome Eingänge für seine Gating-Funktion)
- **B8-Pfad**: MRN-Instabilität → kortikale Modulation instabil → thalamische Efferenz gestört (der Thalamus bekommt inkohärente Rückmeldung vom Kortex)

Der Thalamus ist die Konvergenzstelle, die von beiden Seiten destabilisiert wird — aber über verschiedene Eingänge.

**CSD-Lokalisation als thalamokortikale Konsequenz**

Der destabilisierte Thalamus projiziert über Pulvinar und LGN primär in den Okzipitallappen — dort konvergiert die thalamische Destabilisierung mit der B8-Intratakt-Störung zuerst. Die CSD beginnt okzipital nicht, weil der visuelle Kortex intrinsisch die niedrigste Erregungsschwelle hat, sondern weil er der Ort ist, an dem die B8-Modulation der äußeren kortikalen Schichten (MRN-Territorium) und das thalamische Eingangs-Gating zuerst gemeinsam versagen.

Die Lateralisierung des Symptoms (einseitig links) wäre dann die Lateralisierung des thalamischen Gating-Defizits — nicht die CSD selbst ist lateralisiert, sondern die thalamische Projektion, die sie triggert. Das wäre eine MRT-Vorhersage: Asymmetrischer Befund im Pulvinar/LGN, falls der autoimmune Schaden lateralisiert ist.

**Direkte antagonistische Kopplung von DRN und MRN**

**Literatur [gesichert]**
- MRN-Neurone feuern spontan bei ~0,56 Hz, DRN-Neurone bei ~1,35 Hz — unterschiedliche Taktbereiche.
- MRN und DRN verarbeiten Belohnungs- und Aversionsreize in entgegengesetzter Richtung: DRN signalisiert Belohnung, MRN signalisiert Aversion. Sie sind funktionale Antagonisten.
- DRN-Stimulation erzeugt 5-HT-Freisetzung im SCN, obwohl nur der MRN direkt zum SCN projiziert → multisynaptische DRN→MRN→SCN-Route.
- Die afferente Steuerung ist fundamental verschieden: DRN wird primär über GABA-Disinhibition gesteuert, MRN über glutamatergen exzitatorischen Antrieb.

**Konsequenz für das Modell [hypothetisch — modellspezifisch]**
Die antagonistische Funktion setzt DRN und MRN in eine direkte Kopplung, die nicht über den Thalamus oder Kortex läuft, sondern über die Belohnungs-/Aversions-Balance selbst:

1. **Phantomkompensation**: Wenn der B7 (DRN) durch autoimmunen Schaden phasisch ausfällt, fehlt das Belohnungssignal. Der B8 (MRN) interpretiert dies als Bedarf an erhöhter Aversions-/Wachsamkeitssignalisierung und kompensiert hoch. Aber er kompensiert gegen einen Defekt, nicht gegen einen physiologischen Zustand — chronische Gegensteuerung gegen ein Phantom.

2. **Restart-Kollision**: Wenn der B7 nach dem Kollaps wieder anspringt, trifft das zurückkehrende Belohnungssignal auf einen noch hochgefahrenen B8 im Kompensationsmodus. Beide drücken gleichzeitig in ihre jeweilige Richtung — aktive Gegensteuerung statt physiologisches Alternieren.

3. **Erschöpfungszyklus**: Der B8 hält die Überkompensation tagelang durch, erschöpft sich, fällt aus (HR: flaches hohes Plateau = ANS-Eigendynamik ohne B8-Modulation), regeneriert, springt wieder an — und trifft auf einen ebenfalls regenerierenden B7. Zwei frisch gestartete Antagonisten mit instabilen Taktgebern, die sofort in Überkompensation verfallen. Das ist der Trigger-Moment.

**Demaskierung des zirkadianen Shifts [hypothetisch — modellspezifisch]**

**Bisherige Annahme**
Der zirkadiane Shift liegt bei ~26h als primärer SCN-Defekt. Die Schwebung entsteht aus der Differenz 26h (SCN) gegen 24h (Licht/Dunkel-Zeitgeber).

**Revision**
Der SCN selbst ist möglicherweise intakt bei ~24h. Der scheinbare 26h-Shift ist das Mittel einer **asymmetrischen Spreizung**, die durch die instabile antagonistische Kopplung erzeugt wird:

- B7-Dominanz (B8 erschöpft): DRN→MRN→SCN verschiebt die Phase in eine Richtung
- B8-Dominanz (B7 erschöpft): MRN→SCN verschiebt die Phase in die andere Richtung
- Der gemessene Mittelwert liegt bei ~26h, aber Einzelzyklen schwanken (25h, 27h, nahe 24h bei Balance)

Die ~4–7-Tage-Periodizität der Anfälle ist dann nicht die Schwebungsfrequenz zweier fester Oszillatoren (26h vs. 24h), sondern die **Erschöpfungsperiodik der antagonistischen Kopplung** selbst: Kompensation → Erschöpfung → Ausfall → Regeneration → Restart → Überkompensation. Der SCN wird von diesem Zyklus rhythmisch hin- und hergeschoben.

**Erklärungsgewinn**
Diese Revision erklärt zwei bisher problematische Beobachtungen:

1. **Variable Periodizität**: Ein fester 26h-Oszillator würde eine stabile Schwebungsfrequenz erzeugen (~6 Tage). Die tatsächliche Anfallsperiodizität variiert zwischen 3 und 8 Tagen. Die Erschöpfungsdynamik hängt von Zustandsvariablen ab (Schlafqualität, Belastung, Medikation), was die Variabilität erklärt.

2. **Bidirektionaler Chronotyp-Drift**: Wenn der Shift ein fester 26h-Takt wäre, würde der Chronotyp monoton nach spät driften. Tatsächlich oszilliert er — mal Spätverschiebung, mal Frühverschiebung. Das passt zu einer Spreizung, nicht zu einem festen Offset.

**Testbarkeit**
Die Chronotyp-Verschiebung sollte mit dem Erschöpfungszustand der Antagonisten korrelieren: In B7-dominanten Phasen (steep nadir slope, gute Konsolidierung) Frühverschiebung, in B8-dominanten Phasen (flacher slope, hohe Plateaus) Spätverschiebung. Die HR-Plateau-Analyse liefert die nötigen Proxy-Variablen für beide Zustände.


---

### **B.18 Evidenztabelle**

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
| POST-Ausreißer 28.03: 8,99/h Density, 61 Transitionen (POST-Maximum in PRE-Territorium) | Einzelbeobachtung, große Effektstärke | Tracker-Daten, B.3.2 |
| ~4-Tage-Oszillator unabhängig von Medikation | Hypothetisch, konsistent mit 28.03-Muster | B.3.2, Longitudinaldaten |
| Vornacht-Density → Folgetag-Anfall: r=+0,392, p≈0,003 (n=56) | Statistisch signifikant | Tracker-Daten + Anfallskalender, B.6.2 |
| Anfall-Nacht selbst: r=−0,065 (kein Signal) | Nicht signifikant | B.6.2 (Kontrollbedingung) |
| Density ≥7,0/h → Anfall am Folgetag in 83% (5/6) | Deskriptiv, kleine Stichprobe (n=6) | B.6.2 |
| POST-Nap-Reset erfolgreicher als PRE (78% vs. 38%) | Deskriptiv | Tracker-Daten, B.5.1 |
| Dreiersequenz (Fragm. Nacht → Nap → Anfall): 75% | Deskriptiv, n=8 | B.5.1 |
| Migräne-Nacht 30./31.03: Sumatriptan → 3–4h Resynchronisation (HR 75→63 bpm) | Einzelbeobachtung | HR-Daten, B.15 |
| Post-Sumatriptan Density: invertierte U-Kurve (6,1→7,5→5,8/h) | Deskriptiv, Einzelereignis | B.15 |
| HR-Drop-Periodizität 7,5 Tage (FFT, Power 102,5) | Statistisch signifikant (n=60 Nächte) | Tracker-Daten, FFT-Analyse (B.10) |
| Autokorrelation Lag 7 (r=0,317) und Lag 14 (r=0,213) | Statistisch signifikant | Tracker-Daten, Autokorrelation (B.10) |
| Nap-Outcome durch Pre-Nap-HR determiniert (PPV 85% bei ≥80 bpm) | Statistisch signifikant (n=33) | Tracker-Daten, HR-Analyse (B.11) |
| Anfall auf ansteigender Flanke, Median 2 Tage nach Minimum | Deskriptiv (n=15) | Tracker-Daten + Anfallskalender (B.12) |
| PRE/POST HR-Trajectory-Verteilung identisch (61% vs. 56% linear) | Deskriptiv | Tracker-Daten (B.9) |
| Ganznacht-Slope = temporale Ausschmierung räumlich fragmentierter SWS | Modellinterpretation, konvergent mit B.2–B.3 | Abgeleitet aus HR-Trajectory + Fragmentierungsdaten (B.9.1) |
| Gesundes Muster: erster NREM-Zyklus leistet gesamten sympathischen Rundown in 60–90 min | Literaturgestützt | Brandenberger et al. 1994, Boudreau et al. 2013 (B.9.2) |
| Linearer Ganznacht-Slope in keiner Quelle als Normvariante beschrieben | Literaturgestützt | Übersicht B.9.2 |
| POST-Nap-Kaskadenrate 11% vs. PRE 58% | Deskriptiv | Tracker-Daten (B.11) |
| SWS-Fragmentierung als Mediator orthographischer Engramm-Instabilität (LRS-Phänotyp) | Modellvorhersage | Abgeleitet aus Anhang D, D.7.2 — orthographische Konsolidierung SWS-abhängig |
| HR_RESTING als unabhängiger Zyklusmarker (Elevation d-1/d-2, Drop am Anfallstag) | Deskriptiv, kreuzvalidiert | B.13, `cortical_coherence_proxy_analysis - HR Resting.csv` |
| CSD resynchronisiert Kortex, nicht autonomen Zyklus | Modellinterpretation, konsistent mit Daten | B.13.2 |
| Anfalls-Schwelle relativ zur individuellen HR-Range, nicht absolut | Deskriptiv | B.13 |

### **B.18 Revisionstabelle**

| Kapitel | Revision | Priorität |
|:--------|:---------|:----------|
| **4.5** (CSD als Reset) | Differenzierung ergänzen: CSD resynchronisiert kortikale Kohärenz, aber nicht den autonomen Zyklus. Der Beat läuft unbeeindruckt weiter. Verweis auf B.13.2. | Mittel — Präzisierung, kein Widerspruch |

### **B.19 Limitationen**

- Consumer-Tracker, keine PSG-Validierung. Die Stadienklassifikation ist intern und nicht reproduzierbar.
- n=1, kein Kontrolldesign. Die Perioden-Trennung (PRE/POST) ist konfundiert mit Medikamentenwechsel, Jahreszeit und 13-monatiger Trageunterbrechung.
- POST-Stichprobe klein (18 Nächte). Deep-Fragmentierungsratio erreicht p=0,07 — Power-Problem bei klarer Effektrichtung.
- HR-Variabilität als Validierungsebene durch Betablocker-Confounder eliminiert.
- Die Interpretation des Trackers als „stochastischer Resonanz-Detektor" ist messtheoretisch konsistent, aber nicht extern validiert. Eine PSG-Parallelmessung wäre nötig, um die Tracker-Fragmentierung gegen globale SWA zu kalibrieren.
- Die CSD-als-Resynchronisation-These ist mechanistisch konsistent und erklärt den klinischen Verlauf, aber nicht direkt testbar ohne iktale EEG-Aufzeichnung mit post-iktaler Schlafarchitektur-Analyse.
- Die t-1 Lag-Korrelation (B.6.2) basiert auf n=14 Vornächten vor Anfällen. Drei hochfragmentierte Nächte (Density 13,12; 9,75; 8,54/h) könnten den Effekt dominieren. Multiple Vergleiche (Lag-Analyse + Schwellenwertsuche) ohne formale Korrektur.
- Die Migräne-Nacht-Sonderanalyse (B.15) ist ein Einzelereignis mit pharmakologischer Konfundierung (Sumatriptan-Halbwertszeit ~2h überlappt mit dem Beobachtungsfenster).
- Die Dreiersequenz (B.5.1) und Density-≥7,0-Schwelle (B.6.2) basieren auf n=6–8 Fällen. Diese Befunde sind hypothesengenerierend, nicht konfirmatorisch.
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

### **B.21 H9Z-Brustgurt-Messung 14.–15.04.2026: Einschlaf-Cliff und Plateau-Struktur**

Die unter B.9 beschriebene nächtliche HR-Trajektorie hat eine Auflösungsgrenze im Minutenbereich (Mi-Band 9). Eine ergänzende Messung mit dem Coospo-H9Z-Brustgurt (EKG-Elektroden, ±1 bpm, BT 5.0) über 14.04.2026 18:27 CEST – 15.04.2026 07:59 CEST erfasst 52.849 Beat-to-Beat-RR-Intervalle (99,8 % physiologisch plausibel) — Auflösung auf Einzelschlag-Ebene. Zwei Phänomene werden damit sichtbar, die in den Minuten-aggregierten Mi-Band-Daten systematisch unterdrückt sind: der binäre Charakter des Einschlaf-Übergangs und die 2-Stunden-Plateau-Struktur der Tageszyklik.

**Einschlaf-Cliff statt Slope**

Zeitverlauf 00:00–00:40 CEST (15.04.2026):

| Zeit [CEST] | HR [bpm] | R/S Ratio | Zustand |
|:------------|:---------|:----------|:--------|
| 23:55 | 91 | < 0,4 | Wach, sympathisch (Treppe → Bett) |
| 00:00 | 93 | — | Peak |
| 00:05 | 77 | — | Abfall beginnt |
| 00:10 | 63 | 1,01 | Umschlag |
| 00:15 | 55 | 1,07 | Vagaler Clamp erreicht |
| 00:20–00:40 | 50–56 | 1,08–1,28 | **30 Minuten reiner vagaler Clamp** |

Kein Einschlaf-Slope (normal wäre ein 30–60-min-Gradueller Abfall), sondern binärer Switch in < 15 Minuten. HR fällt 15 bpm unter den Abend-Ruhepuls (68 bpm). Diese Dynamik ist mit dem normalen parasympathischen Einschlafprozess inkompatibel: graduelle Baroreflex-Abwärtsregulation erzeugt keine R/S-Sprünge > 0,5 in < 5 Minuten.

**Mechanistische Interpretation:** Der Cliff ist kein physiologischer Übergang, sondern Ausdruck kumulierter sympathischer Erschöpfung über mehrere Tage. Das System operiert bereits am Abend im Grenzregime (Baseline HR ~70, aber kein LDX-Puffer mehr); beim Wegfall des exogenen Arousal-Drives (Augen zu, Bett) kippt es nicht graduell in den Schlaf, sondern fällt kollektiv in den Vagaler-Clamp-Attraktor. Die drei autonomen Regime (vgl. D.4.3.1) sind hier direkt im zeitlichen Verlauf ablesbar: Baseline → (keine stabile Zwischenzone) → Clamp.

**Awakening 00:41 CEST: Sympathischer Burst nach Clamp**

- R/S crasht auf 0,46, HR springt auf 71 → sympathischer Burst, vermutlich humoral (Adrenalin-Release aus Nebenniere).
- Danach erreicht R/S für den Rest der Nacht nicht wieder Werte > 1,1.
- Restliche Nacht: R/S 0,89–0,98, HR 55–65 → gemischtes Regime ohne erneuten Clamp.

**Deutung:** Der erste Clamp hat den sympathischen Puffer entladen; für den Rest der Nacht reicht die sympathische Reserve nicht mehr aus, um erneut kontrolliert in den Clamp einzutreten. Der kumulative Vortages-Effekt ist damit im Einzelverlauf direkt abbildbar.

**LDX-Interferenz zu Nacht**

- 4 mg LDX zur Nacht eingenommen: keine messbare Wirkung auf den Clamp (weder Dämpfung noch Shift).
- Vorangegangene Nächte mit 7,5 mg LDX zur Nacht: gute autonome Architektur (echter Slope statt Cliff), aber mehr Awakenings — LDX senkt die Arousal-Schwelle, keine echte Erholung → kumulative Depletion.
- Kein LDX-Dosierungsregime in diesem Dosisbereich erzeugt gleichzeitig intakten Slope und stabilen Schlaf.

Dies ist das Dosierungsdilemma, das in 06_leitlinie_titration (Abschnitt 7.2) als Designziel der Retardierung (Alginat-Beads, Abklinggradient-Streckung) formuliert ist.

**Zirkadiane Plateau-Struktur**

Jeden Tag zeigen die Langzeit-Mi-Band-Daten zwei 2-Stunden-Plateaus mit zirkadian stabiler Lage, bestätigt durch die H9Z-Einzeltaganalyse vom 15.04.2026:

```
PRE-Phase → Plateau 1 (2h) → Zwischenphase → Plateau 2 (2h) → POST-Phase
```

**Eigenschaften:**
- PRE und POST identisch in ihrer HR-Baseline.
- Plateaus persistieren auch unter Metoprolol (vgl. B.4) und ohne LDX — **endogen/zirkadian, nicht substanzinduziert**.
- LDX erzeugt am Peak einen zusätzlichen Rechteck-Puls (vgl. D.4.3.1), ohne die darunterliegende Plateau-Struktur zu verändern.

**Anfallskorrelation — Plateau-Konfiguration:**

| Konfiguration | Verlauf | Klinische Assoziation |
|:--------------|:--------|:---------------------|
| **Normal** | Niedriges Plateau zuerst, dann hohes (morgens sanfter, später Aktivitätsanstieg) | Kein Anfall |
| **Anfallstag** | Hohes Plateau zuerst, mit absteigendem Slope über die 2 Stunden | Anfall wahrscheinlich im oder nach dem Plateau |

Der Anfallsprädiktor ist nicht der absolute HR-Wert, sondern der **Intra-Plateau-Gradient**: Ein stabiles Plateau = ausreichende sympathische Reserve (Dämpfungskonstante intakt, vgl. 2.5.5). Ein degradierendes Plateau = Reserve reicht nicht, um das Niveau über 2h zu halten → Anfallsrisiko erhöht.

Mechanistisch entspricht das degradierende Plateau einem Overshoot beim Einsteigen (Adrenozeptor-Supersensitivität auf NE-Depletion-Basis, vgl. 7.4, Buse-Trend 3), gefolgt von dem Unvermögen, das Niveau zu halten — Depletion während der Plateau-Phase. Der Gradient ist damit der funktionsnahste autonome Marker für die aktuelle Puffertiefe.

**Diagnostische Konsequenz:** Die vier HR-Anomalie-Marker (D.4.3.2) sind direkt aus der Plateau-Struktur ablesbar. Für ein Screening reicht ein HR-Logger mit 1-Minuten-Auflösung + Plateau-Detektion; die prädiktive Größe ist dHR/dt über das Morgen-Plateau, nicht der absolute HR-Wert.

| Aussage | Evidenzniveau | Quellenbasis |
|:--------|:--------------|:-------------|
| Binärer Einschlaf-Cliff statt Slope bei kumulativer sympathischer Depletion | Deskriptiv, n=1 Nacht H9Z | H9Z 14.–15.04.2026 |
| 30-min reiner vagaler Clamp unmittelbar nach Einschlaf-Cliff | Deskriptiv, n=1 Nacht | H9Z |
| Zirkadiane 2×2h-Plateau-Struktur, substanzinvariant | Deskriptiv, Langzeit | Mi-Band (n=79 Nächte) + H9Z-Bestätigung |
| Intra-Plateau-Gradient (dHR/dt) als Anfallsprädiktor | Hypothetisch, konsistent mit Einzelfall | Langzeitdaten; vgl. 2.5.5, 7.4 |
| LDX als additiver Rechteck-Puls, plateau-strukturinvariant | Deskriptiv, n=2 Dosen | H9Z |

---

### **B.22 Referenzen**

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
