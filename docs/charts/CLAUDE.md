# docs/charts/ — index.html

Dieses Verzeichnis enthält interaktive HTML-Charts (Plotly-Exports) zur
nächtlichen Herzfrequenz-Analyse. Die `index.html` ist eine einfache Übersichts-
seite im GitHub-Look, die alle vorhandenen Charts über zwei Akkordeons bündelt.

## Aufbau der `index.html`

- **GitHub-ähnliches Styling**, inline in `<style>`, inklusive Dark-Mode via
  `prefers-color-scheme`. Keine externen Abhängigkeiten.
- **Zwei Sektionen / Akkordeons**:
  1. `Nadirs` — bindet alle `nadirs_*.html` ein.
  2. `Plateaus` — bindet alle `plateaus_*.html` ein.
- Jedes Akkordeon-Element:
  - ist initial **eingeklappt** (`<details>` ohne `open`),
  - lädt den Chart beim ersten Aufklappen per `<iframe>` (lazy, um 30 iframes
    beim Seitenaufruf zu vermeiden),
  - zeigt einen **"Direkt öffnen ↗"**-Link zur jeweiligen HTML-Datei.
- Jede Sektion hat einen **Toggle-Button** (`Alle aufklappen` ↔
  `Alle einklappen`), der nur die Elemente der eigenen Sektion betrifft.
- Die Listen der Chart-Dateien stehen als JavaScript-Arrays (`nadirFiles`,
  `plateauFiles`) am Ende der Seite.

## Aktualisieren, wenn neue Charts hinzukommen

Wenn neue `nadirs_YYYY-MM-DD.html` oder `plateaus_YYYY-MM-DD.html` in dieses
Verzeichnis gelegt werden:

1. In `index.html` die entsprechenden Einträge in die JS-Arrays `nadirFiles`
   bzw. `plateauFiles` aufnehmen (chronologisch sortiert).
2. Es ist **kein Build-Schritt** nötig — die Seite wird direkt über GitHub Pages
   ausgeliefert. Ein einfacher Commit genügt.
3. Dateibenennungskonvention **beibehalten** (`nadirs_YYYY-MM-DD.html` /
   `plateaus_YYYY-MM-DD.html`) — das Skript extrahiert das Datum per Regex aus
   dem Dateinamen für die Labels.

## Hinweise

- Die Chart-HTMLs selbst werden außerhalb dieses Verzeichnisses generiert
  (siehe `02_pathogenese_modell/data/`) und hierher kopiert, damit GitHub Pages
  sie ausliefern kann.
- Keine der Chart-Dateien in `docs/charts/` darf manuell editiert werden; sie
  sind reine Ausgabeartefakte.
- Die `index.html` enthält keine Daten, nur eine Einbettung — größere Layout-
  oder Stiländerungen bitte dort zentral vornehmen.
