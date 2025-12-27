import pdfplumber
import os
import re
import json
from pydantic import BaseModel
import datetime

class Product(BaseModel):
    name: str
    quantity: int
    unitPrice: float
    
class Invoice(BaseModel):
    orderId: int
    customerId: str
    date: datetime.date
    products: list[Product]

directory = "invoices-pdf"
inv_number_re_pattern = r'Order ID:\s*(.+)'
inv_customer_re_pattern = r'Customer ID:\s*(.+)'
inv_date_re_pattern = r'Order Date\s*:\s*(\d{4}-\d{2}-\d{2})'
    
files = os.listdir(directory)

files = [
    f for f in os.listdir(directory)
    if f.endswith(".pdf")
]

if not files:
    raise Exception("Nenhum arquivo encontrado!")

existing_order_ids = set()

if os.path.exists("database.json"):
    with open("database.json", "r", encoding="utf-8") as f:
        existing_data = json.load(f)

    existing_order_ids = {
        item["orderId"] for item in existing_data
    }

dataset = []

with pdfplumber.open(directory + '/' + files[0]) as pdf:
    header = pdf.pages[0].extract_table()[0]

for file in files:
    with pdfplumber.open(directory + '/' + file) as pdf:
        first_page = pdf.pages[0]
        pdf_text = first_page.extract_text()
        table = first_page.extract_table()
    
    match_id = re.search(inv_number_re_pattern, pdf_text)
    match_costumer = re.search(inv_customer_re_pattern, pdf_text)
    match_date = re.search(inv_date_re_pattern, pdf_text)
    
    if match_id:
        invoice_id = match_id.group(1)
    
    if invoice_id in existing_order_ids:
        continue

    if match_costumer:
        invoice_customer = match_costumer.group(1)
        
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

    dataset.append(item.model_dump(mode="json"))

with open("database.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=4, ensure_ascii=False)

print("database.json criado com sucesso!")