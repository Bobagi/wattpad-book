import pdfkit

class PDFConverter:
    def __init__(self, wkhtmltopdf_path=None):
        if wkhtmltopdf_path:
            self.config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        else:
            self.config = None

    def convert_html_to_pdf(self, html_content, output_file):
        try:
            pdfkit.from_string(html_content, output_file, configuration=self.config)
            print(f"PDF saved to: {output_file}")
        except Exception as e:
            print(f"Error converting to PDF: {e}")

    def convert_text_to_pdf(self, text_content, output_file):
        # Updated HTML with meta charset and a CSS style specifying a Unicode font.
        html_content = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: 'DejaVu Sans', sans-serif;
                    white-space: pre-wrap;
                }}
            </style>
        </head>
        <body>
            {text_content}
        </body>
        </html>
        """
        self.convert_html_to_pdf(html_content, output_file)
