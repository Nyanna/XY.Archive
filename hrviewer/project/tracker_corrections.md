Der Tracker soll über `/home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome` mit MQTTDuck starten.
Der Listing Endpunkt soll entsprechend in Smarthome integriert werden.

- `/home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/tracking/__main__.py` (kann dann entfernt werden)
- `/home/user/xyan/XY.Archiv/hrviewer/src/xy/smarthome/tracking/web.py

Folgender Punkt kannt korrigiert werden:`
- **LAN-Geräte:** `connected` kann implementiert werden, wenn der die letzte Sichtung über DHCP weniger als 8 Stunden zurückliegt