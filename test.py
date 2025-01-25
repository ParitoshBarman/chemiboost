from xhtml2pdf import pisa

html = """
    <html>
    <head>
        <title>Purchase Invoice</title>
        <style>
            body { font-family: Arial, sans-serif; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            th, td { border: 1px solid black; padding: 4px; text-align: left; }
            .invoice-header { margin-bottom: 15px; }
            .invoice-buttons { margin-top: 20px; }
        </style>
    </head>
    <body>
        <h2>Purchase Invoice</h2>
        <div class="invoice-header">
            <p><strong>Invoice ID:</strong> 18</p>
            <p><strong>Supplier:</strong> Joy Agency</p>
            <p><strong>Contact:</strong> 9832444471</p>
            <p><strong>Purchase Date:</strong> 2025-01-23</p>
            <p><strong>Total Amount:</strong> ₹1068.90</p>
            <p><strong>Total GST:</strong> ₹192.40</p>
            <p><strong>Total with GST:</strong> ₹1261.30</p>
        </div>

        <table>
            <thead>
                <tr>
                    
                    <th>Expiry Date</th>
                    <th>MRP</th>
                    <th>Rate</th>
                    <th>Qty</th>
                    <th>Total</th>
                    <th>Cgst</th>
                    <th>Sgst</th>
                    <th>GST amount</th>
                    <th>Total With GST</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    
                    <td>2025-01-24</td><td>23.00</td><td>19.30</td><td>23</td>
                    <td>443.90</td><td>9.00</td><td>9.00</td><td>79.90</td><td>523.80</td>
                </tr>
                <tr>
                    
                    <td>2025-01-25</td><td>23.00</td><td>125.00</td><td>5</td>
                    <td>625.00</td><td>9.00</td><td>9.00</td><td>112.50</td><td>737.50</td>
                </tr>
                <tr>
                    
                    <td colspan="3" style="border: none;"></td>
                    <td style="border-top: 2px solid black; font-weight: bold; text-align:left;">₹1261.30</td>
                </tr>
            </tbody>
        </table>
    </body>
    </html>
    """


with open("output.pdf", "wb") as pdf:
    pisa.CreatePDF(html, dest=pdf)

print("PDF generated successfully!")
