import requests
from bs4 import BeautifulSoup

class WattpadScraper:
    def __init__(self, url):
        self.url = url
        self.html_content = None
        self.soup = None

    def fetch_page(self):
        """Fetches the HTML page of the book on Wattpad using a User-Agent to simulate a browser."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        }
        try:
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
            self.html_content = response.text
            return True
        except requests.RequestException as e:
            print(f"Error accessing the page: {e}")
            return False

    def parse_content(self):
        """
        Parses the HTML and extracts the book content.
        Adjust the tag selection according to the page layout.
        """
        if not self.html_content:
            if not self.fetch_page():
                return None
        self.soup = BeautifulSoup(self.html_content, 'html.parser')
        paragraphs = self.soup.find_all('p')
        content = "\n\n".join([p.get_text(strip=True) for p in paragraphs])
        return content

    def get_book_content(self):
        """Returns the extracted book content."""
        return self.parse_content()