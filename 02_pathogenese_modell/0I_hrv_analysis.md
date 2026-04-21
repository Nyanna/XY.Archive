---
title: "Der B7-Kern, 5-HT1A-Autorezeptor-Dynamik und ihre Signatur im HRV-Frequenzspektrum"
subtitle: "Eine Kontextualisierung für die pathogenetische Analyse autonomer Oszillationen"
author: "Synthese-Dokument"
date: 2026-04-20
abstract: |
  Dieses Dokument synthetisiert das wissenschaftliche Material zur rostralen Dorsal-Raphe-Region (Zellgruppe B7 nach Dahlström & Fuxe), zur somatodendritischen 5-HT1A-Autorezeptor-Rückkopplung und zu deren Manifestation in den Spektralbändern der Herzfrequenzvariabilität. Ziel ist die kompakte Bereitstellung des pathogenetischen Kontexts für eine nachfolgende empirische Datenauswertung. Nicht enthalten sind formale Herleitungen der spektralen Transformation oder Bifurkationsanalysen des Oszillatormodells.
---

***

## **Anhang I: Tracker-Datenanalyse — HRV Frequenzspektrum**

**Einleitung und Geltungsbereich**

Die serotonerge Neuromodulation des Hirnstamms stellt einen zentralen Konvergenzknoten für die Regulation nozizeptiver, autonomer und arousal-bezogener Funktionen dar. Zwei Beobachtungsebenen, die in der klinischen Forschung unabhängig voneinander etabliert sind, konvergieren in der Systematik des B7-Kerns: die **ultraslow serotonerge Dynamik** (Zeitskala: Minuten) und die **Spektraldynamik der Herzfrequenzvariabilität** in den tieffrequenten Bändern (ULF, VLF). Dieses Dokument formuliert die Brücke zwischen beiden, ohne sie als etablierten Konsens darzustellen: die direkte Kopplungsinstanz zwischen oszillatorischer 5-HT1A-Dynamik im B7-Kern und dem ULF-/VLF-Spektrum der HRV ist in der Primärliteratur bislang nicht als eigenständiges Messparadigma verankert. Die vorliegende Synthese stellt den mechanistischen Rahmen bereit, innerhalb dessen sich dieser Schritt prüfbar formulieren lässt.


**Anatomie und Zellgruppenzuordnung: B7 im Dorsal-Raphe-Komplex**

Die Zellgruppennomenklatur B1–B9 geht auf die histofluoreszenzbasierten Arbeiten von Dahlström und Fuxe (1964) zurück. Im Rahmen dieses Schemas bezeichnet **B7** den rostralen Anteil des Dorsal-Raphe-Kerns (DRN); B6 entspricht dem kaudalen DRN, B8 dem Nucleus raphe medianus (MRN). Der B7-Cluster ist der dichteste 5-HT-haltige Zellverband des gesamten ZNS und die Hauptquelle der aszendierenden serotonergen Projektionen zum Vorderhirn.

Wichtige Projektionsfelder aus B7:

- **Präfrontaler und cingulärer Kortex** – kognitive Kontrolle, affektive Modulation
- **Hippocampus und Amygdala** (teils überlappend mit MRN-Afferenzen) – Gedächtnis, emotionale Salienz
- **Thalamus** – über 5-HT1A/2A Modulation der thalamokortikalen Transmission
- **Hypothalamus (PVN, SCN, LH)** – neuroendokrine und zirkadiane Integration
- **Periaquäduktales Grau, Locus coeruleus, Nucleus raphe magnus** – absteigende nozizeptive Kontrolle

Die somatodendritische Kompartimentierung der 5-HT1A-Rezeptoren innerhalb des B7-Kerns ist immunhistochemisch seit den Arbeiten von Sotelo et al. (1990) und Riad et al. (2000) etabliert. Somit existiert im B7 sowohl die Quelle der Serotonintransmission als auch der Schaltkreis, der diese Quelle autoinhibitorisch reguliert – die strukturelle Voraussetzung für einen eigenständigen Oszillator.

### **I.1 Die 5-HT1A-Autorezeptor-Rückkopplung: Signaltransduktion und Kinetik**

**Rezeptorklasse und G-Protein-Kopplung**

Der 5-HT1A-Rezeptor ist ein klassischer G-Protein-gekoppelter Rezeptor vom Gi/o-Typ. Im somatodendritischen Kompartiment des B7-Kerns fungiert er ausschließlich als **Autorezeptor**; im Vorderhirn überwiegt die postsynaptische Heterorezeptor-Funktion. Die Aktivierung führt über Gαi-Untereinheiten zur Hemmung der Adenylatzyklase (Reduktion von cAMP) und über βγ-Untereinheiten zur Öffnung einwärtsgleichrichtender Kalium-Kanäle der **Kir3-Familie (GIRK)**. Die daraus resultierende Hyperpolarisation reduziert die neuronale Feuerrate und damit die axonale 5-HT-Freisetzung im Zielgebiet.

Der pharmakologisch-mechanistische Nachweis der GIRK-Kopplung ist durch Whole-Cell-Voltage-Clamp-Experimente am DRN gesichert: 5-HT1A-Autorezeptor-aktivierte K⁺-Leitfähigkeit wird durch Ba²⁺ (EC50 ≈ 9.4 µM) vollständig und durch den GIRK-spezifischen Blocker Tertiapin-Q (EC50 ≈ 33.6 nM) zu etwa 84 % blockiert, wobei die residuale Fraktion auf eine von GIRK1-GIRK2-Heteromeren abweichende Untereinheitszusammensetzung hinweist (Montalbano et al., 2015).

**Zeitkonstanten der Rückkopplung**

Die 5-HT1A-Autorezeptor-Rückkopplung operiert auf mehreren getrennten Zeitebenen. Die folgende Gliederung ist eine didaktische Abstraktion aus Elektrophysiologie, Voltammetrie und Modellierung; die einzelnen Konstanten sind experimentell nicht gleich belastbar dokumentiert:

| Prozess | Zeitskala | Ebene |
|---|---|---|
| Akute synaptische IPSC | 100–500 ms | elektrophysiologisch |
| Systemische Gain-Stabilisierung | 2–10 min | voltammetrisch |
| Verzögerungskonstante τ im Feedback-Modell | **10–20 min** | modellbasiert |
| Maximale Inhibition nach Agonist-Stimulation | 15–30 min | pharmakodynamisch |
| Recovery zur Basalrate | 30–60 min | pharmakodynamisch |

Die Verzögerungskonstante τ ist keine direkt gemessene Periode eines beobachteten Zyklus, sondern ein Modellparameter, der die kumulierte Latenz zwischen 5-HT-Freisetzung und voll ausgebildeter postsynaptischer/autorezeptor-vermittelter Rückwirkung repräsentiert. Bei einem delayed-negative-feedback-Oszillator produziert ein τ in diesem Bereich einen Grenzzyklus mit Eigenperiode T ≈ 2τ bis 4τ, also **etwa 20–80 Minuten**.

Die Verortung der einzelnen Zeitkonstanten und ihre Projektion auf die HRV-Spektralbänder ist im Diagramm visualisiert.

![Zeitkonstanten](<images/fig1_autoreceptor_timescales.png>){width=90%}

**Der idealtypische 20-Minuten-Zyklus**

Eine didaktisch strukturierte Darstellung der Autorezeptor-Rückkopplung in fünf Phasen:

- **Phase 1 (0–2 min) – Initialer Anstieg** Erhöhte neuronale Aktivität führt zur somatodendritischen 5-HT-Freisetzung im B7-Kompartiment.

- **Phase 2 (2–5 min) – Rezeptoraktivierung** Bindung von 5-HT an somatodendritische 5-HT1A-Autorezeptoren; Aktivierung der Gi/o-Proteine.

- **Phase 3 (5–12 min) – Effektorkaskade** Öffnung der GIRK-Kanäle, K⁺-Ausstrom, Hyperpolarisation; parallel Hemmung der Adenylatzyklase und cAMP-Reduktion.

- **Phase 4 (12–20 min) – Maximale Inhibition** Minimum der neuronalen Feuerrate; reduzierter 5-HT-Output im Projektionsgebiet.

- **Phase 5 (ab 20 min) – Termination** SERT-vermittelte Clearance; Rezeptor-Dephosphorylierung; Rückkehr zum Basalpotential.

Die Visualisierung der Phasendynamik (somatodendritische 5-HT-Konzentration vs. Feuerrate) nachfolgend. Die Phasenverschiebung von etwa 2–3 Minuten zwischen Feuerraten-Peak (Ende P1) und 5-HT-Konzentrations-Peak (Mitte P2) ist das physikalische Substrat der negativen Rückkopplung und die kinetische Quelle der Oszillationsfähigkeit.

![Zeitkonstanten](<images/fig2_autoreceptor_cycle_phases.png>){width=90%}

**Sensitivität und pathologische Modifikation**

Die 5-HT1A-Autorezeptor-Empfindlichkeit ist nicht konstant, sondern durch mehrere Mechanismen modifizierbar:

- **Stress-induzierte Desensibilisierung**: Längere unkontrollierte Stressbelastung führt zu einer reduzierten Autorezeptor-vermittelten Hemmung der serotonergen Neurone; der Effekt ist korticosteron-abhängig und nach Adrenalektomie nicht mehr nachweisbar (Laaris et al., 1997).
- **SSRI-induzierte Desensibilisierung**: Chronische Behandlung führt zur funktionellen Downregulation der Autorezeptoren – ein Mechanismus, der als zentral für die Wirklatenz der Antidepressiva gilt (Hjorth & Auerbach, 1994).
- **Supersensitivität bei 5-HT-Depletion**: In Tph2⁻/⁻-Mäusen zeigt sich eine etwa zweifache Linksverschiebung der Agonist-Konzentrations-Wirkungs-Kurve bei unveränderter maximaler Response – konsistent mit erhöhter Kopplungseffizienz zu GIRK-Kanälen und ohne Änderung der Rezeptordichte (Montalbano et al., 2018).
- **Transkriptionale Dysregulation**: Überexpression des 5-HT1A-Autorezeptors ist mit reduzierter serotonerger Neurotransmission, Depression und Suizidalität assoziiert; Repressor-Elemente (REST, Freud-1/Freud-2) regulieren die zellspezifische HTR1A-Expression (Albert et al., 2011).

