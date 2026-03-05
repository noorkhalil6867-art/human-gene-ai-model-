import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def fetch_html(url, user_agent=None, timeout=15):
    headers = {"User-Agent": user_agent} if user_agent else {}
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.text

def parse_generic(url, html):
    """
    Generic fallback parser:
    - title: <title>
    - first paragraph under main content (heuristic)
    - source domain
    """
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("title")
    title = title_tag.text.strip() if title_tag else ""

    # Heuristic: first <p> in body
    p = soup.body.find("p") if soup.body else None
    first_para = p.get_text(strip=True) if p else ""

    # For gene-specific pages, add site-specific parsing below:
    parsed = urlparse(url)
    domain = parsed.netloc

    # Site specific example: NCBI gene pages (simple heuristic)
    gene_symbol = ""
    if "ncbi.nlm.nih.gov" in domain:
        # try to find h1 or span with gene symbol
        h1 = soup.find("h1")
        if h1:
            gene_symbol = h1.get_text(strip=True)

    # UniProt example
    if "uniprot.org" in domain:
        # UniProt often has <h1> with entry name
        h1 = soup.find("h1")
        if h1:
            gene_symbol = h1.get_text(strip=True)

    return {
        "title": title,
        "summary": first_para,
        "gene_symbol": gene_symbol,
        "domain": domain
    }

def scrape_gene(url, user_agent=None):
    html = fetch_html(url, user_agent=user_agent)
    data = parse_generic(url, html)
    return data
if __name__ == "__main__":
    test_url = "https://www.ncbi.nlm.nih.gov/gene/672"  # BRCA1 gene page
    result = scrape_gene(test_url, user_agent="gene_scraper/1.0")
    print(result)