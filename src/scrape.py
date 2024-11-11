"""
- Based on name of the company get the latest information about the company.
"""

# import asyncio
# from crawl4ai import AsyncWebCrawler

# async def main(URL):
#     async with AsyncWebCrawler(verbose=True) as crawler:
#         # Run the crawler on a specified URL
#         result = await crawler.arun(url=URL)
#         # Print the extracted content in Markdown format
#         print(result.markdown)

# # Execute the async main function
# URL = "https://help.zluri.com/"
# asyncio.run(main(URL))


# system_context = """
# """

from vector_db import qdrant_client
import uuid

collection_name = "zluri"
def base_line_1():
    import requests
    from bs4 import BeautifulSoup

    def scrape_text_from_urls(urls):
        extracted_texts = []

        for url in urls:
            try:
                # Attempt to fetch the URL with SSL verification
                response = requests.get(url, timeout=10)
                response.raise_for_status()  # Raise an error for bad responses

            except requests.exceptions.SSLError as ssl_err:
                print(f"SSL Error while fetching {url}: {ssl_err}")
                # Optionally, try fetching with verify=False
                try:
                    print("Retrying without SSL verification...")
                    response = requests.get(url, timeout=10, verify=False)
                    response.raise_for_status()
                except Exception as e:
                    print(f"Failed to fetch {url} after retry: {e}")
                    continue  # Skip this URL if it fails again

            except requests.exceptions.RequestException as e:
                print(f"Request failed for {url}: {e}")
                continue  # Skip this URL if it fails

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract text from desired tags (e.g., paragraphs)
            texts = soup.find_all(['p', 'span', 'li', 'div'])
            page_text = "\n".join([text.get_text() for text in texts])
            
            extracted_texts.append(page_text)

        return extracted_texts

    # Example usage
    urls = [
        "https://help.zluri.com/",
    ]

    extracted_texts = scrape_text_from_urls(urls)

    # Print the extracted texts
    for i, text in enumerate(extracted_texts):
        print(f"Text from URL {urls[i]}:\n{text[:]}...\n")  # Print first 500 characters of each scraped text


import requests
from bs4 import BeautifulSoup
import time

def scrape_text_and_links(url, visited=None, depth=1, max_depth=2):
    if visited is None:
        visited = set()  # Track visited URLs to avoid loops

    if depth > max_depth:
        return  # Stop recursion if maximum depth is reached

    try:
        
        response = requests.get(url, timeout=10)
        response.raise_for_status() 

        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            # Make sure to handle relative URLs
            full_url = requests.compat.urljoin(url, href)

            # Check if the link has already been visited
            if full_url not in visited:
                visited.add(full_url)  # Mark this URL as visited
                # Recursively scrape the found link
                content = get_me_content(full_url)
                content = content.replace("  ","")
                content = content.split()
                content = " ".join(content)
                print(f"Text from {full_url}:\n{content[:100]}...\n")  # Print first 500 characters of each scraped text
                payload = {
                    "uid":str(uuid.uuid4()),
                    "content":content,
                    "url":full_url
                }
                rep = qdrant_client.insert_new_data(collection_name, payload)
                print(rep)
                time.sleep(1)  # Optional: be polite and wait a bit before the next request
                scrape_text_and_links(full_url, visited, depth + 1, max_depth)

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")

# Example usage
start_url = "https://help.zluri.com/docs/" # "https://www.zluri.com/"

# def get_me_links(start_url):
#     ans = []

def get_me_content(single_url):
    response = requests.get(single_url, timeout=10)
    response.raise_for_status()  # Raise an error for bad responses

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    texts = soup.find_all(['p', 'span', 'li', 'div'])
    page_text = "\n".join([text.get_text() for text in texts])
    return page_text

# scrape_text_and_links(start_url, max_depth=2)  # Set max_depth as needed
# qdrant_client.get_classification_result()
# print(qdrant_client.get_specific_data(collection_name, ticket_id))



"""
To-Do:

- Make your information retrieval reobust:
    - Pre-process the data before storing it into vectorDB.
        - Remove repeatative contents.
    - Chunk data instead of feeding entire set
    - If content is very huge summarize it and then store it.
"""