Für den pathogenetischen Kontext ist insbesondere die Stress/Glucocorticoid-induzierte Modifikation relevant, da sie einen direkten Mechanismus für eine trait-artige Oszillator-Verschiebung bietet.

### **I.2 Oszillationsdynamik: empirische Evidenz und mathematisches Modell**

**Direkter Nachweis ultraslow-Oszillationen**

Die Existenz ultraslow-Oszillationen des extrazellulären Serotonins ist mittlerweile mit zwei unabhängigen Methodologien gesichert:

**Fast-Scan Controlled-Adsorption Voltammetry (FSCAV)** – die Hashemi-Gruppe dokumentierte in der CA2-Region des murinen Hippocampus robuste basale 5-HT-Oszillationen mit einer Periode von etwa 10 Minuten, die in vivo, jedoch nicht in vitro auftreten und von Geschlecht und chronischem Stressparadigma weitgehend unabhängig sind (Witt et al., 2022). Akute Escitalopram-Gabe verschiebt die mittlere Frequenz nach oben und reduziert die Amplitude. Bei höherer Abtastrate (Sample-Zeit ~14 s) zeigte sich eine dominante Oszillationsperiode von etwa 6.5 Minuten.

**GRAB5-HT3.0 Fiber Photometry** – mit dem genetisch kodierten G-Protein-gekoppelten 5-HT-Sensor konnten Cooper et al. (2024/2025) im hippocampalen CA1 ultraslow-Oszillationen (<0.05 Hz, entspricht Perioden >20 s) sowohl im Wach- als auch im NREM-Zustand nachweisen. Die Phase dieser Oszillationen differenziert Substates innerhalb der klassischen Verhaltenszustände: Sharp-Wave-Ripples häufen sich auf der absteigenden Phase, Mikroarousals und EMG-Peaks auf der aufsteigenden.

**DRN-Populationsaktivität** – korrespondierende ultraslow-Oszillationen der serotonergen Populationsaktivität im Raphe-Kern selbst wurden mit Einzelzellableitung (Mlinar et al., 2016) und Fiber Photometry (Kato et al., 2022) dokumentiert; Turi et al. (2024) ergänzten die Beobachtung im Gyrus dentatus während NREM.

**Autoreceptor-Kontrolle in mathematischen Modellen**

Die Arbeitsgruppe Best, Nijhout und Reed hat seit 2010, später in Kollaboration mit Hashemi, ein quantitatives Modell der serotonergen Terminal- und Somadynamik entwickelt. Die 2020-Version (Best, Duncan, Sadre-Marandi, Hashemi, Nijhout, Reed) berücksichtigt explizit, dass der Autorezeptor-Effekt **nicht instantan** und auch nach Rückkehr der extrazellulären 5-HT-Konzentration zur Baseline noch anhaltend wirksam ist. Diese Verzögerung ist in Differentialgleichungs-Systemen als Delay-Term τ oder als mehrstufige kinetische Kaskade implementiert.

Für den vorliegenden Kontext genügt die kompakte Notation:

> dS/dt = f(Firing) − k_clear · S
> dFiring/dt = −g(S(t − τ)) · Firing + Input

Wobei *S* die extrazelluläre 5-HT-Konzentration, *Firing* die B7-Feuerrate, *τ* die effektive Verzögerung der Autorezeptor-Rückwirkung und *g* eine sättigende (z. B. Hill-förmige) Aktivierungsfunktion des Autorezeptors bezeichnet.

Systeme dieser Struktur zeigen bei hinreichend großem τ·Gain-Produkt eine **Hopf-Bifurkation** in einen Grenzzyklus. Die Eigenperiode liegt im Bereich 2τ–4τ; Phasenform und Harmonik hängen von der Steilheit von *g* und der Nichtlinearität der Clearance ab.

**Zustandsabhängigkeit**

Die absolute Feuerrate der 5-HT-Neurone ist stark vigilanzabhängig: am höchsten im aktiven Wachzustand, reduziert im NREM, minimal (bis 0) im REM. Der ultraslow-Oszillationscharakter bleibt jedoch in beiden Wach- und NREM-Zuständen bestehen, mit phasenabhängiger Substate-Struktur. Damit ist der B7-Oszillator nicht ein REM-gebundener Rhythmus, sondern ein kontinuierlich verfügbarer Hintergrundtakt des serotonergen Systems.

**HRV-Frequenzbänder: Standard und erweiterte Systematik**

**Standardklassifikation (Task Force 1996 / Shaffer & Ginsberg 2017)**

| Band | Frequenzbereich | Perioden | Dominante Quelle |
|---|---|---|---|
| HF | 0.15–0.40 Hz | 2.5–6.7 s | Respiratorische Sinusarrhythmie, vagal |
| LF | 0.04–0.15 Hz | 6.7–25 s | Baroreflex, gemischt vagal/sympathisch |
| VLF | 0.0033–0.04 Hz | 25–300 s | Intrinsisches kardiales Nervensystem, Thermoregulation, RAAS |
| ULF | ≤ 0.003 Hz | 5 min – 24 h | Zirkadiane, neuroendokrine, Baroreflex-Integrale |

Die ULF-Messung erfordert per Konvention mindestens 24-h-Ableitungen; kürzere Aufzeichnungen erlauben keine saubere spektrale Trennung der Langzeit-Anteile. VLF ist in der Mortalitätsprognose (post-MI, Herzinsuffizienz) klinisch stärker assoziiert als LF oder HF.

**Sub-Banding (ULF1, ULF2)**

Eine feinere Unterteilung des ULF-Bandes in ULF1 und ULF2 ist keine Konvention der Task-Force-Nomenklatur, aber in spezialisierten Analysepipelines (z. B. Kubios, individualisierte Metabase-Abfragen) verwendbar. Eine typische Aufteilung ist:

- **ULF1**: 0.00001–0.001 Hz (Perioden ~16 min bis >24 h) – zirkadiane und langsame homöostatische Schleifen (HPA-Achse, Thermoregulation, Baroreflex-Integrale)
- **ULF2**: 0.001–0.0033 Hz (Perioden ~5–16 min) – ultradiane Zeitskala; hier erwartet sich die serotonerge Oszillator-Signatur

Die genauen Bandgrenzen sind implementierungsabhängig; für die pathogenetische Interpretation ist die Erfüllung der Bedingung **P ≈ 2τ–4τ ⇒ Period ∈ [20, 80] min** entscheidend, das Band muss diese Perioden umfassen.

**Methodologische Konsequenz: Sichtbarkeit im VLF**

Bei Standard-HRV-Pipelines mit kurzen Aufzeichnungsfenstern oder ohne dediziertes ULF-Sub-Banding landet die gesamte Spektralenergie unterhalb von 0.04 Hz faktisch im VLF-Topf. Ein in ULF2 zu erwartender Peak ist dann im berichteten VLF-Wert "eingemischt". Zwei weitere Mechanismen verstärken diese VLF-Sichtbarkeit:

1. **Harmonische Komponenten**: Der Autorezeptor-Zyklus ist asymmetrisch (steiler Anstieg, plateauartige Inhibition, exponentielle Clearance). Die asymmetrische Wellenform wurde auch von Cooper et al. (2024/2025) für die Hippocampus-5-HT-Oszillation direkt beschrieben. Eine Fourier-Zerlegung erzeugt diskrete Oberwellen bei Vielfachen der Grundfrequenz. Für eine 20-min-Grundperiode liegen die 2.–5. Harmonischen bei Perioden von 10, 6.7, 5 und 4 Minuten – die höheren Harmonischen (4–5 min) fallen per Definition ins VLF-Band.

2. **Nichtlineare Kopplungseffekte**: Die Projektion der serotonergen Oszillation auf die RR-Zeitreihe ist keine lineare 1:1-Abbildung, sondern geht durch zentrale autonome Netzwerke (siehe Abschnitt 6). Dies kann frequenzabhängige Modulations- und Amplitudeneffekte erzeugen, die die Grundfrequenz entfernen oder verschieben.

**Die Sichtbarkeit der Autorezeptor-Dynamik im VLF ist daher nicht ein Widerspruch zur modellierten Grundfrequenz in ULF2, sondern deren erwartete Manifestation unter realistischen Methodik-Bedingungen.** Ein gleichzeitig berichteter Peak in ULF2 und VLF bei gleichzeitigem Fehlen in LF/HF ist mit einem harmonisch reichen, tieffrequenten Einzelprozess kompatibel.

### **I.3 Zentrale autonome Kopplungswege: vom B7 zum RR-Intervall**

Damit eine oszillatorische Aktivität des B7-Kerns im HRV-Spektrum sichtbar werden kann, bedarf es eines definierten Kopplungspfades zur kardialen autonomen Kontrolle. Die relevanten anatomisch-funktionellen Pfade sind:

- **DRN → Nucleus raphe obscurus / raphe pallidus**: intra-raphale serotonerge Projektionen modulieren die prä-sympathische und prä-parasympathische medulläre Ausgangsebene. Der Raphe pallidus ist eine Schlüsselstation für die thermoregulatorische sympathische Ausgangsbahn.
- **DRN → NTS (Nucleus tractus solitarii)**: serotonerge Afferenzen zum NTS modulieren die baroreflex-vermittelte vagale und sympathische Gewichtung; direkte 5-HT1A- und 5-HT2-Effekte im NTS sind dokumentiert.
- **DRN → DMNX (dorsaler Vaguskern) / Nucleus ambiguus**: direkte und indirekte Einflussnahme auf den kardialen Vagus.
- **DRN → Hypothalamus (PVN, SCN, LH)**: Modulation der HPA-Achse (PVN-CRH-Ausgang), zirkadianer Kopplung (SCN) und der orexinergen/hypothalamischen Aktivierungssysteme. Denuelle et al. (2007) und Stankewitz & May belegten die präiktale Hypothalamus-Aktivierung bei spontanen Migräneattacken.
- **DRN → PAG (periaquäduktales Grau)**: absteigende nozizeptive Kontrolle; im ictalen Zustand bei Migräne persistierend aktiviert (Weiller et al., 1995).

