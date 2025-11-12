# Python Web Scraper

A robust and flexible Python web scraping library built with `requests` and `BeautifulSoup4`. This library provides a simple yet powerful interface for extracting data from websites with built-in error handling, retry logic, and exponential backoff.

## Features

- 🚀 Simple and intuitive API
- 🔄 Automatic retry logic with exponential backoff
- 🛡️ Comprehensive error handling
- 🎨 CSS selector-based data extraction
- ⚙️ Customizable headers and timeouts
- 📦 Session management for efficient requests
- 🔍 BeautifulSoup4 integration for powerful HTML parsing

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)
- [Best Practices](#best-practices)
- [Error Handling](#error-handling)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install requests beautifulsoup4
```

### Install from Source

```bash
git clone https://github.com/yourusername/python-web-scraper.git
cd python-web-scraper
pip install -r requirements.txt
```

### Requirements File

Create a `requirements.txt` file with:

```
requests>=2.28.0
beautifulsoup4>=4.11.0
lxml>=4.9.0
```

## Quick Start

```python
from web_scraper import WebScraper

# Initialize the scraper
scraper = WebScraper(timeout=10)

# Define CSS selectors for data extraction
selectors = {
    'title': 'h1.page-title',
    'description': 'p.description',
    'price': 'span.price'
}

# Scrape data from a URL
try:
    data = scraper.scrape('https://example.com', selectors)
    print(data)
finally:
    scraper.close()
```

## API Documentation

### WebScraper Class

The main class for web scraping operations.

#### `__init__(timeout=30, headers=None)`

Initialize a new WebScraper instance.

**Parameters:**

- `timeout` (int, optional): Request timeout in seconds. Default: 30
- `headers` (dict, optional): Custom HTTP headers. Default: Standard browser headers

**Example:**

```python
scraper = WebScraper(
    timeout=15,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept-Language': 'en-US,en;q=0.9'
    }
)
```

#### `fetch_url(url, retries=3)`

Fetch HTML content from a URL with retry logic.

**Parameters:**

- `url` (str): The URL to fetch
- `retries` (int, optional): Number of retry attempts. Default: 3

**Returns:**

- `str`: HTML content of the page
- `None`: If all retry attempts fail

**Raises:**

- `requests.exceptions.RequestException`: For network-related errors

**Example:**

```python
html = scraper.fetch_url('https://example.com', retries=5)
if html:
    print("Successfully fetched content")
```

#### `parse_html(html_content)`

Parse HTML content using BeautifulSoup4.

**Parameters:**

- `html_content` (str): Raw HTML content to parse

**Returns:**

- `BeautifulSoup`: Parsed HTML object
- `None`: If parsing fails

**Example:**

```python
html = scraper.fetch_url('https://example.com')
soup = scraper.parse_html(html)
if soup:
    title = soup.find('title').text
    print(f"Page title: {title}")
```

#### `extract_data(soup, selectors)`

Extract data from parsed HTML using CSS selectors.

**Parameters:**

- `soup` (BeautifulSoup): Parsed HTML object
- `selectors` (dict): Dictionary mapping field names to CSS selectors

**Returns:**

- `dict`: Extracted data with keys matching selector names

**Example:**

```python
selectors = {
    'heading': 'h1',
    'paragraphs': 'p',
    'links': 'a[href]'
}
data = scraper.extract_data(soup, selectors)
```

#### `scrape(url, selectors, retries=3)`

Complete scraping workflow: fetch, parse, and extract data.

**Parameters:**

- `url` (str): The URL to scrape
- `selectors` (dict): CSS selectors for data extraction
- `retries` (int, optional): Number of retry attempts. Default: 3

**Returns:**

- `dict`: Extracted data
- `None`: If scraping fails

**Example:**

```python
data = scraper.scrape(
    'https://example.com/products',
    {
        'product_name': 'h2.product-title',
        'price': 'span.price-value',
        'rating': 'div.rating'
    },
    retries=5
)
```

#### `close()`

Close the requests session and clean up resources.

**Example:**

```python
scraper.close()
```

## Usage Examples

### Example 1: Basic Web Scraping

```python
from web_scraper import WebScraper

# Create scraper instance
scraper = WebScraper()

# Scrape a simple webpage
url = 'https://example.com'
selectors = {
    'title': 'h1',
    'content': 'div.content p'
}

try:
    data = scraper.scrape(url, selectors)
    if data:
        print(f"Title: {data['title']}")
        print(f"Content: {data['content']}")
except Exception as e:
    print(f"Error: {e}")
finally:
    scraper.close()
```

### Example 2: Scraping Multiple Pages

```python
from web_scraper import WebScraper

urls = [
    'https://example.com/page1',
    'https://example.com/page2',
    'https://example.com/page3'
]

selectors = {
    'title': 'h1.page-title',
    'author': 'span.author-name',
    'date': 'time.publish-date'
}

scraper = WebScraper(timeout=20)
results = []

try:
    for url in urls:
        print(f"Scraping {url}...")
        data = scraper.scrape(url, selectors)
        if data:
            results.append(data)

    print(f"Successfully scraped {len(results)} pages")
finally:
    scraper.close()
```

### Example 3: Custom Headers and User Agent

```python
from web_scraper import WebScraper

custom_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

scraper = WebScraper(timeout=15, headers=custom_headers)

try:
    data = scraper.scrape(
        'https://example.com',
        {'content': 'div.main-content'}
    )
    print(data)
finally:
    scraper.close()
```

### Example 4: Advanced Data Extraction

```python
from web_scraper import WebScraper

scraper = WebScraper()

# Complex selectors for e-commerce site
selectors = {
    'product_name': 'h1[itemprop="name"]',
    'price': 'span.price-current',
    'original_price': 'span.price-original',
    'rating': 'div.rating span.rating-value',
    'reviews_count': 'span.reviews-count',
    'availability': 'div.stock-status',
    'description': 'div#product-description p',
    'images': 'img.product-image',
    'specifications': 'table.specs tr'
}

try:
    url = 'https://example-shop.com/product/12345'
    product_data = scraper.scrape(url, selectors, retries=5)

    if product_data:
        print("Product Information:")
        print("-" * 50)
        for key, value in product_data.items():
            print(f"{key}: {value}")
finally:
    scraper.close()
```

### Example 5: Error Handling and Logging

```python
from web_scraper import WebScraper
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

scraper = WebScraper(timeout=10)

urls = [
    'https://example.com/valid-page',
    'https://example.com/404-page',
    'https://invalid-domain.xyz'
]

selectors = {'title': 'h1'}

try:
    for url in urls:
        logger.info(f"Attempting to scrape: {url}")

        try:
            data = scraper.scrape(url, selectors, retries=3)
            if data:
                logger.info(f"Success: {data}")
            else:
                logger.warning(f"No data extracted from {url}")
        except Exception as e:
            logger.error(f"Failed to scrape {url}: {str(e)}")
            continue
finally:
    scraper.close()
    logger.info("Scraper closed")
```

### Example 6: Context Manager Pattern

```python
from web_scraper import WebScraper
from contextlib import closing

# Using closing context manager
with closing(WebScraper(timeout=15)) as scraper:
    data = scraper.scrape(
        'https://example.com',
        {'title': 'h1', 'content': 'article p'}
    )
    print(data)
# Session automatically closed
```

### Example 7: Extracting Lists and Multiple Elements

```python
from web_scraper import WebScraper

scraper = WebScraper()

# For extracting all matching elements
html = scraper.fetch_url('https://news-site.com')
soup = scraper.parse_html(html)

if soup:
    # Extract all article titles
    articles = soup.select('article.news-item')

    all_articles = []
    for article in articles:
        article_data = {
            'title': article.select_one('h2.title').text.strip(),
            'summary': article.select_one('p.summary').text.strip(),
            'author': article.select_one('span.author').text.strip(),
            'date': article.select_one('time').get('datetime')
        }
        all_articles.append(article_data)

    print(f"Found {len(all_articles)} articles")
    for article in all_articles:
        print(f"- {article['title']} by {article['author']}")

scraper.close()
```

### Example 8: Handling Dynamic Content

```python
from web_scraper import WebScraper
import time

scraper = WebScraper(
    timeout=30,
    headers={'User-Agent': 'Mozilla/5.0 (compatible; Bot/1.0)'}
)

try:
    # Fetch page
    html = scraper.fetch_url('https://example.com/dynamic-content')

    if html:
        # Some sites require parsing delay
        time.sleep(2)

        soup = scraper.parse_html(html)

        # Extract data with fallback selectors
        selectors = {
            'title': 'h1.main-title, h1.title, h1',
            'description': 'div.description, p.desc, div.content p:first-child'
        }

        data = scraper.extract_data(soup, selectors)
        print(data)
finally:
    scraper.close()
```

## Best Practices

### 1. Always Close Sessions

Always call `close()` to free up resources:

```python
scraper = WebScraper()
try:
    # Your scraping code
    data = scraper.scrape(url, selectors)
finally:
    scraper.close()
```

### 2. Respect Robots.txt

Check the website's `robots.txt` file before scraping:

```python
from urllib.robotparser import RobotFileParser

def can_scrape(url):
    rp = RobotFileParser()
    rp.set_url(f"{url}/robots.txt")
    rp.read()
    return rp.can_fetch("*", url)

if can_scrape("https://example.com"):
    scraper = WebScraper()
    # Proceed with scraping
```

### 3. Implement Rate Limiting

Add delays between requests to avoid overwhelming servers:

```python
import time

scraper = WebScraper()
urls = ['url1', 'url2', 'url3']

for url in urls:
    data = scraper.scrape(url, selectors)
    time.sleep(2)  # 2-second delay between requests
```

### 4. Use Appropriate Headers

Identify your scraper properly:

```python
headers = {
    'User-Agent': 'MyBot/1.0 (+https://mywebsite.com/bot)',
    'From': 'your-email@example.com'
}
scraper = WebScraper(headers=headers)
```

### 5. Handle Errors Gracefully

Implement comprehensive error handling:

```python
try:
    data = scraper.scrape(url, selectors, retries=3)
    if data:
        process_data(data)
    else:
        log_failure(url)
except Exception as e:
    handle_error(e)
finally:
    scraper.close()
```

### 6. Validate Extracted Data

Always validate scraped data:

```python
data = scraper.scrape(url, selectors)
if data and data.get('title') and data.get('content'):
    # Data is valid
    save_data(data)
else:
    # Invalid or incomplete data
    log_error(f"Invalid data from {url}")
```

### 7. Use Specific Selectors

Be as specific as possible with CSS selectors:

```python
# Good: Specific selector
selectors = {'price': 'div.product-info span.price-value'}

# Less reliable: Generic selector
selectors = {'price': 'span'}
```

### 8. Monitor Performance

Track scraping performance:

```python
import time

start_time = time.time()
data = scraper.scrape(url, selectors)
end_time = time.time()

print(f"Scraping took {end_time - start_time:.2f} seconds")
```

## Error Handling

The scraper implements robust error handling with exponential backoff:

### Automatic Retry Logic

```python
# Automatically retries on failure with exponential backoff
data = scraper.scrape(url, selectors, retries=5)
```

### Common Exceptions

```python
from requests.exceptions import (
    Timeout,
    ConnectionError,
    HTTPError,
    RequestException
)

try:
    data = scraper.scrape(url, selectors)
except Timeout:
    print("Request timed out")
except ConnectionError:
    print("Connection failed")
except HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")
except RequestException as e:
    print(f"Request error: {e}")
```

### Exponential Backoff

The scraper automatically implements exponential backoff:

- 1st retry: 1 second delay
- 2nd retry: 2 seconds delay
- 3rd retry: 4 seconds delay
- 4th retry: 8 seconds delay
- And so on...

## Troubleshooting

### Issue: Connection Timeouts

**Problem:** Requests are timing out frequently.

**Solution:**
```python
# Increase timeout value
scraper = WebScraper(timeout=60)
```

### Issue: 403 Forbidden Errors

**Problem:** Website is blocking requests.

**Solution:**
```python
# Use realistic browser headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com/'
}
scraper = WebScraper(headers=headers)
```

### Issue: Empty Data Extraction

**Problem:** Selectors return no data.

**Solution:**
```python
# Debug by examining the HTML structure
html = scraper.fetch_url(url)
soup = scraper.parse_html(html)
print(soup.prettify())  # Inspect HTML structure

