import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

def get_unique_sublinks(url, max_depth=2):
    visited = set()
    result = []
    queue = deque([(url, 0)])  # (link, depth)

    while queue:
        current_url, depth = queue.popleft()
        
        if current_url in visited or depth > max_depth:
            continue
        
        visited.add(current_url)

        try:
            response = requests.get(current_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            base_url = "{0.scheme}://{0.netloc}".format(urlparse(url))
            
            for link in soup.find_all("a", href=True):
                href = link['href']
                full_url = urljoin(base_url, href)
                
                # Only follow unique links within the same domain
                if urlparse(full_url).netloc == urlparse(url).netloc:
                    if full_url not in visited and full_url not in result \
                            and "login?redirect" not in full_url \
                            and "https://help.zluri.com#" not in full_url \
                            and "https://help.zluri.com/docs/" in full_url :
                        queue.append((full_url, depth + 1))
                        result.append(full_url)
                        print(full_url)

        except requests.RequestException as e:
            print(f"Could not retrieve {current_url}: {e}")

    return result

# Use the function to get unique sublinks up to depth 2
if __name__ == "__main__":
    url = "https://help.zluri.com/docs"
    file_name = "sublinks.txt"

    # Get unique sublinks and save them to a text file
    unique_sublinks = get_unique_sublinks(url, max_depth=2)

    with open(file_name, "w") as file:
        for link in unique_sublinks:
            file.write(link + "\n")