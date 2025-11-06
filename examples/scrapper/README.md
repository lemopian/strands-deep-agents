# WebScraper

A robust, flexible Python web scraper for fetching and parsing HTML content with comprehensive error handling and retry logic.

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Robust URL Fetching**: Automatically retries failed requests with exponential backoff
- **HTML Parsing**: Powered by BeautifulSoup for reliable HTML parsing
- **Flexible Data Extraction**: Use CSS selectors to extract specific data
- **Error Handling**: Comprehensive error handling with custom exceptions
- **Context Manager Support**: Clean resource management with `with` statements
- **Session Management**: Persistent HTTP sessions for better performance
- **Logging**: Built-in logging for debugging and monitoring
- **Link Extraction**: Automatically extract and resolve relative URLs
- **Custom Headers**: Support for custom HTTP headers
- **Timeout Control**: Configurable request timeouts

## 📦 Installation

### Prerequisites

- Python 3.7 or higher

### Install Dependencies

```bash
pip install requests beautifulsoup4
```

Or using a requirements.txt file:

```bash
# requirements.txt
requests>=2.28.0
beautifulsoup4>=4.11.0
```

```bash
pip install -r requirements.txt
```

### Optional: Install Additional Parsers

For better performance, you can install additional HTML parsers:

```bash
# lxml parser (faster)
pip install lxml

# html5lib parser (more lenient)
pip install html5lib
```

## 🚀 Quick Start

Here's a simple example to get you started:

```python
from scraper import WebScraper

# Create a scraper instance
with WebScraper() as scraper:
    # Scrape a webpage
    result = scraper.scrape('https://example.com')
    
    # Print the page title
    print(f"Title: {result.get('title')}")
    print(f"Status: {result.get('status_code')}")
```

## 📖 Usage Examples

### Example 1: Basic URL Scraping

```python
from scraper import WebScraper

# Using context manager (recommended)
with WebScraper() as scraper:
    result = scraper.scrape('https://example.com')
    
    if 'error' not in result:
        print(f"URL: {result['url']}")
        print(f"Status Code: {result['status_code']}")
        print(f"Title: {result['title']}")
    else:
        print(f"Error: {result['error']}")
```

### Example 2: Custom Data Extraction with CSS Selectors

```python
from scraper import WebScraper

# Define CSS selectors for data extraction
selectors = {
    'main_heading': 'h1',
    'paragraphs': 'p',
    'links': 'a',
    'article_title': 'article h2',
    'prices': '.price'
}

with WebScraper() as scraper:
    result = scraper.scrape('https://example.com', selectors=selectors)
    
    if 'error' not in result:
        data = result['data']
        print(f"Main Heading: {data.get('main_heading')}")
        print(f"Paragraphs: {data.get('paragraphs')}")
        print(f"All Links: {data.get('links')}")
    else:
        print(f"Scraping failed: {result['error']}")
```

### Example 3: Manual Control (Fetch, Parse, Extract)

```python
from scraper import WebScraper

with WebScraper() as scraper:
    # Step 1: Fetch the URL
    response = scraper.fetch_url('https://example.com')
    
    # Step 2: Parse the HTML
    soup = scraper.parse_html(response.text)
    
    # Step 3: Extract specific text
    headings = scraper.extract_text(soup, 'h2')
    print(f"All H2 headings: {headings}")
    
    # Step 4: Extract all links
    links = scraper.extract_links(soup, base_url='https://example.com')
    print(f"Found {len(links)} links")
```

### Example 4: Extracting Links

```python
from scraper import WebScraper

with WebScraper() as scraper:
    # Fetch and parse
    response = scraper.fetch_url('https://example.com')
    soup = scraper.parse_html(response.text)
    
    # Extract all links (converts relative to absolute URLs)
    links = scraper.extract_links(soup, base_url='https://example.com')
    
    print(f"Found {len(links)} links:")
    for link in links[:5]:  # Print first 5 links
        print(f"  - {link}")
```

### Example 5: Custom Headers and Timeout

