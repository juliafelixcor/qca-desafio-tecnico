import pandas as pd

class InvoiceAnalyzer:
    def __init__(self, path):  
        self.path = path
        
    def normalize_invoices(self):
        df = pd.read_json(self.path)
        df = df.explode("products").reset_index(drop=True)
        products = pd.json_normalize(df["products"])
        df = pd.concat([df.drop(columns=["products"]), products], axis=1)
        df["total_item"] = df["quantity"] * df["unitPrice"]
        return df

    def average_invoices(self, df):
        total_invoice = df.groupby("orderId")["total_item"].sum()
        return total_invoice.mean()

    def most_frequent_product(self, df):
        return df["name"].value_counts().idxmax()

    def total_spent_per_product(self, df):
        total_product = df.groupby("name")["total_item"].sum()
        return total_product

    def products_price_list(self, df):
        df_products = df[["name", "unitPrice"]]
        return df_products

    def print_report(self, average_invoices, frequent_product, total_spent, products_list):
        print("\n----------- Invoice Analytics Report -----------\n")

        print(f"Average invoice value: ${average_invoices:.2f}")
        print(f"Most frequent product: {frequent_product}\n")

        print("Total spent per product:")
        total_products = total_spent.items()
        for product, total in total_products:
            print(f" - {product}: ${total:.2f}")

        print("\nProduct list (Name|Unit Price):")
        products = products_list.drop_duplicates()
        for _, row in products.iterrows():
            print(f" - {row['name']} | ${row['unitPrice']:.2f}")