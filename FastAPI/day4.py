# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import Dict

# app = FastAPI()


# class Product(BaseModel):
#     name: str
#     description: str
#     price: float
#     in_stock: bool = True   


# products_db: Dict[int, dict] = {}


# @app.post("/products/{product_id}")
# def create_product(product_id: int, product: Product):
#     if product_id in products_db:
#         raise HTTPException(status_code=400, detail="Product already exists")
    
#     products_db[product_id] = product.dict()
#     return {
#         "message": "Product created successfully ",
#         "product_id": product_id,
#         "product": products_db[product_id]
#     }


# @app.get("/products/{product_id}")
# def read_product(product_id: int):
#     if product_id not in products_db:
#         raise HTTPException(status_code=404, detail="Product not found")
    
#     return {
#         "message": "Product retrieved successfully",
#         "product_id": product_id,
#         "product": products_db[product_id]
#     }



# @app.put("/products/{product_id}")
# def update_product(product_id: int, product: Product):
#     if product_id not in products_db:
#         raise HTTPException(status_code=404, detail="Product not found")
    
#     products_db[product_id] = product.dict()
#     return {
#         "message": "Product updated successfully ",
#         "product_id": product_id,
#         "product": products_db[product_id]
#     }


# @app.delete("/products/{product_id}")
# def delete_product(product_id: int):
#     if product_id not in products_db:
#         raise HTTPException(status_code=404, detail="Product not found")
    
#     deleted_product = products_db.pop(product_id)
#     return {
#         "message": "Product deleted successfully ",
#         "product_id": product_id,
#         "deleted_product": deleted_product
#     }



from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app =FastAPI()

#def request of body model
class Item (BaseModel):
    q:str
    des:str
    price:float

#database(temporal storage in memory)
items_db={}

#Post request(add item)
@app.post("/items/{item_id}")
def create_item(item_id:int,item:Item):
    if item_id in items_db:
        raise HTTPException (status_code=400, detail="Item already exists")
    items_db [ item_id]=item.dict()
    return {"message":"Item created successfully", "item_id":item_id, "item":items_db[item_id]}

#Get request (fetch item by id)
@app.get("/items/{item_id}")
def read_item(item_id:int):
    if item_id not in items_db:
        raise HTTPException (status_code=404, detail="Item not found")
    return {"item":items_db[item_id]}






