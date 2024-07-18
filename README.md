# termin.bremen.de
Prüft die elektronische Terminvereinbarung der Bremer Behörden auf frühere Termine.

Die Funktionalität wird täglich durch GitHub Actions geprüft: [![Test](https://github.com/apirek/termin.bremen.de/actions/workflows/test.yml/badge.svg)](https://github.com/apirek/termin.bremen.de/actions/workflows/test.yml)

## Beschreibung
Kopiere den "Frühestmöglicher Termin"-Link von einer Dienstleistungs-Seite, z.B. https://termin.bremen.de/termine/directentry?mdt=6&loc=5&cnc-181=1 von [Kraftfahrzeug anmelden](https://www.service.bremen.de/dienstleistungen/kraftfahrzeug-anmelden-8389).
Starte `./termine.py` mit dem Link und einen Zeitpunkt, vor dem freie Termine aufgelistet werden sollen: 
```sh
./termine.py "https://termin.bremen.de/termine/directentry?mdt=6&loc=5&cnc-181=1" "2024-07-31 18:00"
```
Frühere Termine werden ausgegeben oder das Programm beendet mit Status 1:
```
2024-07-25 14:45
```
