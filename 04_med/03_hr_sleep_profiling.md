# HR-Schlafprofilierung: Methodik und physiologische Grundlage

## 1. Einordnung

Dieses Dokument beschreibt eine Methode zur Analyse nächtlicher Herzfrequenz-Zeitreihen aus Consumer-Wearables (PPG-basiert, 1-Minuten-Taktung), die über reine Schlafstadienerkennung hinausgeht. Die Methode extrahiert eine hierarchische Plateau-Struktur aus der HR-Kurve und interpretiert sie als Proxy für die Modulationsqualität subkortikaler serotonerger Kerngebiete (B7/DRN und B8/MRN) im Schlaf.

Die Methode ist explorativ, auf einem Einzelfall entwickelt (n=1, 88 Nächte über 16 Monate), und nicht extern validiert. Sie wird dokumentiert, weil die extrahierten Parameter signifikante Korrelationen mit migränösen Anfällen zeigen und sich kohärent in ein theoretisches Modell der Raphe-Dysregulation einfügen. Die Methode könnte als Hypothesengenerator für systematische Studien dienen.

---

## 2. Stand der Wissenschaft: HR im Schlaf

### 2.1 Gesicherte Grundlagen

Die nächtliche Herzfrequenz ist kein passiver Nebeneffekt des Schlafs, sondern ein aktiv regulierter Parameter, der die sympathovagale Balance widerspiegelt.

**Ultradian HR-Oszillationen im Schlaf.** Brandenberger et al. (1994) dokumentierten, dass die HR im Schlaf nicht monoton sinkt, sondern in ultradianen Zyklen von ~90 Minuten oszilliert, synchron mit der NREM-REM-Zyklik. Der vagale Tonus (gemessen über HF-HRV) folgt einem klaren Muster: Anstieg in NREM, Abfall in REM. Die HR-Oszillation ist damit nicht Rauschen, sondern ein Readout der zentralen Schlafstadiengenerierung.

**Circadiane Modulation.** Boudreau et al. (2013) zeigten, dass die HRV-Oszillationen im Schlaf eine circadiane Hüllkurve besitzen: Die vagale Dominanz ist in der ersten Nachthälfte stärker als in der zweiten, unabhängig vom Schlafstadium. Es gibt also mindestens zwei überlagerte Oszillatoren in der nächtlichen HR: den ultradianen (~90 min, schlafstadiengekoppelt) und den circadianen (~24 h, SCN-gesteuert).

**HR als ANS-Proxy.** Die HR integriert sympathische und parasympathische Einflüsse auf den Sinusknoten. Im Schlaf verschiebt sich die Balance zugunsten des Parasympathikus, was den nächtlichen HR-Abfall erzeugt. Die Tiefe und Stabilität dieses Abfalls reflektiert die Qualität der parasympathischen Aktivierung — und damit indirekt die Integrität der zentralen Regulatoren, die den autonomen Tonus steuern.

**Serotonin und autonome Regulation.** Der dorsale Raphekern (DRN, B7) projiziert sowohl in den Thalamus als auch in autonome Kerngebiete. Serotonerge Neurone feuern im Wachzustand tonisch, reduzieren ihre Feuerrate in NREM und pausieren in REM (Monti 2008). Der nächtliche HR-Verlauf ist damit teilweise ein downstream-Readout der serotonergen Aktivität: Wenn der DRN supprimiert ist, sinkt der sympathische Tonus, die HR fällt. Wenn der DRN reaktiviert (Microarousal, REM-Ende), steigt sie.

### 2.2 Was die Literatur nicht liefert

**Keine Plateau-Analyse.** Die bestehende Schlaf-HR-Forschung arbeitet mit globalen Metriken (mittlere HR, HRV-Indizes pro Schlafstadium, nächtlicher HR-Dip als Prozent des Tagesmittels) oder mit spektralanalytischen Methoden (LF/HF-Ratio, HRV-Power in Frequenzbändern). Eine hierarchische Segmentierung der HR-Kurve in verschachtelte Plateau-Ebenen existiert in der Literatur nicht.