```python
from scraper import WebScraper

# Custom headers for authentication or specific requirements
custom_headers = {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://example.com'
}

# Create scraper with custom configuration
scraper = WebScraper(timeout=30, custom_headers=custom_headers)

try:
    result = scraper.scrape('https://api.example.com/data')
    print(result)
finally:
    scraper.close()  # Don't forget to close if not using context manager
```

### Example 6: Error Handling

```python
from scraper import WebScraper, WebScraperError

with WebScraper() as scraper:
    try:
        response = scraper.fetch_url('https://example.com', retries=5)
        soup = scraper.parse_html(response.text)
        data = scraper.extract_text(soup, 'h1')
        print(f"Extracted: {data}")
        
    except WebScraperError as e:
        print(f"Scraping error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

### Example 7: Scraping Multiple Pages

```python
from scraper import WebScraper

urls = [
    'https://example.com/page1',
    'https://example.com/page2',
    'https://example.com/page3'
]

selectors = {
    'title': 'h1',
    'content': '.article-content p'
}

with WebScraper() as scraper:
    results = []
    
    for url in urls:
        print(f"Scraping: {url}")
        result = scraper.scrape(url, selectors=selectors)
        results.append(result)
    
    # Process results
    for result in results:
        if 'error' not in result:
            print(f"\n{result['url']}:")
            print(f"  Title: {result['title']}")
            print(f"  Data: {result['data']}")
```

### Example 8: Using Different HTML Parsers

```python
from scraper import WebScraper

with WebScraper() as scraper:
    response = scraper.fetch_url('https://example.com')
    
    # Use lxml parser (requires: pip install lxml)
    soup = scraper.parse_html(response.text, parser='lxml')
    
    # Or use html5lib parser (requires: pip install html5lib)
    # soup = scraper.parse_html(response.text, parser='html5lib')
    
    data = scraper.extract_text(soup, 'article')
    print(data)
```

## 📚 API Reference

### WebScraper Class

The main class for web scraping operations.

#### Constructor

```python
WebScraper(timeout: int = 10, custom_headers: Optional[Dict[str, str]] = None)
```

**Parameters:**
- `timeout` (int, optional): Request timeout in seconds. Default: 10
- `custom_headers` (dict, optional): Custom HTTP headers to include in requests

**Example:**
```python
scraper = WebScraper(timeout=30, custom_headers={'Authorization': 'Bearer TOKEN'})
```

---

#### `fetch_url()`

Fetch content from a URL with automatic retry logic.

```python
fetch_url(url: str, retries: int = 3) -> Optional[requests.Response]
```

**Parameters:**
- `url` (str): The URL to fetch
- `retries` (int, optional): Number of retry attempts. Default: 3

**Returns:**
- `requests.Response`: Response object if successful

**Raises:**
- `WebScraperError`: If all retry attempts fail or URL is invalid

**Example:**
```python
response = scraper.fetch_url('https://example.com', retries=5)
print(response.status_code)
```

---

#### `parse_html()`

Parse HTML content using BeautifulSoup.

```python
parse_html(html_content: str, parser: str = 'html.parser') -> BeautifulSoup
```

**Parameters:**
- `html_content` (str): Raw HTML string to parse
- `parser` (str, optional): Parser to use. Default: 'html.parser'
  - Options: 'html.parser', 'lxml', 'html5lib'

**Returns:**
- `BeautifulSoup`: Parsed BeautifulSoup object

**Raises:**
- `WebScraperError`: If parsing fails

**Example:**
```python
soup = scraper.parse_html(response.text, parser='lxml')
```

---

#### `extract_text()`

Extract text content using CSS selectors.

```python
extract_text(soup: BeautifulSoup, selector: str) -> List[str]
```

**Parameters:**
- `soup` (BeautifulSoup): BeautifulSoup object to extract from
- `selector` (str): CSS selector string

**Returns:**
- `List[str]`: List of text strings from matching elements

**Example:**
```python
headings = scraper.extract_text(soup, 'h1, h2, h3')
paragraphs = scraper.extract_text(soup, 'article p')
```

---

#### `extract_links()`

Extract all links from the page.

```python
extract_links(soup: BeautifulSoup, base_url: str = None) -> List[str]
```

**Parameters:**
- `soup` (BeautifulSoup): BeautifulSoup object to extract from
- `base_url` (str, optional): Base URL for resolving relative links

**Returns:**
- `List[str]`: List of absolute URLs

**Example:**
```python
links = scraper.extract_links(soup, base_url='https://example.com')
```

---

#### `extract_data()`

Extract multiple data points using a dictionary of selectors.

```python
extract_data(soup: BeautifulSoup, selectors: Dict[str, str]) -> Dict[str, Union[str, List[str]]]
```

**Parameters:**
- `soup` (BeautifulSoup): BeautifulSoup object to extract from
- `selectors` (dict): Dictionary mapping field names to CSS selectors

**Returns:**
- `dict`: Dictionary with extracted data
  - Single element: returns string
  - Multiple elements: returns list of strings
  - No elements: returns None

**Example:**
```python
selectors = {
    'title': 'h1',
    'author': '.author-name',
    'tags': '.tag'
}
data = scraper.extract_data(soup, selectors)
```

---

#### `scrape()`

Complete scraping workflow: fetch, parse, and extract data.

```python
scrape(url: str, selectors: Optional[Dict[str, str]] = None) -> Dict[str, any]
```

**Parameters:**
- `url` (str): URL to scrape
- `selectors` (dict, optional): Dictionary of CSS selectors for data extraction

**Returns:**
- `dict`: Dictionary containing scraped data and metadata
  - On success: `{'url': str, 'status_code': int, 'title': str, 'data': dict}`
  - On failure: `{'url': str, 'error': str, 'status': 'failed'}`

**Example:**
```python
result = scraper.scrape('https://example.com', selectors={'heading': 'h1'})
```

---

#### `close()`

Close the HTTP session and release resources.

```python
close()
```

**Example:**
```python
scraper = WebScraper()
# ... use scraper ...
scraper.close()
```

---

#### Context Manager Protocol

The WebScraper class supports the context manager protocol for automatic resource cleanup.

```python
with WebScraper() as scraper:
    # Use scraper
    pass
