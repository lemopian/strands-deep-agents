"""
Web Scraper Module

A robust web scraper that fetches content from URLs and parses HTML
to extract specific data with comprehensive error handling.
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Union
import logging
from urllib.parse import urljoin, urlparse
import time


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WebScraperError(Exception):
    """Base exception for WebScraper errors"""
    pass


class WebScraper:
    """
    A flexible web scraper for fetching and parsing HTML content.
    
    Attributes:
        timeout (int): Request timeout in seconds
        headers (dict): HTTP headers for requests
        session (requests.Session): Persistent session for requests
    """
    
    def __init__(self, timeout: int = 10, custom_headers: Optional[Dict[str, str]] = None):
        """
        Initialize the WebScraper.
        
        Args:
            timeout: Request timeout in seconds (default: 10)
            custom_headers: Optional custom headers for requests
        """
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        if custom_headers:
            self.headers.update(custom_headers)
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def fetch_url(self, url: str, retries: int = 3) -> Optional[requests.Response]:
        """
        Fetch content from a URL with retry logic.
        
        Args:
            url: The URL to fetch
            retries: Number of retry attempts (default: 3)
            
        Returns:
            Response object if successful, None otherwise
            
        Raises:
            WebScraperError: If all retry attempts fail
        """
        if not url or not isinstance(url, str):
            raise WebScraperError("Invalid URL provided")
        
        # Validate URL format
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise WebScraperError(f"Invalid URL format: {url}")
        
        for attempt in range(retries):
            try:
                logger.info(f"Fetching URL: {url} (Attempt {attempt + 1}/{retries})")
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                logger.info(f"Successfully fetched URL: {url}")
                return response
                
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout occurred for {url} (Attempt {attempt + 1}/{retries})")
                if attempt == retries - 1:
                    raise WebScraperError(f"Timeout after {retries} attempts")
                time.sleep(1 * (attempt + 1))  # Exponential backoff
                
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP error for {url}: {e}")
                raise WebScraperError(f"HTTP error: {e}")
                
            except requests.exceptions.ConnectionError:
                logger.warning(f"Connection error for {url} (Attempt {attempt + 1}/{retries})")
                if attempt == retries - 1:
                    raise WebScraperError(f"Connection failed after {retries} attempts")
                time.sleep(1 * (attempt + 1))
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error for {url}: {e}")
                raise WebScraperError(f"Request error: {e}")
        
        return None
    
    def parse_html(self, html_content: str, parser: str = 'html.parser') -> BeautifulSoup:
        """
        Parse HTML content using BeautifulSoup.
        
        Args:
            html_content: Raw HTML string
            parser: Parser to use (default: 'html.parser')
            
        Returns:
            BeautifulSoup object
            
        Raises:
            WebScraperError: If parsing fails
        """
        try:
            soup = BeautifulSoup(html_content, parser)
            logger.info("Successfully parsed HTML content")
            return soup
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            raise WebScraperError(f"HTML parsing error: {e}")
    
    def extract_text(self, soup: BeautifulSoup, selector: str) -> List[str]:
        """
        Extract text content using CSS selector.
        
        Args:
            soup: BeautifulSoup object
            selector: CSS selector string
            
        Returns:
            List of text strings from matching elements
        """
        try:
            elements = soup.select(selector)
            texts = [elem.get_text(strip=True) for elem in elements]
            logger.info(f"Extracted {len(texts)} elements using selector: {selector}")
            return texts
        except Exception as e:
            logger.error(f"Error extracting text with selector '{selector}': {e}")
            return []
    
    def extract_links(self, soup: BeautifulSoup, base_url: str = None) -> List[str]:
        """
        Extract all links from the page.
        
        Args:
            soup: BeautifulSoup object
            base_url: Base URL for resolving relative links
            
        Returns:
            List of absolute URLs
        """
        try:
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if base_url:
                    href = urljoin(base_url, href)
                links.append(href)
            
            logger.info(f"Extracted {len(links)} links")
            return links
        except Exception as e:
            logger.error(f"Error extracting links: {e}")
            return []
    
    def extract_data(self, soup: BeautifulSoup, selectors: Dict[str, str]) -> Dict[str, Union[str, List[str]]]:
        """
        Extract multiple data points using a dictionary of selectors.
        
        Args:
            soup: BeautifulSoup object
            selectors: Dictionary mapping field names to CSS selectors
            
        Returns:
            Dictionary with extracted data
        """
        data = {}
        for field, selector in selectors.items():
            try:
                elements = soup.select(selector)
                if len(elements) == 1:
                    data[field] = elements[0].get_text(strip=True)
                elif len(elements) > 1:
                    data[field] = [elem.get_text(strip=True) for elem in elements]
                else:
                    data[field] = None
                    logger.warning(f"No elements found for selector '{selector}' (field: {field})")
            except Exception as e:
                logger.error(f"Error extracting field '{field}': {e}")
                data[field] = None
        
        return data
    
    def scrape(self, url: str, selectors: Optional[Dict[str, str]] = None) -> Dict[str, any]:
        """
        Complete scraping workflow: fetch, parse, and extract data.
        
        Args:
            url: URL to scrape
            selectors: Optional dictionary of CSS selectors for data extraction
            
        Returns:
            Dictionary containing scraped data and metadata
        """
        try:
            # Fetch the page
            response = self.fetch_url(url)
            
            # Parse HTML
            soup = self.parse_html(response.text)
            
            # Extract data
            result = {
                'url': url,
                'status_code': response.status_code,
                'title': soup.title.string if soup.title else None,
            }
            
            # Extract custom data if selectors provided
            if selectors:
                result['data'] = self.extract_data(soup, selectors)
            
            logger.info(f"Successfully scraped data from {url}")
            return result
            
        except WebScraperError as e:
            logger.error(f"Scraping failed for {url}: {e}")
            return {
                'url': url,
                'error': str(e),
                'status': 'failed'
            }
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return {
                'url': url,
                'error': f"Unexpected error: {str(e)}",
                'status': 'failed'
            }
    
    def close(self):
        """Close the session."""
        self.session.close()
        logger.info("Scraper session closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Example usage
if __name__ == "__main__":
    # Example 1: Basic scraping
    with WebScraper() as scraper:
        result = scraper.scrape('https://example.com')
        print(f"Title: {result.get('title')}")
        print(f"Status: {result.get('status_code')}")
    
    # Example 2: Extract specific data
    with WebScraper() as scraper:
        selectors = {
            'heading': 'h1',
            'paragraphs': 'p',
            'links': 'a'
        }
        result = scraper.scrape('https://example.com', selectors=selectors)
        
        if 'error' not in result:
            print(f"\nTitle: {result['title']}")
            print(f"Data: {result['data']}")
        else:
            print(f"Error: {result['error']}")
