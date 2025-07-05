import asyncio
import json
import logging
import sys

from scraper import scrape_data

logger = logging.getLogger(__name__)

async def main():
    try:
        data = await scrape_data()
        print(json.dumps(data, default=str))
        logging.info(f"Completed scraping with {len(data)} elements.")
    except Exception as e:
        print(f"Scraping failed: {e}", file=sys.stderr)
        logging.error(f"Error in the scraping: {e}")

if __name__ == "__main__":
    asyncio.run(main())