**Keine Nadir-basierte Strukturanalyse.** Lokale Minima der HR-Kurve werden in der Literatur nicht systematisch als Strukturelemente behandelt. Die Idee, dass die Menge und Tiefe der HR-Nadirs die Modulationstiefe eines spezifischen subkortikalen Kerngebiets widerspiegelt, ist literaturfremd.

**Keine Merge-Tree-Topologie auf HR-Zeitreihen.** Topologische Datenanalyse (Merge Trees, Persistence Diagrams) wird in anderen Domänen eingesetzt (Bildverarbeitung, Klimadaten, Genomik), aber nicht auf kardiovaskuläre Schlaf-Zeitreihen angewendet. Die hier beschriebene Methode verwendet einen 1D-Merge-Tree-Ansatz für die Plateau-Gruppierung, ist sich aber bewusst, dass dies eine Neukontextualisierung bekannter mathematischer Werkzeuge ist, keine Standardanwendung.

**Keine serotonerge Zuordnung der HR-Mikrostruktur.** Die Literatur verknüpft Serotonin mit dem Schlaf und Serotonin mit der HR, aber nicht die Mikrostruktur der nächtlichen HR (Form, Tiefe und Hierarchie einzelner HR-Wellen) mit dem Zustand spezifischer serotonerger Projektionssysteme. Dies ist der hypothetische Kern der hier beschriebenen Methode.

### 2.3 Verwandte Ansätze

**RMSSD und HRV-basierte Schlafstadien.** Einige Ansätze nutzen HRV-Metriken (RMSSD, pNN50) zur automatischen Schlafstadienerkennung (de Zambotti et al. 2018). Diese arbeiten auf Beat-to-Beat-Intervallen und zielen auf die Stadienzuordnung, nicht auf die Hüllkurvenstruktur.

**Cardiopulmonary Coupling (CPC).** Thomas et al. (2005) entwickelten ein Verfahren, das die Kopplung zwischen HR-Oszillation und Atemrhythmus nutzt, um stabile vs. instabile NREM-Phasen zu klassifizieren. CPC ist konzeptionell verwandt (es erkennt Qualitätsunterschiede innerhalb eines Schlafstadiums), operiert aber auf einer anderen Zeitskala (Beat-to-Beat) und extrahiert keine hierarchische Plateau-Struktur.

**Stochastische Resonanz im Tracker.** Vyazovskiy et al. (2011) zeigten, dass Schlaf nicht global ist, sondern lokal — einzelne kortikale Regionen können im „Off-State" sein, während benachbarte Regionen wach bleiben. Ein Wrist-Tracker mit PPG-Sensor und Accelerometer ist ein stochastischer Resonanz-Detektor: Er samplet einen einzelnen Punkt (Handgelenk) und kodiert die Instabilität des Gesamtsystems als Übergangsfrequenz in seinem Hypnogramm. Die hier beschriebene HR-Analyse ist ein komplementärer Kanal zum selben Phänomen.

---

## 3. Methode

### 3.1 Datengrundlage

**Hardware:** Xiaomi Smart Band 9, PPG-basierte HR-Messung, ~1 Sample/Minute im Schlafmodus.

**Software:** Gadgetbridge (Open-Source Android App), exportiert eine SQLite-Datenbank mit den Tabellen `XIAOMI_ACTIVITY_SAMPLE` (HR-Zeitreihe) und `XIAOMI_SLEEP_TIME_SAMPLE` (Schlafzusammenfassungen).

