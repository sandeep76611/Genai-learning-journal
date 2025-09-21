from fastapi import FastAPI

app=FastAPI()

#Query Parameters
@app.get("/")
def read_item(item_id:int, q:str=None):
    return{"item_id":item_id, "q":q}

#Path Paramters
@app.get("/items/{item_id}")
def read_item(item_id:int):
    return{"item_id":item_id}

#Both Parameters
@app.get("/items/{item_id}/details")
def read_items(item_id:int, include_email:bool=False):
    if include_email:
        return{"item_id":item_id, "include_email":"email included"}
    else:
        return{"item_id":item_id, "include_email":"email not included"}
    


#Path Paramters
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": "John Doe", "role": "customer"}



#Query Parameters
@app.get("/products/")
def search_products(category: str = None, limit: int = 5):
    products = ["Laptop", "Phone", "Tablet", "Camera", "Headphones", "Smartwatch"]
    
    if category == "electronics":
        products = ["Laptop", "Phone", "Tablet"]
    
    return {"category": category, "results": products[:limit]}



#Both Parameters
@app.get("/restaurants/{restaurant_id}/menu")
def get_menu(restaurant_id: int, category: str = None):
    menu = {
        "restaurant_id": restaurant_id,
        "items": ["Burger", "Pizza", "Salad", "Pasta"]
    }
    if category == "veg":
        menu["items"] = ["Salad", "Veg Pizza"]
    
    return menu
