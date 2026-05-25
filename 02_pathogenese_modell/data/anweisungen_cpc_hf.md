# Briefing: REM-Diskriminator-Metriken aus R-R-only-Daten

Ziel-Briefing für die Erweiterung der bestehenden HRV-Aggregationspipeline um zwei REM-sensitive Spektralmaße.

## 1. Ziel

Zwei neue Spalten in der Minutenaggregation, die in REM-Phasen systematisch von NREM2/NREM3 abweichen. Quelle ist ausschließlich die bereits ektopie-bereinigte R-R-Serie der Pipeline. Akzeptable Trennschärfe ist niedrig — Hauptsache, das Signal ist *durchgehend* vorhanden. Keine Schwellwerte, keine Gates, keine kategorialen Outputs, keine Filter, die Minuten verwerfen. NaN ist nur erlaubt, wo es mathematisch unvermeidbar ist (z. B. Fenster komplett ohne valide R-R-Werte). Zwei Eingriffsmodi: regulärer Pipeline-Lauf erzeugt die Spalten mit; ein Flag aktiviert einen Nachhol-Modus, der ausschließlich die zwei neuen Spalten neu berechnet, ohne den Rest der Pipeline zu touchieren.

## 2. Physiologischer Zusammenhang

REM ist autonom kein einheitlicher Zustand, aber zeigt drei robuste Eigenschaften gegen NREM. Erstens: tonische Sympathikus-Reaktivierung — der Mayer-Welle-Generator (Baroreflex, ~0.1 Hz) ist wieder aktiv, während er in NREM3 zusammenbricht. Zweitens: phasische Bursts (PGO-Wellen vom Pons), die mit transienten autonomen Auslenkungen einhergehen. Drittens — und das ist der diagnostisch nutzbare Punkt — atmosphärische Irregularität: die pontinen REM-Generatoren modulieren den respiratorischen Rhythmus, sodass die Atemfrequenz von Atemzug zu Atemzug springt. In NREM ist die Atmung metronomisch; in REM wandert sie.

Diese Atmungs-Irregularität projiziert sich über die respiratorische Sinusarrhythmie (RSA) in die R-R-Serie. RSA ist die HF-Komponente der HRV (~0.15–0.4 Hz). In NREM steht der HF-Peak stabil und kohärent zur Atmung. In REM springt der Peak, und die Phasenkohärenz zwischen R-R-Modulation und (rekonstruierter) Atmung bricht ein. Beide Diskriminatoren — CPC und HF-Peak-Stabilität — adressieren diesen Effekt aus unterschiedlichen mathematischen Perspektiven.

## 3. Literatur und Forschungsstand

Cardiopulmonary Coupling (CPC) wurde von Thomas, Mietus, Peng und Goldberger 2005 (Sleep, 28:1151–1161) eingeführt. Originalmethode arbeitet auf R-R + ECG-derived respiration (EDR aus R-Wave-Amplitudenmodulation). Die Methode definiert vier kardiopulmonale Kopplungsdomänen über das Frequenzspektrum: Very-Low-Frequency-Coupling (VLFC, 0–0.01 Hz, Wake/Übergang), Low-Frequency-Coupling (LFC, 0.01–0.1 Hz, REM und instabiler/fragmentierter Schlaf), High-Frequency-Coupling (HFC, 0.1–0.4 Hz, stabiler NREM2/NREM3). Eine Untergruppe von LFC mit erhöhter spektraler Amplitude (elevated-LFC, e-LFC) markiert sleep-disordered breathing — für die REM-Frage hier nicht relevant, aber als Konfounder bekannt.

Für unseren Fall: EDR ist aus R-R-Daten allein nicht direkt extrahierbar. Die etablierte Workaround-Variante (Pinna et al. 2007, Bartsch et al. 2007, später kommerziell in MyCardio/SleepImage übernommen) verwendet die RSA-Amplitudenhüllkurve als EDR-Surrogat. Die Trennschärfe sinkt gegenüber Original-EDR, bleibt aber für REM-vs-NREM ausreichend. Referenzimplementierungen: PhysioNet stellt MATLAB-Code zum Originalalgorithmus bereit; Python-Ports existieren als `pyCPC` (rudimentär, prüfen) und in Komponenten von `mne-features` und `neurokit2`. Für eine eigene Implementation sind `scipy.signal` (Welch, CSD, Hilbert) und `numpy` ausreichend.

HF-Peak-Stabilität ist methodisch einfacher und in der Schlafstudien-Literatur seit den 1990ern bekannt (Sayers 1973 für RSA-Variabilität generell; Burgess et al. 1999 für Stadienabhängigkeit der RSA-Peak-Wanderung). Es ist kein klinisch standardisiertes Maß, sondern eines unter vielen Features in ML-basiertem Sleep-Staging (Fonseca 2015, Long 2014). Als Standalone-Metrik ist es schwach, aber für unsere Zwecke — niedrige Trennschärfe akzeptabel, durchgängiges Signal nötig — geeignet, weil es nie ausfällt: jedes Spektralfenster hat einen Peak.

