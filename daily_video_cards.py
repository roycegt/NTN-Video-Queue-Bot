#!/usr/bin/env python3
"""
Creates 15 new "Pending" video task cards in the Notion Video Queue
database, dated today. Meant to run once per day (cron, Task Scheduler,
or a GitHub Actions schedule -- see README.md for setup).

Required environment variables:
  NOTION_TOKEN            Your Notion internal integration secret.
  NOTION_DATA_SOURCE_ID   (optional) Overrides the default data source
                          below if you point this at a different board.

Usage:
  NOTION_TOKEN=secret_xxx python3 daily_video_cards.py
"""

import os
import sys
import datetime
import requests

NOTION_VERSION = "2025-09-03"
API_URL = "https://api.notion.com/v1/pages"

# The "Video Queue" data source created in the "Daily Video Tasks" page.
DEFAULT_DATA_SOURCE_ID = "29626529-dd5a-451a-b8ac-30a94a3a44df"
NUM_VIDEOS = 15


def create_card(token: str, data_source_id: str, video_number: int, date_str: str) -> None:
    payload = {
        "parent": {"type": "data_source_id", "data_source_id": data_source_id},
        "properties": {
            "Video": {"title": [{"text": {"content": f"Video {video_number}"}}]},
            "Status": {"select": {"name": "Pending"}},
            "Video #": {"number": video_number},
            "Date": {"date": {"start": date_str}},
        },
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=15)
    if resp.status_code >= 300:
        raise RuntimeError(f"Failed to create Video {video_number}: {resp.status_code} {resp.text}")


def main() -> None:
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        sys.exit("Missing NOTION_TOKEN environment variable.")
    data_source_id = os.environ.get("NOTION_DATA_SOURCE_ID", DEFAULT_DATA_SOURCE_ID)
    today = datetime.date.today().isoformat()

    for n in range(1, NUM_VIDEOS + 1):
        create_card(token, data_source_id, n, today)
        print(f"Created Video {n} for {today}")

    print(f"Done — {NUM_VIDEOS} cards created for {today}.")


if __name__ == "__main__":
    main()
