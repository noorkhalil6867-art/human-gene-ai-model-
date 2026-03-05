import os
import yaml
from dotenv import load_dotenv
from utils import setup_logger, now_iso
from scraper import scrape_gene
from sheets import get_sheets_service, get_existing_urls, append_rows

def load_config():
    with open("config.yaml", "r", encoding="utf8") as f:
        return yaml.safe_load(f)

def load_urls(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip() and not l.strip().startswith("#")]
    return lines

def build_row(data, url):
    # Decide columns: GeneSymbol, Title, Summary, URL, Domain, DateFound
    return [
        data.get("gene_symbol") or "",
        data.get("title") or "",
        data.get("summary") or "",
        url,
        data.get("domain") or "",
        now_iso()
    ]

def main():
    load_dotenv()
    cfg = load_config()

    logger = setup_logger(cfg.get("logging", {}).get("log_file", "scrape.log"))
    service_account_file = os.getenv("SERVICE_ACCOUNT_FILE", "service_account.json")
    sheet_id = os.getenv("SHEET_ID") or cfg.get("spreadsheet", {}).get("id")
    range_name = cfg.get("spreadsheet", {}).get("range", "Sheet1!A:F")
    urls = load_urls(cfg.get("scraper", {}).get("urls_file", "urls.txt"))
    user_agent = cfg.get("scraper", {}).get("user_agent")

    if not sheet_id:
        logger.error("No SHEET_ID set. Put it in .env or config.yaml.")
        return

    sheets_service = get_sheets_service(service_account_file)
    existing = get_existing_urls(sheet_id, range_name, sheets_service)
    logger.info(f"Loaded {len(existing)} existing URLs from sheet.")

    rows_to_add = []
    for url in urls:
        if url in existing:
            logger.info(f"Skipping existing URL: {url}")
            continue
        try:
            logger.info(f"Scraping {url}")
            data = scrape_gene(url, user_agent=user_agent)
            row = build_row(data, url)
            rows_to_add.append(row)
        except Exception as e:
            logger.exception(f"Error scraping {url}: {e}")

    if rows_to_add:
        append_rows(sheet_id, range_name, rows_to_add, sheets_service)
        logger.info(f"Appended {len(rows_to_add)} new rows.")
    else:
        logger.info("No new rows to append.")

if __name__ == "__main__":
    main()
