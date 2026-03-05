Gene Scraper - Automated Gene Information Collector

A Python-based web scraper that automatically collects human gene information from biomedical databases (NCBI, UniProt, etc.) and stores the data in Google Sheets for easy monitoring and analysis.


Features
Automated scraping of gene information from multiple sources (NCBI Gene, UniProt)
Google Sheets integration for data storage and visualization
Duplicate detection - automatically skips already collected URLs
Structured data extraction - gene symbol, title, summary, source domain
Configurable via YAML and environment variables
Comprehensive logging for monitoring and debugging


Data collected for each gene
Gene Symbol (e.g., BRCA1, TP53)
Page title
Summary/description
Source URL
Source domain
Collection timestamp


Use cases
Building a custom gene database
Monitoring updates to gene pages
Research data collection
Educational projects


Tech stack
Python 3
BeautifulSoup4 for HTML parsing
Google Sheets API
Requests for HTTP handling
YAML/Env for configuration

