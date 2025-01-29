from xhtml2pdf import pisa

# HTML content
html_content = """
<html>
    <head><title>Sample PDF</title></head>
    <body>
        <h1>Hello, this is a sample PDF!</h1>
        <p>This is a simple paragraph in the PDF.</p>
    </body>
</html>
"""

# Function to save PDF
def save_pdf(html_content, output_filename):
    with open(output_filename, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
        if pisa_status.err:
            print("Error occurred while generating the PDF")
        else:
            print(f"PDF saved successfully as {output_filename}")

# Save the PDF
save_pdf(html_content, "output2.pdf")
