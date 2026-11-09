Sortiere die Geräte initial nach "Erstmals gesehen". Danach soll die Reihenfolge möglichst stabil gehalten werden. Wenn also Geräte den AP wechseln sollen die im AP Segment zuletzt stehen.
Dies kann damit erreicht werden das sich die Seite die Reihenfolge und die aktuellen Informationen vom Backent als Delta prozessiert.

`/home/user/xyan/XY.Archiv/hrviewer/statics/devices.config.js`
`/home/user/xyan/XY.Archiv/hrviewer/statics/devices.js`
SystemInit:  id=20099565-89be-4140-aa90-bed612b5233c, cwd=/home/user/xyan/XY.Archiv/hrviewer, model=claude-sonnet-5-5
Control Request:
```yaml
id: 88b5-1-0
toolName: read_file
arguments:
  items:
  - path: /home/user/xyan/XY.Archiv/hrviewer/statics/devices.js
  - path: /home/user/xyan/XY.Archiv/hrviewer/statics/devices.config.js
  reason: Read both files to understand current device rendering and sorting
```
/answer 88b5-1-0 allow
ReasoningToken: 395
Control Request:
```yaml
id: 88b5-2-0
toolName: edit_marks
arguments:
  items:
  - path: /home/user/xyan/XY.Archiv/hrviewer/statics/devices.js
    begin_marker: "  function render() {"
    end_marker: "    const byName = (a, b) => a.display_name.localeCompare(b.display_name, \"de\");"
    content: |2-
        /* Stable ordering: initial order is "first seen"; a device that changes
         * section gets a fresh sequence number and therefore moves to the end. */
        const placement = new Map();
        const sequence = new Map();
        let seqCounter = 0;

        function sectionKey(d) {
          const apIp = d.location && d.location.ap_ip;
          return apIp && d.interface !== "lan" ? apIp : null;
        }

        function applyDelta(devices) {
          const firstSeen = (d) => {
            const t = d.first_seen ? new Date(d.first_seen).getTime() : NaN;
            return isNaN(t) ? Infinity : t;
          };
          const present = new Set();
          [...devices]
            .sort((a, b) => firstSeen(a) - firstSeen(b) || a.display_name.localeCompare(b.display_name, "de"))
            .forEach((d) => {
              present.add(d.mac);
              const key = sectionKey(d);
              if (!sequence.has(d.mac) || placement.get(d.mac) !== key) {
                placement.set(d.mac, key);
                sequence.set(d.mac, ++seqCounter);
              }
            });
          for (const mac of [...sequence.keys()]) {
            if (!present.has(mac)) {
              sequence.delete(mac);
              placement.delete(mac);
            }
          }
        }

        function render() {
          if (!snapshot) return;
          const q = filterEl.value.trim().toLowerCase();
          const devices = snapshot.devices.filter((d) => matches(d, q));

          const byAp = new Map();
          snapshot.access_points.forEach((ap) => byAp.set(ap.ip, { ap, devices: [] }));
          const lan = [];
          devices.forEach((d) => {
            const apIp = sectionKey(d);
            if (apIp) {
              if (!byAp.has(apIp)) {
                const l = d.location;
                byAp.set(apIp, { ap: { ip: apIp, mac: l.ap_mac, name: l.ap_name, floor: l.floor, room: l.room }, devices: [] });
              }
              byAp.get(apIp).devices.push(d);
            } else {
              lan.push(d);
            }
          });

          const byName = (a, b) => sequence.get(a.mac) - sequence.get(b.mac);
  - path: /home/user/xyan/XY.Archiv/hrviewer/statics/devices.js
    begin_marker: '      snapshot = await r.json();'
    end_marker: '      snapshot = await r.json();'
    content: |2-
            snapshot = await r.json();
            applyDelta(snapshot.devices);
  reason: Implement stable ordering with first_seen initial sort and delta processing
```
/answer 88b5-2-0 allow
Result Stats: id=20099565-89be-4140-aa90-bed612b5233c, total: 14079, in: 6, out: 2307, reason: 0, read: 14504, write: 11766, start: 1794253607939, end: 1794253612806, time: 4782, total: 17779, io: 0, control: 85, sent: 0, recv: 124
Ich habe `devices.js` angepasst. Getestet habe ich es nicht, auch nicht mit `ast_validate`. `devices.config.js` musste ich nicht ändern.

- **Startreihenfolge:** Beim ersten Laden werden die Geräte nach `first_seen` aufsteigend sortiert und bekommen daraus eine laufende Nummer. Geräte ohne `first_seen` stehen am Ende, untereinander nach Namen.
- **Spätere Abrufe:** Jeder Abruf wird als Delta gegen die gemerkte Reihenfolge verarbeitet. Die Anzeige nutzt immer die neuesten Daten vom Backend, die Position bleibt aber erhalten.
- **AP-Wechsel:** Wechselt ein Gerät den AP oder wechselt zwischen WLAN und LAN, bekommt es eine neue Nummer. Es steht dann am Ende seines neuen Abschnitts.
- **Neue Geräte:** Sie werden ebenfalls hinten angehängt, untereinander nach `first_seen`.
- **Verschwundene Geräte:** Sie werden aus der gemerkten Reihenfolge entfernt. Tauchen sie wieder auf, werden sie wie neue Geräte behandelt.
- **Filter:** Filter und „nur verbunden“ ändern die Reihenfolge nicht.

Der bisherige Namensvergleich `byName` heißt noch so, sortiert aber jetzt nach der gemerkten Reihenfolge. Das ist nur ein irreführender Name, ich kann ihn auf Wunsch umbenennen.
