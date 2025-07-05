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

def parse_date(date_str: str) -> datetime | None:
    try:
        parts = date_str.strip().split()
        if len(parts) != 3:
            raise ValueError("Unexpected date format")

        day = parts[0].zfill(2)
        month = MONTH_MAP.get(parts[1].upper())
        year = parts[2]

        if not month:
            raise ValueError("Not a valid month")

        return datetime.strptime(f"{day} {month} {year}", "%d %b %Y")

    except Exception as e:
        logger.warning(f"Error parsing the date '{date_str}': {e}")
        return None
