from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup

import termine


def test_termine():
    """
    Teste Holen und Parsen von Terminen.
    """
    url = "https://termin.bremen.de/termine/directentry?mdt=3&loc=2&cnc-57=1"
    soup = termine.get_soup(url)
    # Antwort ist auch bei falschen Query-Parametern 200 OK. Suche nach bekanntem String.
    assert soup.find(string="Terminvorschläge:")
    appointments = list(termine.parse_appointments(soup))
    # Ich weiß nicht in welchen Fällen es keine Termine gibt.
    assert len(appointments) > 0
    # Ich vertraue nicht darauf, dass Termine sofort gelöscht werden und unsere Uhren gleich genug gehen.
    yesterday = datetime.now(tz=ZoneInfo("Europe/Berlin")) - timedelta(hours=24)
    assert appointments[0].date >= yesterday
