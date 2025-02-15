import requests
from bs4 import BeautifulSoup
import time
import re

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
        Forces UTF-8 decoding to fix character issues.
        Returns None if the request fails or returns a 403.
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            # Force decode using UTF-8
            html = response.content.decode('utf-8', errors='replace')
            return html
        except requests.HTTPError as e:
            if response.status_code == 403:
                print(f"403 Forbidden for url: {url}")
            else:
                print(f"HTTP Error accessing page: {e}")
            return None
        except requests.RequestException as e:
            print(f"Error accessing page: {e}")
            return None

    def remove_header_block(self, text):
        """
        Removes the header block from the text.
        If "VOCÊ ESTÁ LENDO" is found, removes all text from the beginning 
        up until after the last line that starts with "#". Otherwise, if the initial
        lines contain "#", they are skipped.
        """
        # Check for the phrase "VOCÊ ESTÁ LENDO" (ignoring case)
        header_start = re.search(r'VOC[ÊE]\s+EST[ÁA]\s+LENDO', text, flags=re.IGNORECASE)
        if header_start:
            # Find all lines that start with "#" using multiline matching
            matches = list(re.finditer(r'^\s*#.*$', text, flags=re.MULTILINE))
            if matches:
                last_match = matches[-1]
                return text[last_match.end():].strip()
        else:
            # If not found, remove initial lines that contain "#"
            lines = text.splitlines()
            new_lines = []
            header_removed = False
            for line in lines:
                if not header_removed and '#' in line:
                    continue
                else:
                    header_removed = True
                    new_lines.append(line)
            return "\n".join(new_lines).strip()
        return text

    def extract_content(self, html):
        """
        Parses the HTML and extracts text from <p> tags.
        After extraction, applies remove_header_block to eliminate the repeated header.
        Adjust the tag selection if necessary.
        """
        soup = BeautifulSoup(html, 'html.parser')
        paragraphs = soup.find_all('p')
        content = "\n\n".join([p.get_text(strip=True) for p in paragraphs])
        content = self.remove_header_block(content)
        return content

    def get_book_content(self):
        """
        Retrieves the complete chapter content by fetching the initial page
        and subsequent pages (by appending '/page/{number}' to the URL) until no new
        content is found or a 403 error occurs.
        
        It stops if:
          - The fetched page returns no content.
          - The fetched page content is identical to the previous page (indicating redirection).
          - A 403 error is encountered.
          
        Every 30 pages, it pauses for 10 seconds to avoid timeouts.
        """
        pages_content = []
        
        # Fetch the first page
        first_page_html = self.fetch_page_content(self.url)
        if not first_page_html:
            return None
        content = self.extract_content(first_page_html)
        pages_content.append(content)
        previous_page_content = content
        
        # Fetch subsequent pages
        page_number = 2
        while True:
            if page_number % 30 == 0:
                print("Pausing for 10 seconds to avoid timeout...")
                time.sleep(10)
            
            next_page_url = f"{self.url}/page/{page_number}"
            page_html = self.fetch_page_content(next_page_url)
            if not page_html:
                break  # Stop if the page cannot be fetched (including a 403 response)
            
            page_content = self.extract_content(page_html)
            # Stop if the content is empty or identical to the previous page (likely a redirection)
            if not page_content.strip() or page_content.strip() == previous_page_content.strip():
                break
            
            pages_content.append(page_content)
            previous_page_content = page_content
            page_number += 1
        
        return "\n\n".join(pages_content)
