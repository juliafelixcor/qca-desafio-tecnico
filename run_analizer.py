from invoice_analizer import InvoiceAnalyzer

path = "database.json"
analyzer = InvoiceAnalyzer(path)
df = analyzer.normalize_invoices()
ai = analyzer.average_invoices(df)
mfp = analyzer.most_frequent_product(df)
tsp = analyzer.total_spent_per_product(df)
ppl = analyzer.products_price_list(df)

analyzer.print_report(ai, mfp, tsp, ppl)