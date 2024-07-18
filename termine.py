#!/usr/bin/python
"""
termine.py
Copyright (C) 2023 Axel Pirek

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Generator
import hashlib
import os
import pickle
import sys

from bs4 import BeautifulSoup
import requests


@dataclass
class Appointment:
    date: datetime
    #available: bool = True

    def __str__(self) -> str:
        return self.date.strftime("%Y-%m-%d %H:%M")

    def __lt__(self, other) -> bool:
        return self.date < other.date

    def __le__(self, other) -> bool:
        return self.date <= other.date

    def __eq__(self, other) -> bool:
        return self.date == other.date

    def __hash__(self) -> int:
        return hash(self.date)


def get_soup(url) -> BeautifulSoup:
    session = requests.Session()
    session.headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0",
    }
    response = session.get(url, allow_redirects=True)
    return BeautifulSoup(response.text, "html.parser")


def parse_appointments(soup) -> Generator[Appointment, None, None]:
    if elem := soup.find("h1", class_="error"):
        # elem.next_sibling ist \n, p kommt danach.
        raise RuntimeError(elem.next_sibling.next_sibling)
    for button in soup.find_all("button"):
        # Freie Termine haben button und form, belegte Termine haben disabled button und kein form.
        if button.disabled or button.parent.name != "form":
            continue
        form = button.parent
        date = form.find("input", {"name": "date"})["value"]
        time = button["title"]
        date = datetime.strptime(f"{date}{time}", "%Y%m%d%H:%M")
        yield Appointment(date=date)


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("url", metavar="URL", help="Terminvergabe-URL")
    parser.add_argument("date", metavar="DATE", help="Zeige nur Termine vor diesem (%%Y-%%m-%%d %%H:%%M)",
                        type=lambda s: datetime.strptime(s, "%Y-%m-%d %H:%M"))
    parser.add_argument("-c", action="store_true", help="Zeige nur neue Termine seit dem letzten Aufruf",
                        dest="cache")
    args = parser.parse_args()

    soup = get_soup(args.url)
    appointments = set(parse_appointments(soup))

    if args.cache:
        cache_dir = Path(os.getenv("XDG_CACHE_DIR") or Path(Path.home(), ".cache"), "termin.bremen.de")
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = Path(cache_dir, hashlib.sha256(bytes(args.url, "utf-8")).hexdigest())
        try:
            with open(cache_file, "rb") as f:
                cached_appointments = pickle.load(f)
        except FileNotFoundError:
            cached_appointments = set()
        with open(cache_file, "wb") as f:
            pickle.dump(appointments, f)
        appointments = appointments - cached_appointments

    ret = 1
    for appointment in sorted(appointments):
        if appointment.date >= args.date:
            break
        print(appointment)
        ret = 0

    return ret


if __name__ == "__main__":
    sys.exit(main())