**Limitationen der Datenquelle:**
- PPG-Artefakte (Bewegung, Sensorablösung) werden nicht algorithmisch korrigiert, sondern durch die 10-Minuten-Glättung (MHR10) gedämpft.
- Die zeitliche Auflösung (1 min) erlaubt keine Beat-to-Beat-Analyse; HRV im klassischen Sinn ist nicht verfügbar.
- Die Schlafstadienerkennung des Trackers (Accelerometer + PPG-Fusion) ist proprietär und nicht nachvollziehbar. Die hier beschriebene Methode nutzt die Stadien nur zur Fensterung (Schlafstart/-ende), nicht für die HR-Analyse selbst.

### 3.2 Signalverarbeitung

**MHR10:** Zentrierter gleitender Mittelwert über 10 Minuten. Glättet einzelne Ausreißer und Messartefakte, erhält aber die Wellenstruktur auf der Zeitskala von 15–60 Minuten. Die Wahl von 10 Minuten ist ein Kompromiss: kürzere Fenster (5 min) erhalten mehr Feinstruktur, erzeugen aber Rausch-Nadirs; längere Fenster (30 min) glätten die schnelle Oszillation weg.

### 3.3 Nadir-Detektion

Ein Nadir ist ein lokales Minimum der MHR10-Kurve. Die Detektion verwendet einen Custom-Algorithmus mit drei Parametern:

- **min_depth = 0.5 bpm:** Ein Minimum muss beidseitig mindestens 0.5 bpm unter seinen Nachbarn liegen. Dies filtert Plateaus mit minimaler Welligkeit.
- **min_dist = 10 min:** Mindestabstand zwischen zwei Nadirs. Verhindert die Detektion von Rausch-Doppelminima und erzwingt eine minimale Phasenlänge.
- **Flat-Bottom-Handling:** Der Algorithmus erkennt flache Böden (mehrere aufeinanderfolgende Minimalwerte) korrekt als ein Nadir, anstatt sie zu überspringen (wie `scipy.signal.argrelmin` es tut).

Die Parameter wurden gegen eine visuell annotierte Referenznacht validiert (20 Nadirs in einer 400-Minuten-Nacht, alle visuell identifizierten Minima korrekt detektiert, keine falsch-positiven).

### 3.4 Phasen

Eine Phase ist der Zeitabschnitt zwischen zwei konsekutiven Nadirs. Sie repräsentiert einen einzelnen HR-Hügel — eine Episode, in der die HR vom Nadir ansteigt, ein lokales Maximum erreicht und zum nächsten Nadir absinkt. Für jede Phase werden HR-Mittelwert und HR-Standardabweichung aus den Rohdaten (nicht MHR10) berechnet.

Die Phasen bilden die schnelle Oszillatorebene ab (~15–40 Minuten Periodizität). In der Schlafphysiologie korrespondiert diese Zeitskala grob mit der Dauer einzelner NREM- oder REM-Episoden, aber die Korrespondenz ist nicht eins-zu-eins: Eine Phase kann ein Schlafstadium oder den Übergang zwischen zwei Stadien umfassen.

### 3.5 Plateau-Detektion

#### Konzept

Ein Plateau ist ein HR-Niveau, das durch einen oder mehrere Nadirs auf gleicher Höhe definiert wird. Plateaus repräsentieren die langsame Oszillatorebene — die Hüllkurve, auf der die schnellen HR-Hügel reiten.

Die Grundidee: Zieht man vom tiefsten Punkt eines Nadirs eine horizontale Linie nach links und rechts, schneidet diese Linie die MHR10-Kurve an zwei Punkten. Alles zwischen diesen Schnittpunkten liegt auf oder über dem Niveau dieses Nadirs — das ist das Plateau. Wenn zwei Nadirs auf ähnlichem Niveau liegen und die MHR10 zwischen ihnen nie unter dieses Niveau fällt, gehören sie zum selben Plateau.

#### Algorithmus

**Zwei-Pass-Gruppierung:**

