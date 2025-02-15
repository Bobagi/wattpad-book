import sys
from src.wattpad_scraper import WattpadScraper
from src.pdf_converter import PDFConverter

def main():
    # Check if a URL is provided as a command-line argument; otherwise, prompt the user.
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter the URL of the book on Wattpad: ")

    # Instantiate the scraper to extract content
    scraper = WattpadScraper(url)
    content = scraper.get_book_content()
    
    if content:
        # Specify the path to wkhtmltopdf (ensure the correct executable path and extension)
        wkhtmltopdf_path = r"D:\wkhtmltox\bin\wkhtmltopdf.exe"
        
        # Instantiate the PDF converter, passing the wkhtmltopdf path
        converter = PDFConverter(wkhtmltopdf_path)
        output_file = "book.pdf"
        
        # Convert the text to PDF
        converter.convert_text_to_pdf(content, output_file)
    else:
        print("Failed to extract the book content.")

if __name__ == '__main__':
    main()
