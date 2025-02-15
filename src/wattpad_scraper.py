import requests
from bs4 import BeautifulSoup

class WattpadScraper:
    def __init__(self, url):
        self.url = url
        self.html_content = None
        self.soup = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        }

    def fetch_page_content(self, url):
        """
        Fetches the HTML content of the given URL using custom headers.
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error accessing page: {e}")
            return None

    def extract_content(self, html):
        """
        Parses the HTML and extracts text from <p> tags.
        Adjust the tag selection if necessary.
        """
        soup = BeautifulSoup(html, 'html.parser')
        paragraphs = soup.find_all('p')
        content = "\n\n".join([p.get_text(strip=True) for p in paragraphs])
        return content

    def get_book_content(self):
        """
        Retrieves the complete chapter content by fetching the initial page
        and subsequent pages (appending '/page/{number}' to the URL) until no more
        content is found.
        """
        pages_content = []
        
        # Fetch the first page
        first_page_html = self.fetch_page_content(self.url)
        if not first_page_html:
            return None
        content = self.extract_content(first_page_html)
        pages_content.append(content)
        
        # Fetch subsequent pages
        page_number = 2
        while True:
            next_page_url = f"{self.url}/page/{page_number}"
            page_html = self.fetch_page_content(next_page_url)
            if not page_html:
                break  # Break the loop if the page cannot be fetched
            page_content = self.extract_content(page_html)
            # If the extracted content is empty, assume there are no more pages
            if not page_content.strip():
                break
            pages_content.append(page_content)
            page_number += 1
        
        return "\n\n".join(pages_content)