Die autonome Konvergenz erfolgt damit über mindestens drei Ebenen: (a) direkte medulläre Modulation, (b) hypothalamische Integration, (c) Koordination mit anderen Hirnstamm-Kernen (LC noradrenerg, PAG). Eine B7-Oszillation projiziert daher nicht auf einen einzelnen, sondern auf einen verteilten Satz autonomer Ausgangssysteme mit zum Teil unterschiedlichen Zeitkonstanten – ein struktureller Grund für die Erzeugung harmonisch reicher, mehrmaliger Frequenzkomponenten im HRV-Spektrum.

**Migräne-Pathogenese: Kontextualisierung**

**Der Hirnstamm als persistenter "Generator"**

Die bildgebende Evidenz für eine Hirnstamm-zentrierte Migräne-Pathogenese ist konsistent. Weiller et al. zeigten 1995 in einer PET-Studie während spontaner Migräneattacken eine persistierende Hirnstamm-Aktivierung, die auch nach Sumatriptan-induzierter vollständiger Kopfschmerzremission bestehen blieb – im Unterschied zu den kortikalen Aktivierungen. Dieses Muster wurde später repliziert und erweitert: Afridi et al. (2005) bestätigten die Hirnstamm-Aktivierung, Denuelle et al. (2007) ergänzten die Hypothalamus-Aktivierung, die ebenfalls nach Triptan-Gabe persistierte.

**Serotonerger Transporter bei Migräne**

PET-Studien mit [¹⁸F]FP-CIT dokumentierten eine erhöhte Hirnstamm-SERT-Verfügbarkeit bei Migränepatientinnen im kopfschmerzfreien Intervall im Vergleich zu Kontrollen, interpretiert als Indikator reduzierter serotonerger Neurotransmission im Interiktal-Zustand (Jeong et al., 2016). Zusätzlich zeigte sich eine Korrelation der Attackenschwere mit der SERT-Bindung.

**Prodromalphase als oszillatorischer Zustandswechsel**

Eine einflussreiche Konzeption versteht Migräne als **zyklisches Hirnsyndrom** mit spontanen Netzwerk-Oszillationen, die Schwellenverschiebungen erzeugen. Spontane Oszillationen komplexer Netzwerke mit Beteiligung von Hypothalamus, Hirnstamm und dopaminergen Systemen führen zu Veränderungen kortikaler und subkortikaler Aktivität, verändern Suszeptibilitätsschwellen und tragen nicht nur zum Beginn, sondern auch zur Terminierung der Kopfschmerzphase bei (Schulte & May, 2017).

Dieses Modell ist mit dem B7-Autorezeptor-Oszillator unmittelbar kompatibel:
- Die rostrale DRN-Aktivität ist im Migräne-Generator-Konzept zentral mit involviert.
- Spontane Oszillationen entstehen intrinsisch aus delayed-feedback-Systemen.
- Die Schwellenverschiebung (gain change) ist ein natürliches Produkt einer Hopf-Bifurkation im Autorezeptor-System.

**Thesen zur prodromalen HRV-Signatur**

Aus der Konvergenz der obigen Kapitel lassen sich die folgenden prüfbaren Thesen formulieren:

> **These 1**: Der B7-Autorezeptor-Oszillator ist im interiktalen Zustand im gedämpften Regime; im Prodromalfenster tritt er durch Gain-Erhöhung oder τ-Verschiebung in einen kohärenten Grenzzyklus.

> **These 2**: Die kohärente Grenzzyklus-Aktivität manifestiert sich als schmaler, amplitudenstarker Spektralpeak in ULF2 (Perioden 5–16 min) mit charakteristischer harmonischer Verbreitung in das VLF-Band (über die 3.–5. Harmonische der asymmetrischen Zyklusform).

> **These 3**: Der Peak ist spezifisch für den oszillatorischen Modus und nicht durch allgemeine Sympathikus-Aktivierung erklärbar; Letztere würde primär LF erhöhen und alle langsameren Bänder breit anheben, nicht schmal in ULF2 kanalisieren.

> **These 4**: Die Peak-Schärfe (Q-Faktor f_peak/Δf_3dB) unterscheidet echte Grenzzyklus-Aktivität (Q > 5) von 1/f-Rauschen (Q < 2) und ist daher ein quantitativer Diskriminator gegenüber Artefakten.

> **These 5**: Wirksame zentrale pharmakologische Intervention (z. B. DPH, Ergot-Alkaloide, Triptane) entkoppelt die oszillatorische Kohärenz, nicht notwendigerweise die Oszillator-Amplitude. Entsprechend ist die **ULF2-Varianz (ULF2-CV)** ein sensitiverer Interventionsmarker als der ULF2-Mittelwert; ein gleichzeitiger Anstieg von ULF1 wäre konsistent mit Wiederherstellung der langsameren homöostatischen Bandbreite.

**Epistemische Einordnung**

Diese Synthese verbindet drei Literaturlinien:

1. **Solide etabliert**: Anatomie und Signalkaskade des 5-HT1A-Autorezeptors, die HRV-Band-Standardnomenklatur, die PET-Befunde zur persistierenden Hirnstamm- und Hypothalamus-Aktivierung bei Migräne, die Existenz ultraslow-5-HT-Oszillationen.

2. **Modellbasiert, plausibel**: Die mathematische Autorezeptor-Dynamik (Best/Nijhout/Reed-Linie) mit τ im 10–20-min-Bereich; die Oszillator-Interpretation der Migräne-Pathogenese (Schulte/May-Linie).

3. **Inferenz, nicht direkt belegt**: Die explizite Kopplung einer B7-Autorezeptor-Grenzzyklus-Aktivität auf das ULF2-HRV-Band als prodromaler Biomarker. Diese Brücke ist physiologisch plausibel, in der Primärliteratur jedoch nicht als etabliertes Messparadigma verankert. Die Brücke ist das Arbeitsgebiet der nachgelagerten Datenanalyse, nicht ein Zitat.

Die Nützlichkeit dieser Konzeption bemisst sich an ihrer prospektiven Vorhersagekraft: ob der vorhergesagte ULF2-Peak tatsächlich prodromal und spezifisch ist, ob er pharmakologisch interpretierbar moduliert wird, und ob er zwischen Individuen konsistent bleibt.

### **I.4 Zustandsklassifikation: B7/B8-Beteiligung aus dem Spektralprofil**

Die minutenweise Klassifikation des autonomen Zustands anhand der relativen Verteilung von HF, LF und VLF erlaubt eine Zuordnung zur Aktivität der Raphekerne B7 und B8. Die folgende Taxonomie operiert auf den relativen Anteilen am Gesamtspektrum (Total Power = LF + HF + VLF) und ist als heuristische Zuordnung zu verstehen, nicht als direkte Messung der Kernaktivität.

**Zuordnungslogik:**

HF (0.15–0.4 Hz) wird als B8-Proxy behandelt: respiratorische Sinusarrhythmie, primär vagal, über den parasympathischen Pfad moduliert. LF (0.04–0.15 Hz) wird als B7-Proxy behandelt: Baroreflex-Schleife mit dominanter sympathischer Komponente, vermittelt über den DRN→LC→sympathischen Pfad. VLF (<0.04 Hz) operiert auf der Zeitskala, auf der die B7-Amplitudeninstabilität sichtbar wird — die Hüllkurve des Autoreceptor-Feedback-Loops.

**Klassifikationsregeln:**

| Zustand | Kriterium | B8 | B7 | Interpretation |
|---|---|---|---|---|
| B8-dominant | HF/Total > 0.4, LF/Total < 0.25 | aktiv | supprimiert | Physiologischer NREM, saubere vagale Modulation |
| B7-dominant | LF/Total > 0.4, HF/Total < 0.25 | supprimiert | aktiv | Sympathischer Drive ohne vagale Gegenkraft |
| Beide aktiv | HF/Total > 0.3, LF/Total > 0.3 | aktiv | aktiv | Kohärente duale Modulation |
| Interferenz | VLF/Total > 0.5 | variabel | variabel | B7-Amplitudeninstabilität auf VLF-Zeitskala |
| Both off | Total < 3 ms² | pausiert | pausiert | ANS-Eigenzeit, keine serotonerge Modulation |
| Mixed | keines der obigen | undeterminiert | undeterminiert | Übergangszustand oder unzureichende Trennung |

**Einschränkung:** Die Klassifikation erfordert echte Beat-to-Beat-Intervalle (IBI). PPG-basierte Minutenmittel-HR (z. B. Xiaomi Smart Band) liefern keine saubere Spektralanalyse in diesen Bändern. Die empirische Validierung verwendet Coospo-Brustgurt-Daten mit 5-Minuten-Fensterspektralanalyse.

**Amplitudenmodell vs. Phasenoffset-Modell**

Die ursprüngliche Modellarchitektur postulierte zwei unabhängige Oszillatoren (B7, B8) mit driftendem Phasenoffset als Quelle der ~4-Tage-Schwebung. Diese Konzeption wurde auf Grundlage der empirischen Datenanalyse revidiert.

**Argument gegen das Phasenoffset-Modell:** In der seriellen Architektur SCN↔B8↔B7 hat B7 keine unabhängige Taktquelle. Er empfängt sein Timing von B8 über die SCN-vermittelte zirkadiane Kopplung. Zwei Oszillatoren mit driftendem Phasenoffset setzt voraus, dass beide eine eigene Taktquelle besitzen — B7 hat keine.

**Amplitudenmodell:** Was variiert, ist der B7-Gain — die Stärke, mit der B7 auf den B8-Input antwortet. Dieser Gain wird durch den 5-HT1A-Autoreceptor-Feedback-Loop auf einer eigenen Zeitskala moduliert (Hit 1). Wenn der Autoreceptor-Feedback-Loop über Tage zykliert, entsteht eine Amplitudenmodulation mit ~4-Tage-Periodizität. In den HRV-Daten erscheint dies als Variation der B7-dominierten Spektralkomponenten (LF, VLF), während die B8-Komponente (HF) als Baseline stabil bleibt.

