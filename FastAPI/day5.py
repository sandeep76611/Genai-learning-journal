#validation
#path Parameter Validation
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


#Query Parameter Validation
@app.get("/search/")
def search_item(product: str, limit: int = 10):
    return {"product": product, "limit": limit}


#Request Body Validation using pydantic
from pydantic import BaseModel, Field

class Item(BaseModel):
    name:str =Field(...,min_length=2, max_length=10)
    price: float=Field(...,gt=0) 

@app.post("/items/")
def create_item(item:Item):
    return{"item_name":item.name, "item_price":item.price}


#error handling
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int):
    users={1:"kranthi", 2:"sandeep"}
    if user_id not in users:
        raise HTTPException(status_code=404, detail="user not found")
    return{"user": users[user_id]}

#division example
@app.get("/divide/{num}/{den}")
def divide(num: int, den: int):
    if den == 0:
        raise HTTPException(
            status_code=400,
            detail="Denominator cannot be zero "
        )
    return {"result": num / den}
