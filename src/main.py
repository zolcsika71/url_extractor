# src/main.py
from url_extractor.url_extractor import URLExtractor
from url_extractor.logger import setup_logging
import sys


def main():
    # Setup logging
    logger = setup_logging()

    # Get base URL from user
    base_url = input("Please enter the base URL to extract sub-URLs from: ").strip()

    # Initialize extractor
    extractor = URLExtractor(base_url)

    # Extract URLs
    urls = extractor.extract_urls()

    if urls:
        # Export URLs to file named {base_url}.txt
        if extractor.export_urls(urls):
            print("\nURLs have been successfully exported")
        else:
            print("\nFailed to export URLs")
            sys.exit(1)
    else:
        print("\nFailed to extract URLs")
        sys.exit(1)


if __name__ == "__main__":
    main()