**Konsequenz für die Intervention:** Im Phasenoffset-Modell müsste man resynchronisieren — mechanistisch unklar wie. Im Amplitudenmodell muss man den B7-Gain stabilisieren oder die Downstream-Kaskade der Gain-Instabilität puffern. DPH adressiert empirisch Letzteres.

**Epistemischer Status:** Modellspezifisch, korrigiert aus den Daten der Session April 2026. Die Revision erfordert Änderungen überall im Modelldokument, wo „Phasenoffset" und „destruktive Interferenz" steht — korrekt ist „B7-Amplitudeninstabilität" und „Gain-Oszillation".

**Typ-1 vs. Typ-2 Tiefschlaf: Dissoziation von Bewegungsunfähigkeit und autonomer Modulation**

Die simultane Aufzeichnung von Beschleunigungs-basiertem Sleep-Staging (Xiaomi Smart Band 9) und IBI-basierter Spektralanalyse (Coospo-Brustgurt) offenbart zwei distinkte Tiefschlaf-Modi, die im Bewegungssensor identisch erscheinen:

**Typ 1 — Modulierter Tiefschlaf:** HR 56–60, pNN50 50–60%, HF 25–35 ms², LF 18–22 ms². Beide Oszillatoren aktiv, B8-dominanter vagaler Drive, starke respiratorische Sinusarrhythmie. Entspricht dem physiologischen SWS-Lehrbuch.

