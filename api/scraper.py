import logging
import os

from playwright.async_api import async_playwright
from utilities import parse_date

logger = logging.getLogger(__name__)
START_URL = os.environ.get("START_URL")
SITE_USERNAME = os.environ.get("SITE_USERNAME")
SITE_PASSWORD = os.environ.get("SITE_PASSWORD")

async def scrape_data():
    recordings = []

    async with async_playwright() as playwright:
        chromium = playwright.chromium
        browser = await chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(START_URL, timeout=15000)
        await page.wait_for_selector('input[name="username"]', timeout=15000)
        await page.fill('input[name="username"]', SITE_USERNAME)
        await page.wait_for_selector('input[name="password"]', timeout=15000)
        await page.fill('input[name="password"]', SITE_PASSWORD)
        await page.click('button[type="submit"]')
        await page.wait_for_selector(".recording-item-clickable", timeout=15000)

        while True:
            elements = await page.query_selector_all("a.recording-item-clickable")
            for element in elements:
                try:
                    href = await element.get_attribute("href")
                    link = START_URL + href if href else None
                    thumbnail = await element.query_selector(".recording-item-clickable-thumbnail img")
                    image_url = await thumbnail.get_attribute("src") if thumbnail else None
                    duration_element = await element.query_selector(".duration")
                    duration = await duration_element.inner_text() if duration_element else None
                    date_element = await element.query_selector(".recording-item-clickable-data-match-date")
                    date_str = await date_element.inner_text() if date_element else None
                    date = parse_date(date_str) if date_str else None
                    title_element = await element.query_selector(".recording-item-clickable-data-match-title")
                    title = await title_element.inner_text() if title_element else None

                    recordings.append({
                        "date": date,
                        "title": title,
                        "link": link,
                        "image_url": image_url,
                        "duration": duration
                    })

                except Exception as e:
                    logging.warning(f"Error with an element: {e}")
                    continue

            next_button = await page.query_selector("li.rc-pagination-next[aria-disabled='true']")
            if next_button:
                break

            try:
                next_button = await page.query_selector("li.rc-pagination-next button")
                if next_button:
                    await next_button.click()
                    await page.wait_for_selector("a.recording-item-clickable", timeout=5000)
                    await page.wait_for_timeout(1000)
                else:
                    break
            except Exception as e:
                logging.warning(f"There is no next page: {e}")
                break

        await browser.close()
        logging.info(f"Finalized scraper with {len(recordings)} elements.")

    return recordings
