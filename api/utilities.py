import logging

from datetime import datetime


logger = logging.getLogger(__name__)

MONTHS_MAP = {
    "ENE": "JAN", "FEB": "FEB", "MAR": "MAR", "ABR": "APR",
    "MAY": "MAY", "JUN": "JUN", "JUL": "JUL", "AGO": "AUG",
    "SEP": "SEP", "OCT": "OCT", "NOV": "NOV", "DIC": "DEC"
}

def parse_date(date_str: str) -> datetime:
    clean_date = date_str.replace(",", "").strip().upper()
    parts = clean_date.split()

    if len(parts) != 3:
        raise ValueError(f"Invalid date format: '{date_str}'")

    month, day, year = parts
    parsed_month = MONTHS_MAP.get(month, month)
    date = f"{parsed_month} {day} {year}"

    return datetime.strptime(date, "%b %d %Y")
