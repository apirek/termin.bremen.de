import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup

import termine


def test_termine(tmp_path):
    """
    Teste Holen und Parsen von Terminen.
    """
    url = "https://termin.bremen.de/termine/directentry?mdt=4&loc=3&cnc-1705=1"
    soup = termine.get_soup(url)
    with open(tmp_path / "soup.html", "w") as f:
        f.write(str(soup))
    appointments = list(termine.parse_appointments(soup))
    with open(tmp_path / "appointments.txt", "w") as f:
        for a in appointments:
            f.write(str(a) + "\n")
    # Ich weiß nicht in welchen Fällen es keine Termine gibt.
    assert len(appointments) > 0
    # Ich vertraue nicht darauf, dass Termine sofort gelöscht werden und unsere Uhren gleich genug gehen.
    yesterday = datetime.now() - timedelta(hours=24)
    assert appointments[0].date >= yesterday
