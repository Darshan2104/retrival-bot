import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import logging

class WebpageScraper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        
    def get_webpage_content(self, url: str) -> Optional[Dict[str, str]]:
        """
        Scrapes the header and main content from a given webpage URL.
        
        Args:
            url (str): The URL of the webpage to scrape
            
        Returns:
            Optional[Dict[str, str]]: Dictionary containing header and main content,
                                    or None if scraping fails
        """
        try:
            # Send GET request to the URL
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract header (try different header tags)
            header = None
            for header_tag in ['h1', 'header']:
                header_element = soup.find(header_tag)
                if header_element:
                    header = header_element.get_text(strip=True)
                    break
            
            # Extract main content
            content = None
            content_div = soup.find('div', id='content-container')
            if content_div:
                content = content_div.get_text()
            
            # Check if we found both header and content
            if not header and not content:
                self.logger.warning(f"No header or content found for URL: {url}")
                return None
                
            return {
                'header': header,
                'content': content
            }
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching URL {url}: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Error processing webpage {url}: {str(e)}")
            return None

# Example usage
def main():
    import uuid
    scraper = WebpageScraper()
    data_to_load = []
    
    file_path = 'sublinks.txt'

    with open(file_path, 'r') as file:
        file_contents = file.read()


    urls = file_contents.split('\n')
    # Example URLs to scrape
    # urls = [
    #     "https://help.zluri.com/docs/faq-user-management"

    #     # Add more URLs as needed
    # ]
    
    for url in urls:
        payload = {
            "uid": str(uuid.uuid4())
        }
        payload["url"] = url
        result = scraper.get_webpage_content(url)
        if result:
            print(f"\nResults for {url}:")
            print("Header:", result['header'])
            payload["header"] = result['header']
            print("\nContent:", result['content'])
            payload["content"] = result['content']
            data_to_load.append(payload)
        else:
            print(f"\nFailed to scrape {url}")

    import json
    results = {"data":data_to_load}
    with open('result.json', 'w') as fp:
        json.dump(results, fp)
if __name__ == "__main__":
    main()