1. **Pass 1 (Greedy temporal, Toleranz 1.0 bpm):** Nadirs werden in zeitlicher Reihenfolge durchlaufen. Jeder Nadir wird der bestehenden Gruppe zugeordnet, wenn (a) sein MHR10-Wert innerhalb von 1.0 bpm des Gruppenmittels liegt und (b) die MHR10-Kurve zwischen ihm und mindestens einem Gruppenmitglied nirgends unter das gemeinsame Niveau fällt (Merge-Tree-Konnektivität). Andernfalls bildet er eine neue Gruppe.

2. **Pass 2 (Singleton-Merge, Toleranz 1.3 bpm):** Gruppen mit nur einem Nadir werden nachträglich zusammengeführt, wenn ihre Niveaus ≤ 1.3 bpm auseinanderliegen und die Konnektivitätsbedingung erfüllt ist.

**Plateau-Grenzen:** Vom tiefsten Nadir der Gruppe wird eine horizontale Linie bei seinem MHR10-Wert nach links und rechts verlängert, bis die MHR10-Kurve diese Linie unterschreitet (Toleranz 0.5 bpm). Die Schnittpunkte definieren Start und Ende des Plateaus.

**Elevation-Filter:** Plateaus, deren Niveau weniger als 1.5 bpm über dem Niveau ihres Eltern-Plateaus (des nächstniedrigeren umschließenden Plateaus) liegt, werden als Rauschen entfernt. Dies erzwingt einen minimalen strukturellen Abstand zwischen den Ebenen der Hierarchie.

#### Merge-Tree-Topologie

Die Gruppierung ist formal ein 1D-Merge-Tree (aus der topologischen Datenanalyse): Beim schrittweisen Anheben eines Schwellwerts von unten verschmelzen benachbarte Bassins zu einem gemeinsamen Plateau, sobald der Schwellwert ihr trennendes Minimum erreicht. Dasselbe Prinzip findet sich als Watershed Transform in der Bildverarbeitung (dort auf 2D) und ist verwandt mit dem Prominenz-Begriff in der Topographie.

### 3.6 Stacktiefe

Die Stacktiefe eines Plateaus ist die Anzahl der Plateaus mit niedrigerem Niveau, die es zeitlich vollständig umschließen. Das tiefste Plateau der Nacht (Baseline) hat Stacktiefe 0. Höhere Plateaus, die innerhalb der Baseline liegen, haben Stacktiefe 1, usw.

Die Stacktiefe quantifiziert die Verschachtelungstiefe der Modulation: Mehr Ebenen bedeuten, dass die HR-Kurve eine tiefere hierarchische Struktur besitzt — mehr überlagerte Modulatoren erzeugen mehr ineinander verschachtelte Niveaus.

---

## 4. Physiologische Interpretation

### 4.1 Zwei-Oszillatoren-Modell

Die Nacht-HR zeigt zwei überlagerte Oszillationen:

1. **Schneller Oszillator** (~15–40 min): Erzeugt die HR-Hügel (Phasen). Korrespondiert zeitlich mit der ultradianen NREM/REM-Zyklik, ist aber nicht identisch mit ihr, da die HR die sympathovagale Balance integriert, nicht das Schlafstadium direkt.

2. **Langsamer Oszillator** (~60–120 min): Moduliert die Amplitude und das Grundniveau der schnellen Hügel. Erzeugt die Plateaus — Niveaus, auf denen mehrere Hügel reiten. Dieser Oszillator hat keine direkte Entsprechung in der klassischen Schlafstadien-Nomenklatur.

Die Plateau-Hierarchie bildet ab, wie diese beiden Oszillatoren interagieren. Bei sauberer Modulation erzeugt der langsame Oszillator wenige, gleichmäßig verteilte Niveaus, auf denen der schnelle Oszillator regelmäßig schwingt. Bei gestörter Modulation fragmentiert die Hierarchie: zu viele Ebenen, ungleichmäßige Dauern, Brüche in der Konsistenz.

### 4.2 Mapping auf die serotonerge Modulation