## 4. Mathematik

### CPC

Sei $r(t)$ die auf gleichmäßiges Raster (typisch 2 Hz, kubisch interpoliert) gebrachte R-R-Zeitreihe und $e(t)$ das EDR-Surrogat. Beide werden über ein Fenster $W$ analysiert. Schritte:

EDR-Konstruktion. $r(t)$ wird bandpass-gefiltert im respiratorischen Band (0.1–0.4 Hz). Auf das gefilterte Signal wird die Hilbert-Transformation angewandt; der Betrag des resultierenden analytischen Signals ist die RSA-Amplitudenhüllkurve $e(t)$. Diese Hüllkurve trägt die Atmungs-Modulationsinformation, soweit sie sich in der RSA spiegelt.

Cross-Spektrum. Über Welch-Periodogramme (Hanning-Fenster, 50% Overlap, Segment-Länge typisch 256 Samples bei 2 Hz Raster) werden Auto-Power $S_{rr}(f)$, $S_{ee}(f)$ und Cross-Power $S_{re}(f)$ geschätzt. Die magnitude-squared Coherence ist

$$ \gamma^2(f) = \frac{|S_{re}(f)|^2}{S_{rr}(f) \cdot S_{ee}(f)} $$

mit Wertebereich $[0, 1]$. Die CPC-Größe ist das Produkt aus Coherence und Cross-Power-Magnitude:

$$ \mathrm{CPC}(f) = \gamma^2(f) \cdot |S_{re}(f)| $$

Aggregation in Bänder. Pro Analysefenster werden drei Skalare berechnet:

$$ \mathrm{LFC} = \int_{0.01}^{0.1} \mathrm{CPC}(f)\, df, \quad \mathrm{HFC} = \int_{0.1}^{0.4} \mathrm{CPC}(f)\, df, \quad \mathrm{VLFC} = \int_{0}^{0.01} \mathrm{CPC}(f)\, df $$

Für REM-Diskrimination ist das interessanteste Aggregat das LFC/HFC-Verhältnis oder die LFC-Ratio $\mathrm{LFC}/(\mathrm{LFC} + \mathrm{HFC})$. Eine einzelne Spalte reicht; das Verhältnis ist normalisierter und robuster gegen absolute Powerschwankungen über die Nacht. Konvention: hohe Werte → REM/instabiler Schlaf, niedrige Werte → stabiler NREM.

Fenstergröße ist methodisch heikel. Originalmethode arbeitet mit ~8.5 min (1024 Samples @ 2 Hz). Für eine Minutenaggregation mit Gleitfenster ist eine Fensterbreite von 5–8 min um den Minuten-Marker zentriert sinnvoll. Das ist breiter als das HRV-Standardfenster der bestehenden Pipeline — das ist methodisch erforderlich, weil im LFC-Band (untere Grenze 0.01 Hz, Periode 100 s) ohne ausreichend lange Fenster keine sinnvolle Spektralauflösung möglich ist. Diese Breite mit dem bestehenden Slide-Schema in Einklang bringen, ohne das Schema zu ändern.

### HF-Peak-Stabilität

Pro Spektralfenster (vermutlich bereits durch die Pipeline berechnet) wird die Frequenz $f_{\max}$ des dominanten Peaks im HF-Band 0.15–0.4 Hz bestimmt. Bei normaler Atmung liegt $f_{\max}$ um 0.2–0.3 Hz (12–18 Atemzüge/min). Über ein gleitendes Fenster von typisch 5 min wird die Standardabweichung oder Interquartilrange von $f_{\max}$ berechnet:

$$ \sigma_{\mathrm{HF}}(t) = \mathrm{SD}\big( \{ f_{\max}(\tau) : \tau \in [t - 2.5\,\mathrm{min}, t + 2.5\,\mathrm{min}] \} \big) $$

Hohe Werte ($\sigma_{\mathrm{HF}} \gtrsim 0.03$ Hz) deuten auf instabile Atmung und damit REM hin; niedrige Werte ($\lesssim 0.01$ Hz) auf metronomische NREM-Atmung. Die absoluten Schwellen sind individuell und nicht relevant — als Spalte wandert das Maß einfach mit, die Interpretation passiert nachgelagert.

