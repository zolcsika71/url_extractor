# src/url_extractor/url_extractor.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
from typing import Set, Optional
from pathlib import Path
import re


def normalize_url(url: str) -> str:
    """Normalize URL to prevent duplicates"""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


class URLExtractor:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.logger = logging.getLogger('url_extractor')
        self.visited_urls: Set[str] = set()

    def get_base_domain(self) -> str:
        """Extract and format base domain for filename"""
        parsed = urlparse(self.base_url)
        # Remove a scheme (http/https) and common prefixes
        domain = parsed.netloc.replace('www.', '')
        # Replace invalid filename characters with underscores
        domain = re.sub(r'[^\w\-_.]', '_', domain)
        return domain

    def extract_urls(self, max_depth: int = 1) -> Optional[Set[str]]:
        """Extract all sub-URLs from the base URL"""
        try:
            self.logger.info(f"Starting URL extraction from: {self.base_url}")

            response = requests.get(self.base_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            urls = set()
            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    absolute_url = urljoin(self.base_url, href)
                    normalized_url = normalize_url(absolute_url)

                    # Only include URLs from the same domain
                    if urlparse(normalized_url).netloc == urlparse(self.base_url).netloc:
                        urls.add(normalized_url)

            self.logger.info(f"Found {len(urls)} unique URLs")
            return urls

        except requests.RequestException as e:
            self.logger.error(f"Error fetching URLs: {str(e)}")
            return None

    def export_urls(self, urls: Set[str]) -> bool:
        """Export URLs to a text file named {base_url}.txt"""
        try:
            # Create output directory if it doesn't exist
            output_dir = Path(__file__).parent.parent.parent / 'output'
            output_dir.mkdir(exist_ok=True)

            # Generate filename based on base URL
            filename = f"{self.get_base_domain()}.txt"
            output_file = output_dir / filename

            # Write URLs in a simple list format
            with open(output_file, 'w') as f:
                # Add base URL first
                f.write(f"{self.base_url}\n")
                # Add all other URLs, sorted for consistency
                for url in sorted(urls):
                    if url != self.base_url:  # Avoid duplicate base URL
                        f.write(f"{url}\n")

            self.logger.info(f"Successfully exported URLs to {output_file}")
            return True

        except IOError as e:
            self.logger.error(f"Error writing to file: {str(e)}")
            return False