# Session automatically closed
```

---

### WebScraperError Exception

Custom exception class for WebScraper-specific errors.

```python
try:
    scraper.fetch_url('invalid-url')
except WebScraperError as e:
    print(f"Scraper error: {e}")
```

## ⚙️ Configuration

### Timeout Settings

Control how long to wait for responses:

```python
# Short timeout for fast responses
scraper = WebScraper(timeout=5)

# Longer timeout for slow servers
scraper = WebScraper(timeout=60)
```

### Custom Headers

Add custom HTTP headers for authentication, language preferences, etc.:

```python
headers = {
    'User-Agent': 'MyBot/1.0',
    'Accept-Language': 'en-US',
    'Authorization': 'Bearer TOKEN',
    'Accept': 'application/json'
}

scraper = WebScraper(custom_headers=headers)
```

### Retry Configuration

Adjust the number of retry attempts:

```python
with WebScraper() as scraper:
    # Try up to 5 times
    response = scraper.fetch_url('https://example.com', retries=5)
```

### Parser Selection

Choose the HTML parser based on your needs:

```python
# Default parser (included with Python)
soup = scraper.parse_html(html, parser='html.parser')

# lxml (fastest, requires installation)
soup = scraper.parse_html(html, parser='lxml')

# html5lib (most lenient, requires installation)
soup = scraper.parse_html(html, parser='html5lib')
```

### Logging Configuration

The scraper uses Python's built-in logging. Configure it to control output:

```python
import logging

# Show debug messages
logging.basicConfig(level=logging.DEBUG)

# Only show warnings and errors
logging.basicConfig(level=logging.WARNING)

# Disable logging
logging.basicConfig(level=logging.CRITICAL)
```

## 🛡️ Error Handling

### Exception Hierarchy

```
Exception
└── WebScraperError
    ├── Invalid URL format
    ├── Timeout errors
    ├── HTTP errors
    ├── Connection errors
    └── Parsing errors
```

### Common Error Scenarios

#### 1. Invalid URL

```python
try:
    scraper.fetch_url('not-a-valid-url')
except WebScraperError as e:
    print(f"Invalid URL: {e}")
```

#### 2. Timeout Errors

```python
try:
    scraper.fetch_url('https://very-slow-site.com', retries=3)