Die folgende Zuordnung ist hypothetisch und basiert auf einem Modell der Raphe-Dysregulation, nicht auf direkter neurophysiologischer Messung.

**B7 (DRN) als Modulationstiefe.** Der dorsale Raphekern projiziert über den Thalamus in den Kortex und beeinflusst über den Locus coeruleus (LC) den sympathischen Tonus. Die Feuerrate des B7 im Schlaf korreliert mit dem HR-Level: Höhere B7-Aktivität $\rightarrow$ höherer sympathischer Tonus $\rightarrow$ höhere HR. Die Nadirs der MHR10-Kurve markieren Momente minimaler B7-Aktivität — die Punkte, an denen die serotonerge Suppression maximal ist und der Parasympathikus dominiert.

**Plateau-Niveau als B7-Amplitudenmarker.** Das Niveau eines Plateaus (definiert durch die tiefsten Nadirs der Gruppe) reflektiert, wie tief der B7 die HR drücken kann. Ein tiefes Baseline-Plateau (niedrige MHR10 an den Nadirs) zeigt eine hohe B7-Modulationskapazität — er kann den sympathischen Tonus effektiv suppressen. Ein hohes Baseline-Plateau zeigt reduzierte Modulationskapazität oder B7-Ausfall.

**Hohe Plateaus als ANS-Eigenzeit.** Plateaus weit über der Baseline repräsentieren Phasen, in denen der B7 die HR nicht moduliert — das autonome Nervensystem agiert in seiner Eigendynamik. Diese Phasen sind gekennzeichnet durch flache HR (geringe MHR10-Variabilität innerhalb des Plateaus), da ohne B7-Modulation der einzige verbleibende Treiber die langsame circadiane Drift und die Arousal-Dynamik ist.

**Nadir-Slope als B7-Progressionsmarker.** Die Regression der Nadir-MHR10-Werte über die Nacht (nadir_slope) zeigt, ob der B7 über die Nacht progressiv tiefer moduliert (negativer Slope = physiologische parasympathische Vertiefung) oder ob die Modulation stagniert oder ansteigt (flacher/positiver Slope = fehlende Progression). Ein flacher nadir_slope ist im Modell der direkteste HR-basierte Proxy für B7-Defizienz.

### 4.3 B8 (MRN) und die Schwebung

Der mediane Raphekern (B8/MRN) ist die einzige direkte serotonerge Afferenz des SCN. Im Modell erzeugt die Phasenbeziehung zwischen B7 und B8 eine Schwebung mit einer Periodizität von ~4–7 Tagen.

In der HR-Profilierung ist die B8-Instabilität nicht direkt sichtbar, sondern als inter-Nacht-Variabilität der Modulationsqualität: Wenn die B7/B8-Phasenbeziehung synchron ist, zeigt die Nacht eine saubere Plateau-Hierarchie (wenige Brüche, gleichmäßige Level-Abstände). Wenn sie desynchron ist, fragmentiert die Hierarchie. Die Nacht-zu-Nacht-Schwankung der Modulationsqualitäts-Metriken (break_frac, spacing_cv, stack_symmetry) reflektiert damit die quasi-wöchentliche B7/B8-Schwebung.

### 4.4 Anfallszyklus-Signatur

Auf der Basis von 88 Nächten (59 PRE unter Betablocker, 29 POST unter LDX) und 38 Anfallstagen zeigt sich eine charakteristische Sequenz in den Modulationsqualitäts-Metriken:

**Tag −2 (zwei Tage vor Anfall):** Sauberste Modulation — niedrigste break_frac (0.51 vs. Baseline 0.59, MWU p=0.037), niedrigster spacing_cv (0.62 vs. 0.77, p=0.046). Interpretation: B7 arbeitet noch stabil. Die Schwebungsphase ist günstig.