# Test different selectors
test_selectors = ['h1', 'h1.title', 'div.header h1']
for selector in test_selectors:
    result = soup.select_one(selector)
    print(f"{selector}: {result}")
```

### Issue: Memory Leaks

**Problem:** Memory usage grows over time.

**Solution:**
```python
# Always close sessions
scraper = WebScraper()
try:
    for url in large_url_list:
        data = scraper.scrape(url, selectors)
        process_data(data)
finally:
    scraper.close()  # Essential for cleanup
```

### Issue: Rate Limiting or IP Blocking

**Problem:** Getting blocked after multiple requests.

**Solution:**
```python
import time
import random

scraper = WebScraper()
for url in urls:
    data = scraper.scrape(url, selectors)
    # Random delay between 2-5 seconds
    time.sleep(random.uniform(2, 5))
```

### Issue: JavaScript-Rendered Content

**Problem:** Content not available in HTML source.

**Solution:**

This scraper works with static HTML. For JavaScript-rendered content, consider using Selenium or Playwright:

```python
# This library doesn't handle JavaScript rendering
# Consider using selenium for dynamic content
from selenium import webdriver

driver = webdriver.Chrome()
driver.get(url)
html = driver.page_source
# Then use parse_html() on this content
```

### Issue: SSL Certificate Errors

**Problem:** SSL verification failures.

**Solution:**
```python
# Note: Only for development/testing
import requests
requests.packages.urllib3.disable_warnings()

