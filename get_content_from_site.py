def get_me_content(single_url):
    import requests
    from bs4 import BeautifulSoup

    response = requests.get(single_url, timeout=10)
    response.raise_for_status()  # Raise an error for bad responses

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    texts = soup.find_all(['div'])
    page_text = "\n".join([text.get_text() for text in texts])
    return page_text

