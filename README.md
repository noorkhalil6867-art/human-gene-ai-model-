# gene_scraper

Lightweight scraper to monitor biotech / human gene pages and append new entries into Google Sheets.

Flow:
1. Read list of URLs from urls.txt
2. Scrape each URL for basic metadata (title, first paragraph, etc)
3. Check Google Sheet for existing URL (de-dup)
4. Append new rows with timestamp

Requirements: see requirements.txt
Setup: configure service_account.json and .env (see instructions)
service_account.json contain private_key_id for the data to be scrapped from ncbi. 