**Tag −1 (Nacht vor Anfall):** Rigidere Modulation — niedrigster intra_dur_cv (0.66 vs. 0.81, p=0.091). Die Plateaus gleicher Tiefe werden gleichförmiger. Interpretation: B7 unter zunehmendem Stress, verliert Adaptivität.

**Tag 0 (Anfallsnacht):** Nadir_slope flacht ab (−0.24 vs. −0.43, p=0.023), Stack wird bodenlastig (stack_symmetry 0.25 vs. 0.31, p=0.054), mehr Nadirs und Phasen (p=0.023). Interpretation: B7-Restart mit desolatem Takt — er moduliert, aber desynchron. Die HR zeigt die höchste Fragmentierung.

Die Sequenz ist konsistent mit einem Modell, in dem nicht der B7-Ausfall den Anfall auslöst, sondern der instabile Restart nach dem Ausfall. Der B7 springt über seine Autoregulation an, aber die asymmetrisch regenerierten Komponenten erzeugen ein kurzes Fenster mit hoher Amplitude bei fehlender Phasenkohärenz.

---

## 5. Modulationsqualitäts-Metriken

### 5.1 Übersicht

Die Methode extrahiert pro Nacht 25 Metriken in vier Kategorien:

| Kategorie | Metriken | Misst |
|-----------|----------|-------|
| Plateau-Struktur | n_plateaus, max_depth, base_level, total_range | Grundarchitektur der Hierarchie |
| Modulationsqualität | dur_cv, count_cv, break_frac, spacing_cv, stack_symmetry, intra_dur_cv | Konsistenz und Regularität der hierarchischen Schichtung |
| ANS-Autonomie | frac_high, frac_vhigh, n_d3 | Anteil der Schlafzeit ohne B7-Modulation |
| Phasen/Nadir-Dynamik | phase_dur_cv, nadir_slope, nadir_range | Taktqualität und Progressionsdynamik |

### 5.2 Definitionen

**break_frac** (Modulationsbrüche): Anteil der Plateaus, deren Dauer um mehr als den Faktor 2 von der mittleren Dauer auf benachbarten Stacktiefen abweicht. Misst, wie konsistent die hierarchische Schichtung über die Stacktiefen ist. Hohe Werte zeigen Stellen, an denen ein Plateau viel zu lang oder zu kurz für seine Position in der Hierarchie ist.

**spacing_cv** (Level-Abstandsregularität): Variationskoeffizient der Abstände zwischen den Plateau-Niveaus. Bei gleichmäßiger Schichtung (regelmäßige bpm-Abstände zwischen den Ebenen) ist der CV niedrig. Hohe Werte zeigen, dass einige Level-Sprünge viel größer sind als andere — die Hierarchie hat Lücken.

**stack_symmetry** (Dauer-Symmetrie): Verhältnis der mittleren Plateaudauer in der oberen Stackhälfte zur unteren Hälfte. Werte < 1 (bodenlastig) zeigen, dass die tiefen Plateaus die Nacht dominieren und die hohen Plateaus kurzlebig sind. Werte > 1 (kopflastig) zeigen das Gegenteil — ausgedehnte ANS-Eigenzeit.

**nadir_slope** (Nadir-Progression): Lineare Regression der MHR10-Werte an den Nadir-Positionen über den Verlauf der Nacht. Ein negativer Slope zeigt die physiologische progressive parasympathische Vertiefung: Die Nadirs werden über die Nacht tiefer. Ein flacher oder positiver Slope zeigt das Fehlen dieser Progression — der stärkste einzelne Korrelat mit Anfällen in der vorliegenden Daten (r=+0.24, p=0.023 am Anfallstag).

---

## 6. Confounders und Limitationen

### 6.1 Pharmakologische Confounders

