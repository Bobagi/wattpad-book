import pdfkit

class PDFConverter:
    def __init__(self, wkhtmltopdf_path=None):
        """
        Initializes the PDF conversion.
        If the path to wkhtmltopdf is provided, creates a custom configuration.
        """
        if wkhtmltopdf_path:
            self.config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        else:
            self.config = None

    def convert_html_to_pdf(self, html_content, output_file):
        """Converts an HTML string into a PDF file."""
        try:
            pdfkit.from_string(html_content, output_file, configuration=self.config)
            print(f"PDF saved at: {output_file}")
        except Exception as e:
            print(f"Error converting to PDF: {e}")

    def convert_text_to_pdf(self, text_content, output_file):
        """
        Converts plain text to PDF.
        The method wraps the text in basic HTML so that pdfkit can process it.
        """
        html_content = f"<html><body><pre>{text_content}</pre></body></html>"
        self.convert_html_to_pdf(html_content, output_file)