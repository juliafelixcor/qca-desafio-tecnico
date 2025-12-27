import pandas as pd

def normalize_invoices(path):
    df = pd.read_json(path)
    df = df.explode("products").reset_index(drop=True)
    products = pd.json_normalize(df["products"])
    return pd.concat([df.drop(columns=["products"]), products], axis=1)

def average_invoices(df):
    df["total-item"] = df["quantity"] * df["unitPrice"]
    total_fatura = df.groupby("orderId")["total-item"].sum()
    return total_fatura.mean()

def most_frequent_product(df):
    return df["name"].value_counts().idxmax()

def total_spent_per_product(df):
    df["total-item"] = df["quantity"] * df["unitPrice"]
    total_product = df.groupby("name")["total-item"].sum()
    return total_product

def products_price_list(df):
    df_products = df[["name", "unitPrice"]]
    return df_products

def print_report(df):
    print("\n----------- Invoice Analytics Report -----------\n")

    print(f"Average invoice value: ${average_invoices(df):.2f}")
    print(f"Most frequent product: {most_frequent_product(df)}\n")

    print("Total spent per product:")
    total_products = total_spent_per_product(df).items()
    for product, total in total_products:
        print(f" - {product}: ${total:.2f}")

    print("\nProduct list (Name|Unit Price):")
    products = products_price_list(df).drop_duplicates()
    for _, row in products.iterrows():
        print(f" - {row['name']} | ${row['unitPrice']:.2f}")

def main():
    path = "database.json"
    normalize_invoices(path)
    df = normalize_invoices("database.json")
    
    print_report(df)

if __name__ == "__main__":
    main()