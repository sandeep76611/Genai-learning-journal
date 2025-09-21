from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {
        "app_name": "My First FastAPI App",
        "developer": "Sandeep ",
        "purpose": "Learning FastAPI basics"
    }


@app.get("/multiply")
def multiply(a: int, b: int):
    result = a * b
    return {"a": a, "b": b, "result": result}

#baic parameters
@app.get("/parameters")
def read_item(item_id:int,q:str=None):
    return {"item_id":item_id,"q":q}

#Default values
@app.get("/products/")
def read_products(skip: int =0, limit: int=10):
    return{"skip": skip, "limit":limit}

#Required vs optional
from typing import Optional
@app.get("/users/")
def read_users(name: str, age:Optional[int]=None):
    return{"name": name, "age":age}

#Parameters Validation
from fastapi import Query
@app.get("/search/")
def search_items(q:str = Query(min_length=3, max_length=10, regex="^[a-zA-Z]+$")):
    return{"query": q}

#Multiple Query with same key
from typing import List
@app.get("/tags/")
def get_tags(tags: List[str]=Query(default=[])):
    return{"tags":tags}