**Typ 2 — Amodaler Tiefschlaf:** HR 64–72, pNN50 < 5%, alle Bänder < 3 ms². Bewegungsunfähigkeit bestätigt (Tracker meldet „Deep"), aber das ANS zeigt keine Oszillation. Das Herz schlägt metronomisch gleichförmig.

**Modellinterpretation:** Typ 1 = B8 aktiv, B7 korrekt supprimiert → saubere vagale Durchmodulation mit RSA. Typ 2 = beide Kerne pausiert → thalamokortikaler Shutdown erzeugt Bewegungsunfähigkeit, aber die autonome Modulation fehlt. Die HR settelt auf dem sympathischen Grundtonus ohne aktive serotonerge LC-Suppression — deshalb 64–72 statt 56.

**Konsequenz:** Beschleunigungs-basiertes Sleep-Staging und autonome Modulationsqualität sind orthogonale Dimensionen. Typ-2-Tiefschlaf hat die kortikale Abschaltung, aber nicht den autonomen Drive, der die glymphatische Clearance-Pumpe antreibt. Dies erklärt, warum subjektiv erholsamer Schlaf und Tracker-gemessene Schlaftiefe dissoziieren können.

**Beobachtete Häufigkeit:** Typ-2-Episoden treten reproduzierbar in der zweiten Nachthälfte auf (nach ~4–5 Stunden), typischerweise nach einem Hochmodulations-Zyklus und gefolgt von einem Interferenz-Rebound. Die zweite Nachthälfte ist regenerativ gescheitert — der Organismus kommt seit der Kindheit mit der Regenerationskapazität der ersten 5 Stunden aus. „Kurzschläfer" ist eine Fehlattribution: der Organismus hat gelernt, dass Weiterschlafen keinen Regenerationsmehrwert liefert.

**DPH als Kaskadenpuffer: Empirische Befunde**

Diphenhydramin (DPH) wurde ursprünglich im Modell als B7-Gain-Modulator konzeptualisiert, gestützt auf Crawford et al. (2013): H1-Blockade im DRN supprimiert selektiv B7. Die empirische Testung über vier Nächte mit IBI-Spektralanalyse ergibt ein differenzierteres Bild:

**Befundlage aus vier Nächten (16.–20. April 2026):**

| Nacht | Substanz | B7-dom% | VLF% | HR mean | Interpretation |
|---|---|---|---|---|---|
| N1 (16. Apr) | DPH | 2.4 | 42.0 | 64.6 | B7 niedrig — Zyklusposition, nicht DPH |
| N2 (18. Apr) | Desloratadin | 5.1 | 42.4 | 67.1 | Unbehandelte Baseline (2. Gen. penetriert BHS nicht) |
| N3 (19. Apr) | DPH + Naratriptan | 0.9 | 41.6 | 67.8 | Natürlicher B7-Kollaps, Kaskade abgefangen |
| N4 (20. Apr) | DPH | 8.6 | 45.4 | — | B7 feuert durch trotz DPH |

**Schlussfolgerungen:**

1. DPH moduliert den B7-Gain nicht messbar. N4 zeigt den höchsten B7-Dominanz-Wert aller vier Nächte unter DPH. N1 hatte niedrige B7-Dominanz nicht wegen DPH, sondern weil B7 zufällig an diesem Zyklustag niedrig war.
2. Der VLF-Fingerabdruck (42 ± 1%) ist über alle vier Nächte stabil — keine der Interventionen hat die Grunddynamik des Autoreceptor-Feedback-Loops verändert.
3. DPH puffert die Downstream-Kaskade der B7-Instabilität, nicht die Instabilität selbst. Die N3-Erfahrung (subjektive post-iktale Klarheit ohne Anfall) zeigt: der B7-Kollaps fand statt (65 min Typ-2), aber die CSD-Kaskade und ANS-Destabilisierung wurden abgefangen.
4. Die subjektive Schlafqualität unter DPH dissoziiert von der spektralen Signatur: DPH verbessert das Erleben einer gegebenen B7-Zyklusposition, verändert aber nicht die Position selbst.

**DPH als Tagesintervention bei Prodromen:** Ein einzelner Datenpunkt (20. April, DPH um 16:00 bei laufendem Prodrom) zeigt eine kurze vasomotorische Reaktion (Hitzewelle am VLF-Nadir, 16:37) mit subjektiver Klarheit, aber ohne spektrale Normalisierung — LF/HF steigt nach dem initialen Dip weiter an. Die subjektive Erfahrung dissoziiert von der spektralen Messung. Der kortikale H1-Effekt (Rauschreduktion) und der autonome Effekt (ANS-Kaskade) sind unabhängige Pfade.

**PFC-Ressourcenkonkurrenz-Modell**

Die Beobachtung, dass DPH-induzierte sympathische Kaskadenpufferung unter laufendem LDX zu subjektiver kognitiver Klarheit führt, lässt sich als Ressourcenkonkurrenz modellieren:

Im prodromalen Zustand stabilisiert LDX den DA/NA-Pfad für Kognition (MD-Thalamus→PFC), muss aber gleichzeitig Ressourcen in die NTS-Suppression investieren (PFC→PAG→NTS), um die sympathische Kaskade kortikal zu kompensieren. Die kognitive Kapazität wird für ANS-Kontrolle verbrannt.

DPH bricht die sympathische Nachentladung über einen separaten Pfad (H1-Blockade). Der PFC muss den NTS nicht mehr aktiv suppressen. Die gesamte LDX-Kapazität steht für Kognition zur Verfügung. Die resultierende Klarheit ist nicht DPH-Wirkung, sondern LDX-Wirkung, die zuvor durch Bandbreitenbelegung maskiert war.

Dieses Modell erklärt sowohl die N3-Erfahrung (post-iktale Klarheit am Folgetag trotz normaler LDX-Dosis) als auch die akute Tagesintervention (Klarheit 40 Minuten nach DPH bei laufendem LDX). Der Mechanismus ist identisch: B7-Störsignal reduziert → PFC-Ressourcen frei.

**Der 20-Minuten-VLF-Rhythmus als direkte Autorezeptor-Signatur**

Die minutenweise VLF-Analyse des prodromalen Tages (20. April 2026, 10:00–20:00 Uhr) zeigt eine reguläre Oszillation mit einem medianen Inter-Peak-Intervall von 20 Minuten (Mean 23 min). Dieser Rhythmus ist über den gesamten Aufzeichnungszeitraum nachweisbar, mit Amplitudenmodulation aber stabiler Periodizität.

Die 20-Minuten-Periodizität fällt exakt in den vorhergesagten Bereich des 5-HT1A-Autorezeptor-Grenzzyklus (T ≈ 2τ–4τ bei τ = 10–20 min, Abschnitt I.1). Damit ist der VLF-Rhythmus ein Kandidat für die direkte HRV-basierte Messung der Autorezeptor-Rückkopplung, wie in These 2 (Abschnitt I.3) postuliert.

**Beobachtete Substruktur:** Nach dem VLF-Spike um 16:00 Uhr (VLF = 9262 ms²) zeigt sich eine transiente Frequenzverdopplung — Inter-Peak-Intervalle von 7–10 Minuten statt 20 Minuten. Diese Verdopplung ist konsistent mit einem überschwingenden Regelkreis, der sich nach einer großen Perturbation über mehrere verkürzte Zyklen restabilisiert.

**Epistemischer Status:** Die 20-Minuten-Periodizität ist ein einzelner Datenpunkt (n=1, ein Tag). Die Stabilität über Tage und Nächte, die Inter-Individuen-Variabilität und die pharmakologische Modulierbarkeit der Periodizität sind noch zu prüfen. Die Übereinstimmung mit der modellierten Autorezeptor-Kinetik ist bemerkenswert, aber nicht beweisend — Thermoregulation und andere VLF-Quellen müssen differentialdiagnostisch ausgeschlossen werden.

### **I.5 Zweidimensionale Zustandsrepräsentation: Dominanz und Interferenz**

Die kategoriale Zustandsklassifikation (Abschnitt I.4) quantisiert den Zustandsraum in sechs diskrete Bins und verliert dabei Graduierungsinformation. Eine bessere Kompression der drei Spektralbänder in einen zweidimensionalen kontinuierlichen Zustandsraum ergibt sich aus zwei orthogonalen Achsen, die die autonome Output-Balance und die Oszillator-Stabilität separat erfassen.

**Achse 1: Dominanz (autonome Balance)**

```
dominanz(t) = (HF(t) - LF(t)) / (HF(t) + LF(t))
```

Der Wertebereich reicht von -1 (reines LF, maximale sympathische Dominanz) bis +1 (reines HF, maximale vagale Dominanz). Null entspricht dem Gleichgewicht HF = LF. Die Achse misst nicht direkt die Aktivität der Raphekerne B7 oder B8, sondern die autonome Output-Balance — den Nettobeitrag des sympathischen vs. parasympathischen Arms zum kardialen Spektrum. Im Schlaf steigt die Dominanz nicht weil B8 stärker feuert (serotonerge Neurone reduzieren im NREM), sondern weil B7s sympathischer Drive wegfällt und der vagale Grundtonus überwiegt. Die Achsenbeschriftung ist daher korrekt als „+vagal / -sympathisch" zu lesen; die B7/B8-Attribution ist eine Modellinterpretation, keine direkte Messung.

Division-by-Zero-Absicherung: Wenn HF + LF = 0 und Total ≥ TOTAL_MIN, dann dominanz = 0.0 (reines VLF, keine LF/HF-Aussage möglich).

**Achse 2: Interferenz (Oszillator-Stabilität)**

```
interferenz(t) = VLF(t) / (LF(t) + HF(t) + VLF(t))
```

Der Wertebereich reicht von 0 (kein VLF-Anteil, maximale Kongruenz der schnellen Oszillatoren) bis 1 (reines VLF, maximale Divergenz). Im Amplitudenmodell ist dies das Maß für die Instabilität des B7-Autoreceptor-Feedback-Loops auf der VLF-Zeitskala. Der empirisch ermittelte individuelle Baseline-Wert liegt bei ~0.42 (Trait-Fingerabdruck über vier Nächte stabil, Abschnitt I.6).

**Cutoff-Regel:** Wenn Total(t) < TOTAL_MIN (Default: 3.0 ms²), werden beide Achsen auf NULL gesetzt. Unterhalb dieser Schwelle ist jede Ratio-Berechnung rauschgetrieben und nicht interpretierbar. TOTAL_MIN ist skalierungsabhängig und muss bei geänderter App-Konfiguration oder Fenstergröße proportional angepasst werden.

**Rückabbildung auf kategoriale Klassifikation:**

Die Sechs-Klassen-Taxonomie aus Abschnitt I.4 ist ein Spezialfall der kontinuierlichen Darstellung. Die Schwelle dominanz = ±0.23 entspricht dem Punkt, an dem HF/Total = 0.4 bei LF/Total = 0.25 erreicht wird: (0.4 - 0.25) / (0.4 + 0.25) = 0.231. Die Interferenz-Schwelle bei 0.5 bleibt identisch. Damit gilt: B8-dominant = dominanz > 0.23 bei interferenz < 0.5; B7-dominant = dominanz < -0.23 bei interferenz < 0.5; Interferenz-Zone = interferenz ≥ 0.5; Balance-Zone = |dominanz| ≤ 0.23 bei interferenz < 0.5.

**Empirische Validierung: Phasenraum-Darstellung**

Die Darstellung des 19. April 2026 (24-Stunden-Aufzeichnung, Nacht + Tag) im Phasenraum (X = dominanz, Y = interferenz) zeigt zwei scharf getrennte Cluster:

- **Nacht (00:00–06:30):** Dominanz +0.1 bis +0.8, Interferenz 0.1 bis 0.7. Der Cluster liegt im vagal-dominierten Quadranten mit variabler Interferenz. Die intranight Oszillation zwischen B8-Plateaus (unten rechts: hohe Dominanz, niedrige Interferenz) und VLF-Bursts (oben Mitte: mittlere Dominanz, hohe Interferenz) ist als vertikale Streuung sichtbar.

- **Tag (07:00–23:59):** Dominanz -0.6 bis -0.9, Interferenz 0.3 bis 0.8. Ein dichter Cluster im sympathisch-dominierten Quadranten mit durchgehend erhöhter Interferenz. Bemerkenswert: die Variation liegt fast ausschließlich auf der Interferenz-Achse — die Dominanz-Dimension ist komprimiert.

- **Nap (13:09–13:50):** Der einzige Brückenpunkt. Dominanz wandert von -0.5 durch Null bis +0.15 — der Moment, wo der sympathische Drive kurz nachlässt. Gleichzeitig steigt die Interferenz auf 0.82 — das Maximum des gesamten Tages. Der Nap-Kollaps ist im Phasenraum der Punkt maximaler Interferenz bei minimaler Dominanzbindung.

**Prodromale Zustandsraum-Kompression**

Die Analyse über mehrere aufeinanderfolgende Tage (16.–20. April) zeigt eine progressive Kompression der Dominanz-Achse auf -1 während der Wachstunden. Am 19. April ist die Dominanz am unteren Rand verankert (mean -0.68, median -0.68, std 0.24) — das System hat nur noch einen effektiven Freiheitsgrad (Interferenz), die Dominanz-Dimension ist kollabiert.

Dieses Phänomen ist die Tagesauflösung des B7-Gain-Ramps im Phasenraum: der progressive Verlust der Dominanz-Varianz über Tage ist die prodromale Signatur, nicht ein einzelner Spike.

**Prodromalmetrik: B7-Exposure und B7-Risk**

Aus der zweidimensionalen Darstellung lassen sich zwei quantitative Prodromalmetriken ableiten:

**B7-Exposure** — das Integral der Dominanz-Exkursion unter einem Schwellenwert θ, berechnet über die Wachminuten:

```
b7_exposure = Σ max(0, θ - dominanz(t))    für alle Wachminuten t mit dominanz(t) < θ
```

Mit θ = -0.6 (empirisch kalibriert: -0.6 entspricht LF/HF = 4.0, deutliche sympathische Übersteuerung). Eine Minute bei dominanz = -0.95 trägt 0.35 bei, eine bei -0.65 nur 0.05. Dies gewichtet tiefe Exkursionen überproportional — konsistent mit der Annahme, dass der physiologische Schaden nichtlinear mit der Dominanz-Tiefe skaliert.

**Geltungsbereich:** Beide Metriken sind ausschließlich auf die Wachstunden (z. B. 07:00–23:00 oder ab LDX-Einnahme bis Schlaf) zu berechnen. Die nächtliche Dominanzverschiebung Richtung +vagal ist physiologisch und würde den prodromalen Effekt verdecken — konsistent mit der Tatsache, dass B7 im NREM seine Feuerrate physiologisch reduziert und damit nicht informativ für den Gain-Zustand ist.

**Abgrenzung zur bestehenden Literatur**

Die zweidimensionale Zustandsrepräsentation (Dominanz × Interferenz) hat kein direktes Vorbild in der publizierten Schlaf- oder Migräneforschung. Die bestehende Literatur lässt sich in drei Ansätze gliedern, die jeweils anders ansetzen:

**(1) LF/HF-Ratio als skalarer sympathovagaler Index.** Die gesamte Migräne-HRV-Literatur (Zhang et al. 2021; Chuang et al. 2023; Mosek et al. 1999) verwendet die LF/HF-Ratio als eindimensionalen Marker der autonomen Balance. Dies entspricht funktionell der hier definierten Dominanz-Achse, jedoch ohne Normierung auf den Bereich [-1, +1] und ohne Trennung einer zweiten, orthogonalen Dimension. VLF wird in diesen Studien als separater Parameter mitberichtet, aber nie als eigenständige Achse eines interpretierten Zustandsraums operationalisiert. Die Frage *wie dominant ist der sympathische Arm* wird nicht von der Frage *wie instabil ist das System* getrennt.

**(2) Multivariate ML-Klassifikatoren für HRV-basiertes Sleep-Staging.** Die Schlaf-HRV-Literatur (Radha et al. 2019; Xiao et al. 2013; Mendez et al. 2010) verwendet bis zu 41 HRV-Features als Input für neuronale Netze, Random Forests oder Hidden-Markov-Modelle. Mendez et al. erwähnen explizit einen „phase space of HRV parameters" — gemeint ist jedoch der mathematische Phasenraum der RR-Zeitreihe selbst (Poincaré-Plots, Return Maps), nicht ein physiologisch interpretierter Zustandsraum der autonomen Balance. Die Features dienen als Input für Black-Box-Klassifikatoren; die Dimensionsreduktion erfolgt durch den Algorithmus, nicht durch eine interpretierbare Kompression.

**(3) Gruppenmittelwerte iktal vs. interiktal.** Alle publizierten Migräne-HRV-Studien vergleichen Gruppenmittelwerte zwischen Zuständen: iktal vs. interiktal vs. Kontrolle. Keine untersucht eine longitudinale intra-individuelle Trajektorie im Zustandsraum über Tage oder über einen Anfallszyklus. Die Konzeption, dass die prodromale Signatur nicht ein Schwellenwert eines einzelnen Parameters ist, sondern eine progressive Kompression des Zustandsraums (Varianzreduktion der Dominanz-Achse über Tage), existiert in der Primärliteratur nicht.

**Drei Alleinstellungsmerkmale der vorliegenden Methodik:**

Erstens: die Kompression von drei Spektralbändern (LF, HF, VLF) in zwei interpretierte, orthogonale Achsen — autonome Balance (Dominanz) und Oszillator-Stabilität (Interferenz) — statt drei uninterpretierter absoluter Power-Werte oder einer einzelnen Ratio. Die Trennung der Stabilitätsfrage von der Balancefrage ist der konzeptuelle Kern.

Zweitens: die Phasenraum-Darstellung als minutenweise Trajektorie über Stunden und Tage statt als Gruppenmittelwert eines Querschnittsdesigns. Die prodromale Dynamik wird als Pfad durch den Zustandsraum sichtbar, nicht als Punktschätzer.

Drittens: die Ableitung eines Exposure-Integrals (b7_risk) als gewichtete Metrik, die Tiefe und Dauer der sympathischen Exkursion. Kumulative Metriken dieser Art sind in der HRV-Forschung nicht etabliert; die Standardpraxis verwendet Epochenmittelwerte oder Gesamtnacht-Aggregate.

Die methodische Einfachheit der Transformation — zwei Divisionen aus Standardparametern, keine Modellkalibrierung, keine Trainingsphase — steht in Kontrast zur konzeptuellen Neuheit der Interpretation. Die Achsen sind nicht neu; ihre orthogonale Kombination und die Phasenraum-Visualisierung als diagnostisches Werkzeug sind es.

**Referenzen (Abgrenzung):**
- Zhang M, et al. (2021). *Heart Rate Variability Analysis in Episodic Migraine: A Cross-Sectional Study.* Front Neurol 12: 647092.
- Chuang CH, et al. (2023). *Abnormal heart rate variability and its application in predicting treatment efficacy in patients with chronic migraine.* Cephalalgia 43(11): 03331024231206781.
- Mosek A, et al. (1999). *Autonomic Dysfunction in Migraineurs.* Headache 39: 108–117.
- Radha M, et al. (2019). *Sleep stage classification from heart-rate variability using long short-term memory neural networks.* Sci Rep 9: 14149.
- Xiao M, et al. (2013). *Sleep stages classification based on heart rate variability and random forest.* Biomed Signal Process Control 8: 624–633.
- Mendez MO, et al. (2010). *Sleep staging classification based on HRV: time-variant analysis.* Conf Proc IEEE Eng Med Biol Soc 2009: 5862–5865.

**Epistemischer Status:** Die Zweidimensionale Zustandsrepräsentation ist eine datengetriebene Kompression, keine modelltheoretische Ableitung. Die Achsen sind Verhältnisse der drei Standard-HRV-Spektralbänder und damit methodologisch gesichert. Die Interpretation als B7/B8-Proxy ist modellspezifisch. Der Schwellenwert θ = -0.6 ist aus einem einzelnen prodromalen Tag kalibriert und erfordert Validierung über weitere Zyklen. Die B7-Risk-Metrik als Prodromalmarker ist eine Arbeitshypothese. Die Abgrenzung zur bestehenden Literatur zeigt, dass die Methodik konzeptuell neu ist — entsprechend fehlt externe Validierung vollständig.

**Literaturverzeichnis**

**Anatomie, Rezeptoren, Signaltransduktion**

- Dahlström A, Fuxe K (1964). *Evidence for the existence of monoamine-containing neurons in the central nervous system.* Acta Physiol Scand 62 Suppl 232: 1–55.
- Sotelo C, Cholley B, El Mestikawy S, Gozlan H, Hamon M (1990). *Direct immunohistochemical evidence of the existence of 5-HT1A autoreceptors on serotoninergic neurons in the midbrain raphe nuclei.* Eur J Neurosci 2: 1144–1154.
- Riad M, Garcia S, Watkins KC, et al. (2000). *Somatodendritic localization of 5-HT1A and preterminal axonal localization of 5-HT1B serotonin receptors in adult rat brain.* J Comp Neurol 417: 181–194.
- Montalbano A, Mlinar B, Bonfiglio F, Polenzani L, Magnani M, Corradetti R (2015). *Pharmacological Characterization of 5-HT1A Autoreceptor-Coupled GIRK Channels in Rat Dorsal Raphe 5-HT Neurons.* PLoS ONE 10(10): e0140369.
- Montalbano A et al. (2018). *Increased functional coupling of 5-HT1A autoreceptors to GIRK channels in Tph2⁻/⁻ mice.* (PubMed 29126768)
- Laaris N, Haj-Dahmane S, Hamon M, Lanfumey L (1997). *Stress-induced alterations of somatodendritic 5-HT1A autoreceptor sensitivity in the rat dorsal raphe nucleus – in vitro electrophysiological evidence.* (PubMed 9243251)
- Albert PR, Le François B, Millar AM (2011). *Transcriptional dysregulation of 5-HT1A autoreceptors in mental illness.* Mol Brain 4: 21.
- Andrade R, Huereca D, Lyons JG, Andrade EM, McGregor KM (2015). *5-HT1A Receptor-Mediated Autoinhibition and the Control of Serotonergic Cell Firing.* ACS Chem Neurosci 6(8): 1110–1118.

**Ultraslow 5-HT-Oszillationen**

- Witt CE, Mena S, Honan LE, Batey L, Salem V, Ou Y, Hashemi P (2022). *Low-Frequency Oscillations of In Vivo Ambient Extracellular Brain Serotonin.* Cells 11(10): 1719.
- Mlinar B, Montalbano A, Piszczek L, Gross C, Corradetti R (2016). *Firing Properties of Genetically Identified Dorsal Raphe Serotonergic Neurons in Brain Slices.* Front Cell Neurosci 10: 195.
- Kato T et al. (2022). (zitiert in Cooper et al. 2024; Fiber-Photometry DRN)
- Turi GF et al. (2024). *Serotonin dynamics in the dentate gyrus during NREM.* (zitiert in Cooper et al. 2024/2025)
- Cooper et al. (2024/2025). *Ultraslow serotonin oscillations in the hippocampus delineate substates across NREM and waking.* eLife / bioRxiv (doi 10.1101/2024.07.09.602643).
- Saylor RA, Hersey M, West A, Buchanan AM, Berger SN, Nijhout HF, Reed MC, Best J, Hashemi P (2019). *In vivo Hippocampal Serotonin Dynamics in Male and Female Mice.* Front Neurosci 13: 362.

**Mathematisches Modell**

- Best JA, Nijhout HF, Reed MC (2010). *Serotonin synthesis, release and reuptake in terminals: a mathematical model.* Theor Biol Med Model 7: 34.
- Best J, Nijhout HF, Reed M (2010). *Models of dopaminergic and serotonergic signaling.* Pharmacopsychiatry 43 Suppl 1: S61–S66.
- Best J, Duncan W, Sadre-Marandi F, Hashemi P, Nijhout HF, Reed M (2020). *Autoreceptor control of serotonin dynamics.* BMC Neurosci 21(1): 40.

**HRV-Nomenklatur**

- Task Force of the European Society of Cardiology and the North American Society of Pacing and Electrophysiology (1996). *Heart rate variability: standards of measurement, physiological interpretation, and clinical use.* Circulation 93: 1043–1065.
- Shaffer F, Ginsberg JP (2017). *An Overview of Heart Rate Variability Metrics and Norms.* Front Public Health 5: 258. Die ULF-Bandgrenze ≤ 0.003 Hz mit Perioden von 5 min bis 24 h, Messung mittels 24-h-Ableitungen, VLF-Band 0.0033–0.04 Hz mit Perioden 25–300 s.
- Kleiger RE, Stein PK, Bigger JT (2005). *Heart rate variability: measurement and clinical utility.* Ann Noninvasive Electrocardiol 10(1): 88–101.
- Lehrer PM et al. (Hrsg.; laufend aktualisierte Übersichten zur LF-Resonanz).

**Migräne-Bildgebung und Pathogenese**

- Weiller C, May A, Limmroth V, Jüptner M, Kaube H, Schayck RV, Coenen HH, Diener HC (1995). *Brain stem activation in spontaneous human migraine attacks.* Nat Med 1(7): 658–660.
- Afridi SK, Giffin NJ, Kaube H, et al. (2005). *A positron emission tomography study in spontaneous migraine.* Arch Neurol 62: 1270–1275.
- Afridi SK, Matharu MS, Lee L, et al. (2005). *A PET study exploring the laterality of brainstem activation in migraine using glyceryl trinitrate.* Brain 128: 932–939.
- Denuelle M, Fabre N, Payoux P, Chollet F, Geraud G (2007). *Hypothalamic activation in spontaneous migraine attacks.* Headache 47: 1418–1426.
- Maniyar FH, Sprenger T, Monteith T, Schankin C, Goadsby PJ (2014). *Brain activations in the premonitory phase of nitroglycerin-triggered migraine attacks.* Brain 137: 232–241.
- Schulte LH, May A (2016). *The migraine generator revisited: continuous scanning of the migraine cycle over 30 days and three spontaneous attacks.* Brain 139(7): 1987–1993.
- Schulte LH, Mehnert J, May A (2020). *Migraine as a cycling brain syndrome.* Neurol Sci (review).
- Jeong HJ et al. (2016). *Increased Brainstem Serotonergic Transporter Availability in Adult Migraineurs.* Nucl Med Mol Imaging 50(3): 233–238.

---

### **I.6 Empirische HRV-Datenanalyse — April 2026**

Dieser Teil analysiert sechs IBI-basierte HRV-Datensätze (vier Nächte, zwei Tage) aus dem Zeitraum 16.–20. April 2026. Die Aufzeichnungen stammen von einem Coospo H808S-Brustgurt mit Beat-to-Beat-Auflösung; die Spektralanalyse erfolgte in gleitenden 5-Minuten-Fenstern. Die Analyse testet Vorhersagen des pathogenetischen Modells zur B7-Amplitudeninstabilität, zur pharmakologischen Modulation durch DPH und Naratriptan, und zur Dissoziation von Tiefschlaf-Staging und autonomer Modulationsqualität.

**Methodik**

**Hardware:** Coospo H808S Brustgurt (EKG-basiert, Beat-to-Beat IBI-Erfassung). Kein PPG — die absoluten Power-Werte sind nicht artefaktgedämpft.

**Spektralanalyse:** Gleitende 5-Minuten-Fenster. Standard-Bandgrenzen: HF 0.15–0.4 Hz, LF 0.04–0.15 Hz, VLF <0.04 Hz. Zusätzlich: pNN50 (Prozent aufeinanderfolgender NN-Intervalle mit >50 ms Differenz) als Zeitdomänen-Proxy für vagale Modulation.

**Zustandsklassifikation:** Minutenweise Zuordnung zu B7/B8-Zuständen nach den Regeln in Abschnitt I.4. Schwellenwerte: B8-dominant (HF/Total > 0.4, LF/Total < 0.25), B7-dominant (LF/Total > 0.4, HF/Total < 0.25), Interferenz (VLF/Total > 0.5), Beide aktiv (HF > 0.3 und LF > 0.3), Both-off (Total < 3 ms²).

**Glättung:** 5-Minuten gleitender Mittelwert (zentriert) für Visualisierung, Rohdaten für Klassifikation und Statistik.

**Visualisierung:** Metabase/Interaktive HTML-Dashboards (Chart.js) als separate Downloads verfügbar.

#### **Nacht 1 — 16. April 2026 (DPH)**

**Kontext:** Diphenhydramin als Schlafintervention. Kein Prodrom, keine akute Symptomatik. Aufzeichnung 00:00–08:00 Uhr mit Lücke 06:00–07:44.

**Deskriptive Statistik:**

| Parameter | Wert |
|---|---|
| HR mean | 64.6 bpm |
| HR min | 44.6 bpm (tiefster aller vier Nächte) |
| VLF% | 42.0 |
| LF% | 25.1 |
| HF% | 32.9 |
| LF/HF median | 0.92 |
| B7-dominant | 2.4% (niedrigster Wert) |
| B8-dominant | 21.3% |
| Interferenz | 41.0% |
| Typ-2 amodal | 12 min |

**Befundmuster:** Die Nacht zeigt eine geordnete Zyklik: B8-dominante Plateaus (HF > LF, niedrige VLF) alternieren mit Interferenz-Blöcken (VLF > LF+HF). Die B8-Plateaus sind die saubersten aller vier Nächte — HF klar über LF, HR erreicht 51 bpm mit pNN50 von 74%. Das Kernstück der Regeneration liegt in den ersten 5 Stunden.

In der zweiten Nachthälfte ab ~04:50 treten 12 Minuten Typ-2-Tiefschlaf auf (pNN50 < 5%, Total Power < 4 ms²). Diese Episoden zeigen Bewegungsunfähigkeit im Xiaomi-Tracker, aber keine autonome Modulation — das Herz schlägt metronomisch bei 63–65 bpm.

Ab 05:10 startet die letzte große Regenerationsphase mit den höchsten Power-Werten der Nacht (Total > 175 ms², VLF bis 173 ms²) und dem tiefsten HR-Nadir (51 bpm, pNN50 74%). Diese Phase trägt den Hauptanteil der glymphatischen Clearance.

**Interpretation:** Die niedrige B7-Dominanz (2.4%) wurde initial DPH zugeschrieben. Die spätere Vergleichsanalyse (N4) zeigt, dass dies nicht haltbar ist — die niedrige B7-Aktivität reflektiert die Zyklusposition, nicht die Pharmakologie.

![Dashboard Nacht 16. April](<images/dashboard_N1_16apr_DPH.png>){width=90%}

#### **Nacht 2 — 18. April 2026 (Desloratadin)**

**Kontext:** Desloratadin als 2.-Generations-Antihistaminikum penetriert die Blut-Hirn-Schranke nicht relevant. Diese Nacht fungiert als unbehandelte Baseline. Aufzeichnung 00:00–07:47 Uhr.

**Deskriptive Statistik:**

| Parameter | Wert |
|---|---|
| HR mean | 67.1 bpm |
| HR min | 45.7 bpm |
| VLF% | 42.4 |
| LF% | 24.9 |
| HF% | 32.8 |
| LF/HF median | 0.96 |
| B7-dominant | 5.1% |
| B8-dominant | 20.7% |
| Interferenz | 42.5% |
| Typ-2 amodal | 22 min |

**Befundmuster:** Die globalen Spektralproportionen sind nahezu identisch mit N1 — VLF 42.4% vs 42.0%, HF 32.8% vs 32.9%, LF 24.9% vs 25.1%. Diese Übereinstimmung über zwei Nächte mit unterschiedlicher Pharmakologie ist bemerkenswert und deutet auf einen stabilen individuellen Fingerabdruck hin.

Hauptunterschiede zu N1: HR-Mean 2.5 bpm höher, B7-Dominanz verdoppelt (5.1% vs 2.4%), 22 statt 12 Minuten Typ-2-Tiefschlaf. Die Einschlafphase zeigt einen HR-Spike auf 95 bpm (sympathische Einschlafreaktion), der in N1 fehlt.

Das Aphasie-Fenster um 05:24–05:38 (pNN50 < 5%, alle Bänder < 2 ms²) ist länger als in N1 und wird gefolgt von dem massivsten VLF-Spike der Nacht (120 ms² um 06:06). Die zweite Nachthälfte ab ~03:00 ist von zunehmender VLF-Dominanz geprägt — die Interferenz eskaliert progressiv.

**Interpretation:** Desloratadin bestätigt seine Rolle als Negativkontrolle: kein zentraler H1-Effekt, die Nacht entspricht der unbehandelten Dynamik. Die Verdopplung der B7-Dominanz gegenüber N1 widerlegt rückblickend die Attribution der N1-Befunde an DPH.

![Dashboard Nacht 18. April](<images/dashboard_N2_18apr_Deslor.png>){width=90%}

#### **Nacht 3 — 19. April 2026 (DPH + Naratriptan)**

**Kontext:** Tag der körperlichen Vorbelastung (Sperrmüll, schwere Gartenarbeit). Abends Stammhirn-Ziehen und retrobulbulärer Schmerz rechts — klassische Prodrome eines B7-Kollapses. DPH und Naratriptan um 23:00 Uhr. Verstärkte LDX-Dosis tagsüber, letzte Gabe 16:00 Uhr. Aufzeichnung 23:00–06:30 Uhr.

**Deskriptive Statistik:**

| Parameter | Wert |
|---|---|
| HR mean | 67.8 bpm (höchster Nacht-Wert) |
| HR min | 50.5 bpm |
| VLF% | 41.6 |
| LF% | 21.7 |
| HF% | 36.6 |
| LF/HF median | 0.63 (stark HF-lastig) |
| B7-dominant | 0.9% (fast absent) |
| B8-dominant | 38.6% (verdoppelt) |
| Interferenz | 33.7% |
| Typ-2 amodal | 65 min (massiv) |

**Befundmuster:** Diametral anders als N1/N2. B7 ist nahezu absent (0.9%), B8 nominell dominant (38.6%), aber die absolute HF-Power ist ebenfalls gedämpft. Die B8-Dominanz entsteht nicht durch starke B8-Aktivität, sondern durch noch stärkeres B7-Fehlen — das Verhältnis verschiebt sich zugunsten HF, nicht weil HF stärker ist, sondern weil LF stärker fehlt.

65 Minuten Typ-2-Tiefschlaf verteilen sich auf zwei Blöcke: 03:30–04:00 (HR=72, pNN50=4%, Total=4 ms²) und 06:00–06:29. In diesen Blöcken ist das ANS funktionell silent.

Die HR bleibt trotz B8-Dominanz bei 67.8 bpm — paradox, aber erklärbar durch die körperliche Vorbelastung: erhöhter sympathischer Grundtonus vom Vortag, unabhängig vom Raphe-Zustand.

**Kritische Reinterpretation:** Initial wurde N3 als „DPH+Triptan hat B7 supprimiert" gelesen. Die spätere Analyse (N4-Vergleich) führte zu einer Revision: B7 war am Zykluspunkt des natürlichen Kollapses. DPH und Naratriptan haben nicht den Kollaps verhindert, sondern die Downstream-Kaskade (CSD, ANS-Destabilisierung) abgepuffert. Die 65 Minuten Typ-2 sind der Kollaps selbst — aber ohne die destruktiven Konsequenzen.

**Folgetag:** Subjektiv post-iktale Klarheit ohne Anfall. 2 Stunden Autofahrt, Gartenarbeit, normale LDX-Dosis — alles funktional. Die Klarheit erklärt sich als LDX-Wirkung bei freigegebener PFC-Bandbreite (kein ANS-Störsignal zu kompensieren).

![Dashboard Nacht 19. April](<images/dashboard_N3_19apr_DPH_Triptan.png>){width=90%}

#### **Tag 19. April 2026 — B7-Wiederanfahrt**

**Kontext:** Folgetag nach N3 (DPH+Naratriptan). LDX reguläre Dosis. Autofahrt 07:00–11:00 Uhr, Gartenarbeit nachmittags. Aufzeichnung 07:00–18:33 Uhr.

**Befundmuster als Zeitraffer der B7-Resynchronisation:**

**07:00–09:00 (Autofahrt):** Total Power 2 ms². Das ANS ist spektral stumm. pNN50 durchgehend 0%. HR 105–120 (LDX + Fahrtätigkeit). Die Oszillatoren sind offline — Nachklang des nächtlichen B7-Shutdowns. Bemerkenswert: 4 Stunden Autofahrt ohne messbare autonome Modulation, bei subjektiver Funktionalität. Der PFC-Schutz über LDX kompensiert den fehlenden Raphe-Drive.

**11:00–13:00:** Langsames LF-Anlaufen. B7 beginnt sich zu re-engagieren. VLF noch niedrig.

**13:09–13:45 (Nap):** HR sinkt auf 81, pNN50 bleibt bei 0%, HF bei 0.3–0.5 ms². Reiner Typ-2-Nap. Ab 13:36 steigt VLF steil auf 12 ms² — die Interferenz beginnt im Nap.

**17:00–18:30:** LF=13 ms², VLF=14 ms², pNN50 bis 10%. B7 vollständig online, sofort im Interferenzmodus — die Phasenbeziehung zu B8 war nie korrigiert.

**Zeitkonstante:** Die B7-Wiederanfahrt nach DPH+Naratriptan-Shutdown liegt bei ~10 Stunden. Die Wiederanfahrt endet nicht in Kohärenz, sondern direkt in der Interferenz.

![Dashboard Tag 19. April](<images/dashboard_Tag19_post_abfang.png>){width=90%}

#### **Nacht 4 — 20. April 2026 (DPH allein)**

**Kontext:** DPH ohne Triptan. Vorabend: B7 nach 10-stündigem Re-Engagement vollständig online mit hohem Gain (LF=13 ms², VLF=14 ms²). Aufzeichnung 23:00–07:43 Uhr.

**Deskriptive Statistik:**

| Parameter | Wert |
|---|---|
| HR mean | 68.9 bpm |
| VLF% | 45.4 (über Baseline) |
| LF% | 24.6 |
| HF% | 30.0 |
| LF/HF median | 0.98 |
| B7-dominant | 8.6% (höchster Wert) |
| B8-dominant | 20.0% |
| Interferenz | 43.1% |
| Typ-2 amodal | 0 min |

**Anmerkung zu den absoluten Power-Werten:** N4 zeigt um Faktor 250–450 höhere absolute ms²-Werte als N1–N3. Dies ist nicht geklärt. Die relativen Proportionen und die Zustandsklassifikation sind weiterhin vergleichbar.

**Befundmuster:** Dieser Datensatz ist der entscheidende Falsifikationspunkt für das DPH-als-Gain-Modulator-Modell. DPH bei hohem B7-Ausgangspegel: B7 feuert durch. 8.6% B7-Dominanz — höher als die unbehandelte Desloratadin-Nacht (5.1%). Kein einziger Typ-2-Block; die gesamte Nacht ist durchmoduliert. VLF steigt erstmals über die 42%-Baseline auf 45.4%.

Am Morgen: HR-Spike auf 117 bpm beim Erwachen. Subjektiv Grogginess und Wackelkopf — die Prodromal-Symptomatik des beginnenden B7-Gain-Anstiegs.

**Interpretation:** DPH hat eine Gain-Decke, keine Gain-Nullung. Bei niedrigem B7-Ausgangspegel (N1) reicht die Decke; bei hohem Ausgangspegel (N4) liegt B7 bereits darüber. Die Differenz erklärt, warum N3 das Triptan benötigte — nicht als redundante Ergänzung, sondern als notwendige Erweiterung bei B7-Pegel oberhalb der DPH-Kapazität.

![Dashboard Nacht 20. April](<images/dashboard_N4_20apr_DPH.png>){width=90%}

#### **Tag 20. April 2026 — Prodromale Kaskade und DPH-Tagesintervention**

**Kontext:** Grogginess und Wackelkopf seit dem Morgen (N4-Folge). LDX-Nachdosis am Vormittag. Nap ~13:09–13:45 mit subjektivem Kollaps-Erleben. DPH um 16:00 Uhr als Tagesintervention. Aufzeichnung 10:00–20:00 Uhr.

**VLF-Kollaps im Nap (13:30–13:40):** VLF explodiert von 969 auf 13433 ms² in 6 Minuten. HR fällt von 69 auf 63. HF springt auf 1863 — B8-Gegenreaktion. Danach: HR schießt auf 119, LF/HF > 8, sympathisch entfesselt. Dies ist ein dokumentiertes Schwellenereignis — der B7-Gain überschreitet die Autoreceptor-Rückkopplungskapazität, und der Kollaps erzeugt eine massive VLF-Welle.

**20-Minuten-Rhythmus:** Die VLF-Peak-Analyse über den gesamten Tag zeigt ein reguläres Oszillationsmuster mit medianem Inter-Peak-Intervall von 20 Minuten (Mean 23 min, n=26 Peaks). Dieser Rhythmus entspricht der vorhergesagten Periodizität des 5-HT1A-Autorezeptor-Grenzzyklus (T ≈ 2τ–4τ bei τ = 10–20 min).

**DPH-Intervention (16:00):** Subjektiv: Stammhirn-Ziehen wird zu Drücken, dann verschwindet. Hitzewelle um 16:37. Nackenverspannung löst sich. Subjektive Klarheit. Spektral: kurzer VLF-Nadir (669 ms² um 16:36 — Hitzewelle korreliert mit dem VLF-Tal, nicht dem Peak). Danach: LF/HF steigt auf 7.7, höher als prä-DPH (3.6). Die sympathische Dominanz ist nicht gebrochen, sondern kehrt nach einem 30-Minuten-Dip stärker zurück.

**Dissoziation subjektiv/spektral:** Die subjektive Klarheit dissoziiert von der spektralen Messung. Der kortikale H1-Effekt (Rauschreduktion, Erregbarkeitssenkung) und der autonome Effekt (sympathische Kaskade) sind unabhängige Pfade. DPH adressiert den ersten, nicht den zweiten.

**Frequenzverdopplung nach Spike:** Nach dem 16:00-VLF-Peak zeigt sich eine transiente Halbierung der Periodizität auf 7–10 Minuten statt 20. Dies ist konsistent mit einem überschwingenden Regelkreis, der sich nach großer Perturbation über mehrere verkürzte Zyklen restabilisiert.

![Dashboard Tag 20. April](<images/dashboard_Tag20_prodromal.png>){width=90%}

#### **Synthese: Verknüpfung der Daten mit dem Modell**

**Befund 1: Der 42%-VLF-Fingerabdruck ist ein Trait-Marker.**

Über vier Nächte mit drei verschiedenen pharmakologischen Konditionen (DPH, Desloratadin, DPH+Triptan) liegt der VLF-Anteil bei 42 ± 1.5%. Keine Intervention hat diese Grunddynamik verändert. Im Amplitudenmodell ist dies die Signatur der chronischen B7-Autoreceptor-Instabilität — die VLF-Hüllkurve des instabilen Gain-Regelkreises. Der 42%-Wert ist modellspezifisch als Maß für die Instabilität des 5-HT1A-Feedback-Loops interpretierbar.

**Befund 2: DPH ist ein Kaskadenpuffer, kein Oszillator-Modulator.**

N1 vs N4 zeigt: identisches Molekül, identische Dosis, völlig verschiedene Ergebnisse. Die B7-Dominanz unter DPH hängt von der Zyklusposition ab, nicht von DPH. DPH verbessert die subjektive Schlafqualität und puffert die Downstream-Kaskade (N3: Kollaps ohne CSD), aber es moduliert weder den B7-Gain noch den VLF-Fingerabdruck.

**Befund 3: Typ-1 und Typ-2 Tiefschlaf sind orthogonale Dimensionen.**

Die simultane Aufzeichnung von Beschleunigungs-Staging und IBI-Spektralanalyse zeigt zwei distinkte Tiefschlaf-Modi, die im Bewegungssensor identisch erscheinen. Die zweite Nachthälfte ist überwiegend Typ-2 (amodal) — regenerativ gescheitert. Die funktionale Schlafkapazität beträgt ~5 Stunden; „Kurzschläfer" ist eine Fehlattribution.

**Befund 4: Das Amplitudenmodell hat höhere Erklärungskraft als das Phasenoffset-Modell.**

Die Vorhersage des Amplitudenmodells war: DPH klemmt den B7-Gain auf einen festen Wert, unabhängig von der Zyklusposition → N4 sollte N1 gleichen. Diese Vorhersage wurde falsifiziert — N4 ≠ N1. Die Revision führt zu einer differenzierteren Version: DPH hat eine Gain-Decke, keine Gain-Nullung. Der B7-Gain ist der primäre Freiheitsgrad, aber DPH moduliert ihn nur unterhalb einer Schwelle.

Die stärkere Version des Befunds: DPH moduliert den Gain überhaupt nicht. Die Variation zwischen N1 (2.4% B7-dom) und N4 (8.6% B7-dom) ist ausschließlich Zyklusposition-abhängig. DPH wirkt auf einen unabhängigen Pfad (kortikale H1-Erregbarkeit, Downstream-Kaskadenpufferung).

**Befund 5: Der 20-Minuten-VLF-Rhythmus ist ein Kandidat für die direkte Autorezeptor-Signatur.**

Die minutenweise VLF-Analyse des prodromalen Tages (20. April) zeigt eine reguläre 20-Minuten-Oszillation, exakt im vorhergesagten Bereich des 5-HT1A-Autorezeptor-Grenzzyklus. Dies ist ein einzelner Datenpunkt (n=1), aber die Übereinstimmung mit der Modellvorhersage (These 2, Anhang I) ist bemerkenswert.

**Befund 6: Die subjektive Erfahrung dissoziiert von der spektralen Messung.**

Der Datenpunkt DPH-Tagesintervention (20. April, 16:00) zeigt subjektive Klarheit bei unveränderter oder verschlechterter spektraler Signatur (LF/HF steigt nach DPH). Die Klarheit wird über den kortikalen H1-Pfad vermittelt (Rauschreduktion → PFC-Bandbreite frei), nicht über den autonomen Pfad. Konsequenz: subjektives Befinden ist kein verlässlicher Proxy für den B7-Zustand. Die Spektralanalyse ist dem Erleben epistemisch überlegen.

**Befund 7: Die prodromale Signatur ist eine Zustandsraum-Kompression.**

Die zweidimensionale Zustandsrepräsentation (Abschnitt I.5) zeigt, dass die prodromale Entwicklung über Tage nicht als einzelnes Schwellenereignis, sondern als progressive Kompression der Dominanz-Achse auf -1 während der Wachstunden sichtbar wird. Am prodromalen Tag (19. April) ist die Dominanz-Varianz auf std = 0.24 kollabiert; das System hat nur noch einen effektiven Freiheitsgrad. DPH stellt die Varianz wieder her, ohne den Mittelwert zu verschieben — es löst die Kompression, nicht die Ursache. Die abgeleitete Metrik b7_risk (interferenz-gewichtetes Exposure-Integral, Abschnitt I.5) ist ein Kandidat für einen prospektiven Prodromalmarker.

**Offene Fragen:**

1. Korreliert der VLF-Anteil (>42% vs <42%) über Nächte hinweg mit der Anfallszyklik? Das wäre der spektrale Proxy für die Schwebungsperiode.
2. Ist das Typ-2/Typ-1-Verhältnis zykluspositionsabhängig? Mehr Typ-2 nahe dem Interferenzmaximum?
3. Gibt es ein Molekül, das den B7-Gain direkt moduliert (nicht nur die Downstream-Kaskade puffert)? Guanfacin (TAAR1) bleibt der offene Kandidat.
4. Ist die 20-Minuten-Periodizität über Tage stabil oder verschiebt sie sich mit der Zyklusposition?
5. Repliziert die nächtliche Kombination LDX+Doxepin die N3-Klarheit reproduzierbar?
6. Validiert sich b7_risk als prospektiver Prodromalmarker über mehrere Zyklen? Kritischer Test: sagt ein b7_risk-Anstieg über aufeinanderfolgende Tage den nächsten Anfall vorher, bevor subjektive Prodrome auftreten?
7. Ist die Zustandsraum-Kompression (Varianzreduktion der Dominanz-Achse in den Wachstunden) der sensitivere Frühindikator als b7_risk?

**Anhang: Interaktive Dashboards**

Die folgenden HTML-Dateien enthalten interaktive Visualisierungen (Chart.js) der Rohdaten mit Zustandsklassifikation, HR/pNN50-Verlauf und Spektralband-Zeitreihen:

- `dashboard_N1_16apr_DPH.html` — Nacht 1
- `dashboard_N2_18apr_Deslor.html` — Nacht 2
- `dashboard_N3_19apr_DPH_Triptan.html` — Nacht 3
- `dashboard_N4_20apr_DPH.html` — Nacht 4
- `dashboard_Tag19_post_abfang.html` — Tag 19. April
- `dashboard_Tag20_prodromal.html` — Tag 20. April