---
title: "Der B7-Kern, 5-HT1A-Autorezeptor-Dynamik und ihre Signatur im HRV-Frequenzspektrum"
subtitle: "Eine Kontextualisierung für die pathogenetische Analyse autonomer Oszillationen"
author: "Synthese-Dokument"
date: 2026-04-20
abstract: |
  Dieses Dokument synthetisiert das wissenschaftliche Material zur rostralen Dorsal-Raphe-Region (Zellgruppe B7 nach Dahlström & Fuxe), zur somatodendritischen 5-HT1A-Autorezeptor-Rückkopplung und zu deren Manifestation in den Spektralbändern der Herzfrequenzvariabilität. Ziel ist die kompakte Bereitstellung des pathogenetischen Kontexts für eine nachfolgende empirische Datenauswertung. Nicht enthalten sind formale Herleitungen der spektralen Transformation oder Bifurkationsanalysen des Oszillatormodells.
---

***

## **Anhang I: Tracker-Datenanalyse — HRV**

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

### **I.1 Die 5-HT1A-Autorezeptor-Rückkopplung: Signaltransduktion und Kinetik

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

### **I.4 Epistemische Einordnung**

Diese Synthese verbindet drei Literaturlinien:

1. **Solide etabliert**: Anatomie und Signalkaskade des 5-HT1A-Autorezeptors, die HRV-Band-Standardnomenklatur, die PET-Befunde zur persistierenden Hirnstamm- und Hypothalamus-Aktivierung bei Migräne, die Existenz ultraslow-5-HT-Oszillationen.

2. **Modellbasiert, plausibel**: Die mathematische Autorezeptor-Dynamik (Best/Nijhout/Reed-Linie) mit τ im 10–20-min-Bereich; die Oszillator-Interpretation der Migräne-Pathogenese (Schulte/May-Linie).

3. **Inferenz, nicht direkt belegt**: Die explizite Kopplung einer B7-Autorezeptor-Grenzzyklus-Aktivität auf das ULF2-HRV-Band als prodromaler Biomarker. Diese Brücke ist physiologisch plausibel, in der Primärliteratur jedoch nicht als etabliertes Messparadigma verankert. Die Brücke ist das Arbeitsgebiet der nachgelagerten Datenanalyse, nicht ein Zitat.

Die Nützlichkeit dieser Konzeption bemisst sich an ihrer prospektiven Vorhersagekraft: ob der vorhergesagte ULF2-Peak tatsächlich prodromal und spezifisch ist, ob er pharmakologisch interpretierbar moduliert wird, und ob er zwischen Individuen konsistent bleibt.

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