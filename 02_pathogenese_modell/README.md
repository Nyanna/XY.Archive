# Pathogenetisches Modell

> **Arbeitshypothese.** Keine gesicherte Diagnose, keine Leitlinie. Strukturierte Gesprächsgrundlage für ärztliche Beurteilung. Evidenzniveau variiert pro Abschnitt und ist jeweils explizit gekennzeichnet.

Integriertes Syndrom-Modell: **kongenitale Raphe-Dysregulation** (5-HT1A-Autorezeptor-Instabilität) und **hypothalamische Circadian-Dysregulation** als ko-primäre Defekte, die downstream fünf klinisch ko-auftretende Phänotypen produzieren — Migräne, thalamische Gating-Insuffizienz, ASD-Phänotyp, autonome Dysregulation und interozeptive Inkohärenz. Two-Hit-Architektur: pränatale 5-HT1A-Instabilität (Hit 1) + postnataler D2High-Shift durch iatrogene Glukokortikoidexposition bei atopischer Dermatitis (Hit 2).

Triade-Hypothese: **AD + ADHS + Migräne** als populationsrelevanter, bislang nur in Dyaden untersuchter Phänotyp (~90k–200k Betroffene in Deutschland). Details siehe [`01_overview.md`](01_overview.md).

## Pathogenetischer Verlauf (Kurzform)

| Phase | Kurzbeschreibung |
| :---- | :--------------- |
| **I — Pränatal (Hit 1)** | Kongenitale 5-HT1A-Instabilität, underdämpfte Raphe-Oszillation ab 5.–7. SSW. |
| **II — Fetal** | Instabiles Serotoninsignal verzerrt thalamokortikale Kalibrierung (22.–26. SSW). |
| **III — Postnatal/kindlich (Hit 2)** | Manifeste Gating-Insuffizienz; AD-Manifestation; iatrogene GC-Exposition induziert D2High-Shift. |
| **IV — Chronisch/adult** | Periodische Migräne, quasi-wöchentliche Periodizität als Superposition von zirkadianer Schwebung und B7-Intertakt-Drift gegen B8-SCN-Lock. |
| **V — Pharmakologisch** | Dopaminerge Upstream-Stabilisierung (MPH/LDX) → Migränefreiheit, Bestätigung der D2-Hypersensitivität. |

## Kapitel

| Kapitel | Inhalt |
| :------ | :----- |
| [00 — Intro](00_intro.md) | Titel, Disclaimer, Kurzfassung des Modells. |
| [01 — Pathogenetischer Verlauf (Übersicht)](01_overview.md) | Phasen I–V, Triade-Analyse, epidemiologische Schätzung, Kapitelstruktur. |
| [02 — Primärdefekt: Raphe-Dysregulation](02_primary_defect.md) | Raphe-Anatomie, 5-HT1A-Instabilität, Two-Hit-Architektur, B7/B8-Dual-Oszillator, zirkadiane Schwebung. |
| [03 — Downstream I: Thalamische Fehlkalibrierung](03_downstream.md) | Fetale Kalibrierung auf instabiles Signal, ADHS als SNR-Problem, Gating/Schwelle unter LDX. |
| [04 — Manifestation I: Migräne als Raphe-Zyklusstörung](04_manifestation1.md) | Trigger, CSD-Auslösung, CSD als Reset, Triptan-Mechanismus, Betablocker-Paradox. |
| [05 — Manifestation II: Autonome Dysregulation](05_manifestation2.md) | NTS-Pfade, vestibuloautonomer Reflex, TCR, PFC→NTS-Suppression, B7-Aphasie. |
| [06 — Manifestation III: ASD-Phänotyp](06_manifestation3.md) | ASD als Konfigurationsvariante des Primärdefekts, repetitives Verhalten als Stabilisierung. |
| [07 — Pharmakologische Evidenz: Selbstversuch](07_evidenz.md) | Methylphenidat, Lisdexamfetamin, therapeutisches Fenster. |
| [08 — Interozeptive Inkohärenz](08_synchronisation.md) | Asynchrone Modulationssysteme, LDX als Synchronisator, Kreuzkorrelation ADHS–Migräne–Epilepsie. |
| [09 — Evidenzstatus und Limitationen](09_state_limits.md) | Dreistufige Evidenzklassifikation, offene Fragen. |

## Anhänge

| Anhang | Inhalt |
| :----- | :----- |
| [A — Emotionale Affektion](0A_asd_relation.md) | Arbeitshypothese zur Emotionsverarbeitung; Implikation für ASD-Phänotyp. |
| [B — Tracker-Datenanalyse](0B_sws_phase_v2.md) · [Charts ↗](https://nyanna.github.io/XY.Archive/charts/) | Kortikale Desynchronisation als Marker: Schlaffragmentierung, Nap-Korrelation, HR-Drop-Periodizität, Anfallstiming. Interaktive Visualisierungen unter dem Charts-Link. |
| [C — Phänomenologie eines Bewusstseinsresets](0C_concentration_reset.md) | Erfahrungsbericht: lokaler Schlaf, Bewusstseinsdruck, Nap-als-Reboot. |
| [D — Raphe-Synchronisationsmechanik](0D_raphe_sync.md) | Architektur der neun Raphe-Kerne, Volumentransmission, Reset-Oszillator, Desynchronisationsmodi. |
| [E — CSD und Epilepsie](0E_epilepsie.md) | Fallback-Hierarchie Raphe → CSD → Anfall, Serotonin als Antikonvulsivum, SUDEP. |
| [F — B7/B8-Innervierungsanatomie](0F_b7b8_innervierung.md) | Projektionsmuster DRN vs. MRN, thalamische und hippocampale Interferenzstrukturen. |
| [G — Iatrogene Prävalenz](0G_iatrogene_praevalenz.md) | Historische Korrelation pharmazeutischer Exposition mit ADHS-Prävalenz, Industrieländer-Gradient. |
| [H — Hypothyreose als Kofaktor](0H_hypothyreose.md) | T3/T4 ↔ 5-HT1A-Sensitivität, Modulator der LDX-Wirksamkeit. |
| [I — HRV-Frequenzspektrum](0I_hrv_analysis.md) · [Dashboards ↗](https://nyanna.github.io/XY.Archive/dashboards/)| IBI-basierte Spektralanalyse, VLF-Band als 5-HT1A-Intratakt-Signatur, Trait-Fingerabdruck (42 ± 1,5 % VLF). |

## Build & Daten

Die Einzelkapitel werden per `build.sh` (CI-automatisiert) zur kombinierten Datei [`../02_pathogenese_modell.md`](../02_pathogenese_modell.md) gemerged. Rohdaten und Analyse-Skripte liegen unter [`data/`](data/); siehe [`CLAUDE.md`](CLAUDE.md) für Details.
