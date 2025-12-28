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