**Betablocker (Metoprolol):** Dämpft die HR-Variabilität pharmakologisch. Alle amplitudenbasierten Metriken (nadir_std, nadir_range, mean_phase_std, total_range, frac_high) sind im PRE-Zeitraum (unter Betablocker) nach unten verzerrt. Strukturelle Metriken (break_frac, spacing_cv, stack_symmetry) sind robuster, aber nicht vollständig frei vom Confounder, da die reduzierte HR-Dynamik die Anzahl detektierbarer Plateaus beeinflusst.

**LDX (Lisdexamfetamin):** Erhöht den dopaminergen Tonus, was die serotonerge Regulation indirekt beeinflusst. POST-Daten (unter LDX) zeigen eine veränderte Plateau-Landschaft, die nicht allein auf den Wegfall des Betablockers zurückführbar ist.

**Within-Period-Vergleiche** (Anfalls- vs. Nicht-Anfallsnächte innerhalb derselben Medikationsperiode) sind vom pharmakologischen Confounder nicht betroffen, da die Pharmakologie konstant ist.

### 6.2 Tracker-Limitationen

- **Proprietärer Algorithmus:** Die Schlafstadienerkennung ist nicht nachvollziehbar. Die HR-Analyse nutzt die Stadien nur zur Fensterung, nicht inhaltlich.
- **1-Minuten-Auflösung:** Beat-to-Beat-HRV ist nicht verfügbar. Die Analyse operiert auf der Zeitskala von Minuten, nicht Sekunden.
- **PPG-Artefakte:** Bewegung, Sensorablösung und schlechte Perfusion erzeugen Ausreißer. Die MHR10-Glättung dämpft diese, eliminiert sie aber nicht vollständig.
- **Tracker-Phasenerkennung vs. HR-Analyse:** Die Schlafphasenerkennung basiert primär auf Accelerometerdaten (Bewegung) und ist vom Betablocker entkoppelt. Die HR-Analyse ist es nicht. Dies erzeugt eine informative Dissoziation: Wenn die bewegungsbasierte Fragmentierung (Tracker) und die HR-basierte Fragmentierung (Plateau-Analyse) konvergieren, stärkt das den Befund.

### 6.3 Statistik

- **n=1-Design:** Alle Befunde stammen von einer Person. Generalisierbarkeit ist unbekannt.
- **Multiple Vergleiche:** 25 Metriken × 4 Seizure-Lags × 3 Perioden = 300 Tests. Keine Korrektur für multiples Testen durchgeführt. Die stärksten Befunde (nadir_slope am Anfallstag: p=0.023; break_frac 2 Tage vor Anfall: p=0.037) würden eine Bonferroni-Korrektur nicht überleben.
- **Anfallszahl:** 17 Anfälle in PRE, 3 in POST. Die POST-Analyse ist rein explorativ.
- **Effektstärken:** Klein (r ≈ 0.2). Diagnostisch nicht verwertbar; als Hypothesengeneratoren belastbar.
- **Zirkularität:** Die Methode wurde am selben Datensatz entwickelt und getestet. Eine unabhängige Validierung an separaten Daten ist nicht erfolgt.

### 6.4 Physiologische Zuordnung

Die Zuordnung der HR-Plateaus zu B7/B8-Zuständen ist hypothetisch. Zwischen dem PPG-Signal am Handgelenk und der Feuerrate einzelner Raphekerne liegen multiple vermittelnde Schichten (LC, autonome Ganglien, Baroreflex, Atemrhythmus). Die Spezifität der Zuordnung ist gering — die Methode misst das Integral der sympathovagalen Balance, nicht den B7 oder B8 direkt.

Die modellkonforme Interpretation beruht auf der Konvergenz von:
1. Zeitlicher Passung (Periodizität der Modulationsqualität ≈ vorhergesagte Schwebungsperiode)
2. Richtung der Korrelationen (kongruent mit dem Restart-Modell)
3. PRE/POST-Dissoziation (LDX verändert die Signatur auf modellkonforme Weise)

Konvergenz ersetzt nicht kausale Validierung. Dieselben Daten könnten alternative Interpretationen tragen.

