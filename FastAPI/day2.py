from fastapi import FastAPI, Query
from typing import Optional, List

app = FastAPI()

# Added new products
products = []

# Add a new product (User Input)
@app.post("/add_product/")
def add_product(id: int, name: str, category: str, price: float, tags: List[str] = Query(default=[])):
    product = {"id": id, "name": name, "category": category, "price": price, "tags": tags}
    products.append(product)
    return {"message": "Product added successfully", "product": product}


# Q1. Get All Products
@app.get("/products/")
def get_products():
    return {"products": products}


# Q2. Filter by Category 
@app.get("/products/category/")
def get_products_by_category(category: Optional[str] = None):
    if category:
        return {"products": [p for p in products if p["category"].lower() == category.lower()]}
    return {"products": products}


# Q3. Price Range Filtering 
@app.get("/products/price/")
def get_products_by_price(min_price: Optional[float] = None, max_price: Optional[float] = None):
    filtered = products
    if min_price is not None:
        filtered = [p for p in filtered if p["price"] >= min_price]
    if max_price is not None:
        filtered = [p for p in filtered if p["price"] <= max_price]
    return {"products": filtered}


# Q4. Search by Name (Validation)
@app.get("/products/search/")
def search_products(q: Optional[str] = Query(None, min_length=2, max_length=20)):
    if q:
        return {"products": [p for p in products if q.lower() in p["name"].lower()]}
    return {"products": products}


# Q5. Multiple Tags Filter
@app.get("/products/tags/")
def get_products_by_tags(tags: List[str] = Query(default=[])):
    if tags:
        return {"products": [p for p in products if any(tag in p["tags"] for tag in tags)]}
    return {"products": products}