except WebScraperError as e:
    print(f"Request timed out: {e}")
```

#### 3. HTTP Errors (404, 500, etc.)

```python
try:
    response = scraper.fetch_url('https://example.com/nonexistent')
except WebScraperError as e:
    print(f"HTTP error: {e}")
```

#### 4. Connection Errors

```python
try:
    scraper.fetch_url('https://unreachable-site.com')
except WebScraperError as e:
    print(f"Connection failed: {e}")
```

### Graceful Error Handling with `scrape()`

The `scrape()` method returns error information instead of raising exceptions:

```python
result = scraper.scrape('https://example.com')

if 'error' in result:
    print(f"Scraping failed: {result['error']}")
    print(f"Status: {result['status']}")
else:
    # Process successful result
    print(f"Title: {result['title']}")
```

## 💡 Best Practices

### 1. Always Use Context Managers

Use `with` statements to ensure proper resource cleanup:

```python
# Good ✓
with WebScraper() as scraper:
    result = scraper.scrape('https://example.com')

# Avoid ✗
scraper = WebScraper()
result = scraper.scrape('https://example.com')
# Easy to forget scraper.close()
```

### 2. Respect Robots.txt

Always check and respect a website's `robots.txt` file:

```python
# Check https://example.com/robots.txt before scraping
```

### 3. Add Delays Between Requests

Avoid overloading servers:

```python
import time

with WebScraper() as scraper:
    for url in urls:
        result = scraper.scrape(url)
        time.sleep(1)  # Wait 1 second between requests
```

### 4. Use Specific CSS Selectors

More specific selectors are more reliable:

```python
# Good ✓
selectors = {
    'article_title': 'article.post h1.title',
    'author': 'div.author-info span.name'
}

# Less reliable ✗
selectors = {
    'title': 'h1',
    'author': 'span'
}
```

### 5. Handle Rate Limiting

Implement exponential backoff for rate-limited APIs:

```python
import time

def scrape_with_backoff(scraper, url, max_retries=5):
    for attempt in range(max_retries):
        result = scraper.scrape(url)
        if 'error' not in result:
            return result
        
        wait_time = 2 ** attempt  # Exponential backoff
        print(f"Retry in {wait_time} seconds...")
        time.sleep(wait_time)
    
    return None
```

### 6. Validate Extracted Data

Always check if data was successfully extracted:

```python
data = scraper.extract_text(soup, 'h1')

if data:
    print(f"Found heading: {data[0]}")
else:
    print("No heading found")
```

### 7. Use Appropriate Timeouts

Set timeouts based on expected response times:

```python
# Fast API
scraper = WebScraper(timeout=5)

# Large content or slow server
scraper = WebScraper(timeout=30)
```

### 8. Log Scraping Activities

Keep logs for debugging and monitoring:

```python
import logging

logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### 9. Cache Results

Avoid re-scraping the same content:

```python
cache = {}

def cached_scrape(scraper, url):
    if url in cache:
        return cache[url]
    
    result = scraper.scrape(url)
    cache[url] = result
    return result
```

### 10. Be a Good Web Citizen

- Identify your bot with a descriptive User-Agent
- Add contact information in headers
- Respect rate limits
- Don't scrape personal or sensitive data
- Follow website terms of service

```python
headers = {
    'User-Agent': 'MyBot/1.0 (+https://mysite.com/bot; contact@mysite.com)'
}
scraper = WebScraper(custom_headers=headers)
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Write or update tests
5. Ensure all tests pass
6. Commit your changes: `git commit -am 'Add new feature'`
7. Push to the branch: `git push origin feature/my-feature`
8. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints where applicable
- Add docstrings to all functions and classes
- Keep functions focused and concise

### Testing

Run tests before submitting:

```bash
python -m pytest tests/
```

### Reporting Issues

When reporting bugs, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Relevant code snippets or logs

## 📄 License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Support

If you have questions or need help:

- Check the [API Reference](#api-reference) section
- Review the [Usage Examples](#usage-examples)
- Open an issue on GitHub

---

**Happy Scraping! 🎉**

Remember to always scrape responsibly and ethically.
