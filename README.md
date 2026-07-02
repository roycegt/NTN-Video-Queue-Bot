# Daily Video Cards — Setup

This creates 15 fresh "Pending" video cards in your Notion Video Queue
every day, automatically.

## 1. Get a Notion integration token (one-time, you do this — not me)

1. Go to https://www.notion.so/my-integrations → **New integration**
2. Name it anything (e.g. "Video Queue Bot") → workspace: roycegoldman's Space
3. Copy the **Internal Integration Secret** it gives you. Treat it like a
   password — never paste it into a chat with me or commit it to a public repo.

## 2. Give the integration access to the database

1. Open the "🎬 Daily Video Tasks" page in Notion
2. Click **Share** (top right) → **Connections** → add the integration
   you just created

## 3. Choose how it runs daily — pick ONE:

### Option A — GitHub Actions (recommended: runs even if your laptop is off)

1. Create a **private** GitHub repo, push this folder to it
2. In the repo: **Settings → Secrets and variables → Actions → New repository secret**
   - Name: `NOTION_TOKEN`
   - Value: (paste the secret from step 1 — only you ever see this)
3. That's it. The workflow in `.github/workflows/daily-video-cards.yml`
   runs every day at 11:00 UTC (6:00 AM Colombia time). Change the
   `cron` line if you want a different time.
4. You can test it immediately: repo → **Actions** tab → "Daily Video
   Cards" → **Run workflow**

### Option B — Cron on your own Mac/Linux machine

Requires your computer to be on and awake at the scheduled time.

1. Store your token somewhere only you can read:
   ```
   echo 'export NOTION_TOKEN=your_token_here' > ~/.notion_env
   chmod 600 ~/.notion_env
   ```
2. `pip3 install requests`
3. `crontab -e` and add:
   ```
   0 6 * * * source ~/.notion_env && /usr/bin/python3 /path/to/daily_video_cards.py >> /path/to/daily_video_cards.log 2>&1
   ```

### Option C — Windows Task Scheduler

1. Make a `run.bat` next to the script:
   ```
   set NOTION_TOKEN=your_token_here
   python daily_video_cards.py
   ```
2. Task Scheduler → Create Basic Task → Trigger: Daily → Action: run `run.bat`

## Notes

- The script only *creates* new cards — old "Done" cards will pile up
  over time. Worth archiving them weekly.
- `NOTION_DATA_SOURCE_ID` is already hardcoded to your Video Queue board.
  Only override it if you point this at a different database.
