#!/usr/bin/python
from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime
from typing import Generator
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
    args = parser.parse_args()

    soup = get_soup(args.url)
    appointments = set(parse_appointments(soup))

    ret = 1
    for appointment in sorted(appointments):
        if appointment.date >= args.date:
            break
        print(appointment)
        ret = 0

    return ret


if __name__ == "__main__":
    sys.exit(main())
