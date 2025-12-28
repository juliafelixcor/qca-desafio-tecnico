import pdfplumber
import os
import re
import json
import datetime
from models import Product, Invoice

DIRECTORY = "invoices-pdf"
inv_number_pattern = r'Order ID:\s*(.+)'
inv_customer_pattern = r'Customer ID:\s*(.+)'
inv_date_pattern = r'Order Date\s*:\s*(\d{4}-\d{2}-\d{2})'

class InvoiceExtractor:
    def __init__(self, files):  
        self.files = files
        self.dataset = []
    
    def existing_ids(self):
        existing_order_ids = set()

        if os.path.exists("database.json"):
            with open("database.json", "r", encoding="utf-8") as f:
                existing_data = json.load(f)

            existing_order_ids = {
                item["orderId"] for item in existing_data
            }
        return existing_order_ids
    
    def extracting_information(self, existing_order_ids):
        for file in self.files:
            with pdfplumber.open(DIRECTORY + '/' + file) as pdf:
                first_page = pdf.pages[0]
                pdf_text = first_page.extract_text()
                table = first_page.extract_table()
            
            match_id = re.search(inv_number_pattern, pdf_text)
            match_customer = re.search(inv_customer_pattern, pdf_text)
            match_date = re.search(inv_date_pattern, pdf_text)
            
            if not (match_id and match_customer and match_date and table):
                continue
            
            if match_id:
                invoice_id = match_id.group(1)
            
            if invoice_id in existing_order_ids:
                continue

            if match_customer:
                invoice_customer = match_customer.group(1)
                
            if match_date:
                invoice_date = datetime.datetime.strptime(match_date.group(1), "%Y-%m-%d").date()
                
            item = Invoice(
                orderId = invoice_id,
                customerId = invoice_customer,
                date = invoice_date,
                products = [
                    Product(
                        name = row[1], 
                        quantity = int(row[2]), 
                        unitPrice = float(row[3])
                    )
                    for row in table[1:-1]
                ]
            )

            self.dataset.append(item.model_dump(mode="json"))
        
    def save_json(self): 
        with open("database.json", "w", encoding="utf-8") as f:
            json.dump(self.dataset, f, indent=4, ensure_ascii=False)

        print("database.json criado!")