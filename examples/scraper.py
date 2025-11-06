"""
Web Scraper Module

A flexible web scraper that fetches content from URLs and parses HTML to extract data.
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Union
import logging
from urllib.parse import urlparse
import time


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WebScraper:
    """
    A web scraper class for fetching and parsing HTML content from URLs.
    
    Attributes:
        timeout (int): Request timeout in seconds
        headers (dict): HTTP headers to send with requests
        session (requests.Session): Reusable session for multiple requests
    """
    
    def __init__(self, timeout: int = 10, headers: Optional[Dict[str, str]] = None):
        """
        Initialize the WebScraper.
        
        Args:
            timeout (int): Request timeout in seconds (default: 10)
            headers (dict): Custom HTTP headers (default: user-agent only)
        """
        self.timeout = timeout
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def fetch_url(self, url: str, retries: int = 3) -> Optional[requests.Response]:
        """
        Fetch content from a URL with error handling and retries.
        
        Args:
            url (str): The URL to fetch
            retries (int): Number of retry attempts on failure
            
        Returns:
            requests.Response: Response object if successful, None otherwise
        """
        # Validate URL
        if not self._is_valid_url(url):
            logger.error(f"Invalid URL format: {url}")
            return None
        
        for attempt in range(retries):
            try:
                logger.info(f"Fetching URL: {url} (Attempt {attempt + 1}/{retries})")
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                logger.info(f"Successfully fetched {url}")
                return response
                
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout error for {url} (Attempt {attempt + 1}/{retries})")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP error for {url}: {e}")
                return None
                
            except requests.exceptions.ConnectionError:
                logger.warning(f"Connection error for {url} (Attempt {attempt + 1}/{retries})")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error for {url}: {e}")
                return None
        
        logger.error(f"Failed to fetch {url} after {retries} attempts")
        return None
    
    def parse_html(self, html_content: str) -> Optional[BeautifulSoup]:
        """
        Parse HTML content using BeautifulSoup.
        
        Args:
            html_content (str): Raw HTML content
            
        Returns:
            BeautifulSoup: Parsed HTML object, None if parsing fails
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return None
    
    def extract_data(self, soup: BeautifulSoup, 
                    selectors: Dict[str, str]) -> Dict[str, Union[str, List[str]]]:
        """
        Extract specific data from parsed HTML using CSS selectors.
        
        Args:
            soup (BeautifulSoup): Parsed HTML object
            selectors (dict): Dictionary mapping field names to CSS selectors
            
        Returns:
            dict: Extracted data with field names as keys
        """
        extracted_data = {}
        
        for field_name, selector in selectors.items():
            try:
                elements = soup.select(selector)
                
                if not elements:
                    logger.warning(f"No elements found for selector '{selector}'")
                    extracted_data[field_name] = None
                elif len(elements) == 1:
                    extracted_data[field_name] = elements[0].get_text(strip=True)
                else:
                    extracted_data[field_name] = [elem.get_text(strip=True) for elem in elements]
                    
            except Exception as e:
                logger.error(f"Error extracting data for '{field_name}': {e}")
                extracted_data[field_name] = None
        
        return extracted_data
    
    def scrape(self, url: str, selectors: Dict[str, str]) -> Optional[Dict[str, Union[str, List[str]]]]:
        """
        Complete scraping workflow: fetch, parse, and extract data.
        
        Args:
            url (str): The URL to scrape
            selectors (dict): Dictionary mapping field names to CSS selectors
            
        Returns:
            dict: Extracted data, or None if scraping fails
        """
        # Fetch the URL
        response = self.fetch_url(url)
        if not response:
            return None
        
        # Parse HTML
        soup = self.parse_html(response.text)
        if not soup:
            return None
        
        # Extract data
        data = self.extract_data(soup, selectors)
        return data
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Validate URL format.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def close(self):
        """Close the session."""
        self.session.close()
        logger.info("Session closed")


def main():
    """
    Example usage of the WebScraper class.
    """
    # Initialize scraper
    scraper = WebScraper(timeout=15)
    
    # Example: Scrape a website (using a public example site)
    url = "https://example.com"
    
    # Define what data to extract using CSS selectors
    selectors = {
        'title': 'h1',
        'paragraphs': 'p',
        'links': 'a'
    }
    
    try:
        # Perform scraping
        logger.info("Starting scrape operation...")
        data = scraper.scrape(url, selectors)
        
        if data:
            logger.info("Scraping completed successfully!")
            print("\n=== Extracted Data ===")
            for key, value in data.items():
                print(f"\n{key.upper()}:")
                if isinstance(value, list):
                    for item in value:
                        print(f"  - {item}")
                else:
                    print(f"  {value}")
        else:
            logger.error("Scraping failed")
            
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
