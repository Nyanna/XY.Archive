# docs/charts/ — index.html

Dieses Verzeichnis enthält interaktive HTML-Charts (Plotly-Exports) zur
nächtlichen Herzfrequenz-Analyse. Die `index.html` ist eine einfache Übersichts-
seite im GitHub-Look, die alle vorhandenen Charts über zwei Akkordeons bündelt.

## Aufbau der `index.html`

- **GitHub-ähnliches Styling**, inline in `<style>`, inklusive Dark-Mode via
  `prefers-color-scheme`. Keine externen Abhängigkeiten.
- **Full-Width-Layout**: Der Container nutzt die volle Browserbreite (mit
  `clamp()`-basiertem Seiten-Padding). Nur der Intro-Block (`header`, `.intro`)
  ist auf ~1012 px lesbare Breite begrenzt; die Akkordeons und die eingebetteten
  iframes skalieren mit dem Fenster.
- **Zwei Sektionen / Akkordeons**:
  1. `Nadirs` — bindet alle `nadirs_*.html` ein.
  2. `Plateaus` — bindet alle `plateaus_*.html` ein.
- Jedes Akkordeon-Element:
  - ist initial **eingeklappt** (`<details>` ohne `open`),
  - lädt den Chart beim ersten Aufklappen per `<iframe>` (lazy, um 30 iframes
    beim Seitenaufruf zu vermeiden),
  - der iframe ist per `width: 100%` responsiv — passt sich also automatisch
    an die Containerbreite an. Die Höhe ist fix auf 640 px,
  - zeigt einen **"Direkt öffnen ↗"**-Link zur jeweiligen HTML-Datei.
- Jede Sektion hat einen **Toggle-Button** (`Alle aufklappen` ↔
  `Alle einklappen`), der nur die Elemente der eigenen Sektion betrifft.
- Die Listen der Chart-Dateien stehen als JavaScript-Arrays (`nadirFiles`,
  `plateauFiles`) am Ende der Seite.

## Event-Marker (Seizure-Tage)

Tage, an denen in `02_pathogenese_modell/data/seizures.csv` ein Anfall
dokumentiert ist, werden im Akkordeon deutlich markiert:

- **`Event!`-Badge** (rot) rechts neben dem Datum in der Summary-Zeile.
- **Roter Border-Left** auf der Summary zur schnellen visuellen Erkennung
  auch bei eingeklapptem Zustand.
- Beide Akkordeons (Nadirs + Plateaus) werden markiert, wenn das Datum matcht.

Die Event-Daten stehen als JS-`Set` (`seizureDates`) unterhalb der Datei-Arrays,
im ISO-Format `YYYY-MM-DD`. Die Quelle (`seizures.csv`) verwendet `DD/MM/YYYY`
— beim Pflegen **in ISO umformatieren**. Einträge außerhalb des aktuellen
Chart-Zeitraums dürfen im Set verbleiben; sie haben keinen Effekt.

## Aktualisieren, wenn neue Charts hinzukommen

Wenn neue `nadirs_YYYY-MM-DD.html` oder `plateaus_YYYY-MM-DD.html` in dieses
Verzeichnis gelegt werden:

1. In `index.html` die entsprechenden Einträge in die JS-Arrays `nadirFiles`
   bzw. `plateauFiles` aufnehmen (chronologisch sortiert).
2. **Seizure-Set prüfen**: Für jedes neue Chart-Datum gegen `seizures.csv`
   abgleichen — Treffer als ISO-Datum in das `seizureDates`-Set eintragen.
3. Es ist **kein Build-Schritt** nötig — die Seite wird direkt über GitHub Pages
   ausgeliefert. Ein einfacher Commit genügt.
4. Dateibenennungskonvention **beibehalten** (`nadirs_YYYY-MM-DD.html` /
   `plateaus_YYYY-MM-DD.html`) — das Skript extrahiert das Datum per Regex aus
   dem Dateinamen für die Labels und den Seizure-Match.

## Aktualisieren, wenn neue Seizures dokumentiert werden

Wenn `02_pathogenese_modell/data/seizures.csv` um Einträge ergänzt wird, die in
den Datumsbereich bereits eingebundener Charts fallen:

1. Die relevanten Datumswerte aus der CSV nach ISO konvertieren.
2. In `index.html` dem `seizureDates`-Set hinzufügen.
3. Commit. Keine weiteren Schritte nötig.

## Hinweise

- Die Chart-HTMLs selbst werden außerhalb dieses Verzeichnisses generiert
  (siehe `02_pathogenese_modell/data/`) und hierher kopiert, damit GitHub Pages
  sie ausliefern kann.
- Keine der Chart-Dateien in `docs/charts/` darf manuell editiert werden; sie
  sind reine Ausgabeartefakte.
- Die `index.html` enthält keine Daten, nur eine Einbettung und die
  Seizure-Liste — größere Layout- oder Stiländerungen bitte dort zentral
  vornehmen.
- Bewusste Duplizierung: Das `seizureDates`-Set ist eine von Hand gepflegte
  Kopie der CSV-Daten, kein Runtime-Fetch. Rationale: GitHub Pages liefert nur
  `docs/`, ein Cross-Directory-Fetch von `../../02_pathogenese_modell/data/` ist
  fragil; die kleine Redundanz ist der einfachere Weg.
