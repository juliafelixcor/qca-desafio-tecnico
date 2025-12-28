from invoice_extractor import InvoiceExtractor
import os

DIRECTORY = "invoices-pdf"

files = [
    f for f in os.listdir(DIRECTORY)
        if f.endswith(".pdf")
]
if not files:
    raise Exception("Nenhum arquivo encontrado!")

extractor = InvoiceExtractor(files)
existing_orders_ids = extractor.existing_ids()
extractor.extracting_information(existing_orders_ids)
extractor.save_json()