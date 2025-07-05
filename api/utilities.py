import logging

from datetime import datetime


logger = logging.getLogger(__name__)

MONTH_MAP = {
    "JAN": "Jan",
    "ENE": "Jan",
    "FEB": "Feb",
    "MAR": "Mar",
    "APR": "Apr",
    "ABR": "Apr",
    "MAY": "May",
    "JUN": "Jun",
    "JUL": "Jul",
    "AUG": "Aug",
    "AGO": "Aug",
    "SEP": "Sep",
    "SEPT": "Sep",
    "OCT": "Oct",
    "NOV": "Nov",
    "DEC": "Dec",
    "DIC": "Dec"
}

SPANISH_MONTHS = {
    'ENE': 'JAN', 'FEB': 'FEB', 'MAR': 'MAR', 'ABR': 'APR',
    'MAY': 'MAY', 'JUN': 'JUN', 'JUL': 'JUL', 'AGO': 'AUG',
    'SEP': 'SEP', 'SEPT': 'SEP', 'OCT': 'OCT', 'NOV': 'NOV', 'DIC': 'DEC'
}

def parse_date(raw_date: str) -> datetime | None:
    try:
        parts = raw_date.strip().upper().split()
        if len(parts) != 3:
            raise ValueError(f"Not a valid format: {raw_date}")

        day, mon, year = parts
        mon_eng = SPANISH_MONTHS.get(mon)
        if not mon_eng:
            raise ValueError(f"Invalid month: {mon}")

        translated_date = f"{mon_eng} {day} {year}"
        return datetime.strptime(translated_date, "%b %d %Y")

    except Exception as e:
        print(f"Error parsing the date '{raw_date}': {e}")
        return None