# For production, fix SSL certificates properly
```

### Issue: Encoding Problems

**Problem:** Special characters not displaying correctly.

**Solution:**
```python
# The scraper handles encoding automatically
# If issues persist, check the response encoding
html = scraper.fetch_url(url)
soup = scraper.parse_html(html)

# Access original encoding
# response.encoding in the actual implementation
```

## Contributing

We welcome contributions! Here's how you can help:

### Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/python-web-scraper.git
   ```
3. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Check code style
flake8 web_scraper.py

# Format code
black web_scraper.py
```

### Contribution Guidelines

- Write clear, documented code
- Add tests for new features
- Follow PEP 8 style guidelines
- Update documentation as needed
- Write meaningful commit messages

### Pull Request Process

1. Update the README.md with details of changes
2. Update the CHANGELOG.md
3. Ensure all tests pass
4. Request review from maintainers
5. Address review comments

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

### Reporting Issues

When reporting bugs, include:

- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages and stack traces

### Feature Requests

For feature requests, provide:

- Clear description of the feature
- Use cases and benefits
- Potential implementation approach
- Any relevant examples

## License

MIT License

Copyright (c) 2024 [Your Name]

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

## Acknowledgments

- Built with [Requests](https://requests.readthedocs.io/)
- HTML parsing by [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
- Inspired by the web scraping community

## Support

- 📧 Email: support@example.com
- 💬 Discord: [Join our server](https://discord.gg/example)
- 📝 Issues: [GitHub Issues](https://github.com/yourusername/python-web-scraper/issues)
- 📖 Documentation: [Full Documentation](https://docs.example.com)

## Changelog

### Version 1.0.0 (2024-01-01)

- Initial release
- Basic scraping functionality
- Retry logic with exponential backoff
- CSS selector support
- Session management

---

**Happy Scraping! 🚀**

Remember to always scrape responsibly and respect website terms of service and robots.txt files.