Wichtig für das Peak-Picking: nicht der globale Maximum-Bin, sondern parabolische Interpolation um den lokalen Maximum-Bin, um sub-Bin-Auflösung zu erhalten und Quantisierungs-Plateaus zu vermeiden. Wenn das HF-Band kein klares Maximum hat (Power dort sehr niedrig, z. B. tiefer NREM3 oder Null-Phase), liefert die Methode trotzdem einen Wert — der ist dann zwar wenig physiologisch interpretierbar, aber das ist Teil der Designentscheidung „lieber verrauscht als fehlend".

## 5. Bezug zur bestehenden Pipeline

Beide Metriken setzen auf der ektopie-bereinigten R-R-Serie auf, die die Pipeline bereits produziert. HF-Peak-Stabilität kann auf den bereits berechneten Spektralwerten aufsetzen, falls die Pipeline pro Fenster nicht nur LF/HF-Power, sondern auch die Peak-Frequenz speichert oder leicht rekonstruieren lässt — ansonsten ist ein zweiter Pass über die Spektren günstig. CPC braucht ein eigenständiges, längeres Analysefenster mit eigenem Resampling auf festes Raster; das läuft parallel zum bestehenden Spektral-Pass und konkurriert nicht mit ihm.

Die Zeitachse beider Metriken muss zwingend die Zeitachse der bestehenden Minutenaggregation sein. Eigene Zeitberechnungen via Cumsum auf der R-R-Serie führen zu kumulativem Drift gegenüber der Pipeline-Achse (akkumulierte NaN-Lücken, Filter-Dropouts) und wurden in vorherigen Iterationen bereits als Fehlerquelle identifiziert. Die neuen Funktionen erhalten R-R-Slices und Pipeline-Zeitstempel vom Aufrufer; sie konstruieren keine eigene Zeit.

Nachhol-Flag: ein Modus, der ausschließlich die zwei neuen Spalten neu berechnet, ohne die bestehenden Aggregat-Werte anzufassen. Die konkrete Mechanik (in-place-Update der vorhandenen Aggregat-Datei vs. Sidecar-Output zum Joinen) ist im Pipeline-Kontext zu entscheiden, je nachdem wie die Pipeline aktuell ihre Outputs schreibt.

## 6. Performance

CPC ist die teurere der beiden Metriken. Pro Fenster ein Welch-Periodogramm auf zwei Signalen plus Cross-Spectrum — das ist eine Handvoll FFTs pro Minute. Bei 8-h-Nacht und Minutenaggregation entstehen ~480 Fenster, je 3 FFTs auf ~1000 Samples — das sind Millisekunden auf moderner Hardware. Optimierungsbedarf besteht nicht; der naive Loop ist schnell genug. `scipy.signal.welch` und `scipy.signal.csd` sind ausreichend.

Achtung: das R-R → 2 Hz-Resampling ist die heikelste Stelle. Kubische Spline-Interpolation ist die Konvention (`scipy.interpolate.CubicSpline`). Bei R-R-Lücken (Bewegungsartefakte, Filter-Drops) liefert Spline auf großen Lücken Schwingungs-Artefakte; daher: Lücken > 2 s linear interpolieren oder als NaN durchlassen und das resultierende Fenster mit zu wenig validen Samples eine NaN-Spalte erzeugen lassen. Das ist genau die Stelle, an der „lieber verrauscht als fehlend" mit „mathematisch unvermeidbar NaN" abgewogen wird — Schwellenwert für „zu wenig valide Samples" liberal setzen (etwa <30 % NaN im Fenster akzeptieren).

HF-Peak-Stabilität ist trivial billig. Wenn die Pipeline bereits Spektren cached, ist es ein zweiter Lauf über die Fenster mit Peak-Picking und gleitender SD darauf — Millisekunden insgesamt.

Bibliotheks-Optionen, in absteigender Direktheit: Eigenbau auf `scipy.signal` (volle Kontrolle, ~150 Zeilen); `neurokit2` hat eine `signal_psd`-Komponente und kann Coherence, aber kein direktes CPC; `pyCPC` als Drittprojekt mit unklarer Wartung — als Referenz lesen, nicht als Dependency nehmen.

## 7. Constraints

Keine Thresholds, die Werte in 0/1 wandeln. Keine Gates, die Minuten verwerfen. Keine Glättungsfilter über Stadien-Übergänge hinweg. Keine kategorialen REM/NREM-Labels als Output — die Spalten sind kontinuierlich, die Interpretation passiert nachgelagert. Wenn ein Fenster aus mathematischen Gründen keinen Wert liefern kann (z. B. komplett NaN-R-R), darf null entstehen; alles andere muss einen Wert produzieren, auch bei zweifelhafter Qualität.

Die zwei Spalten sind unabhängig — wenn die eine eine Nacht durchgängig liefert und die andere lückenhaft ist, ist das OK. Die nachgelagerte Auswertung kann beide Signale gegeneinander stellen und sich aus der Konsistenz ein Bild bauen.