---

## 7. Reproduzierbarkeit und prospektive Anwendung

### 7.1 Technische Reproduzierbarkeit

Die Methode ist vollständig in Python implementiert und erfordert nur Open-Source-Bibliotheken (numpy, pandas, scipy) sowie einen Gadgetbridge-kompatiblen Wearable-Tracker. Die Algorithmen sind deterministisch bei gegebenen Parametern.

### 7.2 Prospektive Testbarkeit

Die Methode erzeugt falsifizierbare Vorhersagen:

1. **Intra-individuell:** Der nadir_slope der aktuellen Nacht sollte als Risikoindikator für die nächsten 48 Stunden verwertbar sein. Ein flacher werdender Slope über 2–3 Nächte sollte einem Anfall vorausgehen.

2. **Inter-individuell:** Bei Patienten mit Raphe-Dysregulation (Population A im Modell) sollte die Plateau-Hierarchie eine höhere Nacht-zu-Nacht-Variabilität zeigen als bei gesunden Kontrollen. Bei Patienten ohne Raphe-Beteiligung (Population B) sollte die Methode keine anfallskorrelierten Signaturen finden.

3. **Interventionssensitivität:** Pharmakologische Interventionen, die den B7 modulieren (H1-Antagonisten wie DPH, 5-HT1A-Agonisten), sollten die Plateau-Landschaft auf spezifische, vorhersagbare Weise verändern. Initiale Daten unter DPH (n=3 Nächte) zeigen eine Reduktion der MHR10-Variabilität und einen engeren HR-Korridor — richtungskonsistent mit B7-Suppression.

---

## 8. Zusammenfassung

Die hier beschriebene Methode extrahiert eine hierarchische Plateau-Struktur aus der nächtlichen HR eines Consumer-Wearables. Sie basiert auf der Beobachtung zweier überlagerter Oszillatoren in der Schlaf-HR und verwendet topologische Konzepte (1D-Merge-Tree) zur Formalisierung der Hüllkurvenstruktur.

Die wissenschaftliche Grundlage für die HR als Schlafqualitätsmarker ist gesichert. Die spezifische Methodik (Nadir-Detektion, Plateau-Gruppierung, Stacktiefe, Modulationsqualitäts-Metriken) ist neu und nicht extern validiert. Die physiologische Zuordnung zu serotonergen Kerngebieten ist hypothetisch.

Der potenzielle Wert der Methode liegt nicht in der Diagnostik, sondern in drei Eigenschaften:
1. Sie ist **kontinuierlich** über Monate einsetzbar (keine Labortermine).
2. Sie extrahiert **Nacht-zu-Nacht-Variabilität** als eigentliches Signal, nicht als Rauschen.
3. Sie erzeugt **quantitative, falsifizierbare** Vorhersagen über den Zusammenhang zwischen Schlafarchitektur und Anfallsrisiko.

Ob diese Vorhersagen sich bestätigen, wird die prospektive Anwendung zeigen.

---

## Referenzen

- Boudreau, P. et al. (2013). Circadian variation of heart rate variability across sleep stages. *Sleep*, 36(12), 1919–1928.
- Brandenberger, G. et al. (1994). Ultradian rhythms in heart rate and cardiac vagal tone during sleep. *Journal of Biological Rhythms*, 9(2), 165–178.
- de Zambotti, M. et al. (2018). Wearable sleep technology in clinical and research settings. *Medicine and Science in Sports and Exercise*, 51(7), 1538–1557.
- Monti, J. M. (2008). Roles of dopamine and serotonin in sleep regulation. *Progress in Brain Research*.
- Thomas, R. J. et al. (2005). An electrocardiogram-based technique to assess cardiopulmonary coupling during sleep. *Sleep*, 28(9), 1151–1161.
- Vyazovskiy, V. V. et al. (2011). Local sleep in awake rats. *Nature*, 472, 443–447.