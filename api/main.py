import logging

from fastapi import FastAPI
import json
import os
import psycopg2
import subprocess
import sys


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

app = FastAPI()

DB_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "port": os.environ.get("DB_PORT"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "dbname": os.environ.get("DB_NAME"),
}

def save_to_db(data):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS recordings (
                    id SERIAL PRIMARY KEY,
                    date TIMESTAMP NOT NULL,
                    title TEXT NOT NULL,
                    link TEXT NOT NULL,
                    image_url TEXT NOT NULL,
                    duration TEXT NOT NULL,
                    CONSTRAINT unique_link UNIQUE(link)
                )
            """)
    cur.executemany("""
                    INSERT INTO recordings (date, title, link, image_url, duration)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (link)
                    DO UPDATE SET
                        date = EXCLUDED.date,
                        title = EXCLUDED.title,
                        image_url = EXCLUDED.image_url,
                        duration = EXCLUDED.duration
                    """, [(i["date"], i["title"], i["link"], i["image_url"], i["duration"]) for i in data])
    conn.commit()
    cur.close()
    conn.close()


@app.get("/")
def root():
    return {"message": "Active API"}


@app.get("/scrape")
async def run_scraping():
    result = subprocess.run(
        [sys.executable, os.path.join(os.path.dirname(__file__), "scraper_runner.py")],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {"error": result.stderr}

    try:
        data = json.loads(result.stdout)
    except Exception as e:
        return {
            "error": "Cannot parse JSON",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exception": str(e)
        }

    save_to_db(data)
    return {"status": "ok", "items": len(data)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
