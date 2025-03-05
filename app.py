# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# # Define a Pydantic model for request body
# class Item(BaseModel):
#     name: str
#     description: str = None
#     price: float
#     tax: float = None

# # GET endpoint
# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     return {"item_id": item_id}

# # POST endpoint
# @app.post("/items/")
# def create_item(item: Item):
#     return item
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model for request body
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

# In-memory list to store items
items = []

# POST endpoint
@app.post("/items/")
def create_item(item: Item):
    new_item = item.dict()  # Convert Pydantic model to dictionary
    new_item["item_id"] = len(items) + 1  # Assign a unique item_id
    items.append(new_item)
    return new_item

# GET endpoint to list all items
@app.get("/items/")
def read_all_items():
    return items

# GET endpoint to read a specific item by item_id
@app.get("/items/{item_id}")
def read_item(item_id: int):
    try:
        return next(item for item in items if item["item_id"] == item_id)
    except StopIteration:
        return {"error": "Item not found"}

# GET endpoint to update a specific item by item_id
@app.get("/items/update/{item_id}")
def update_item(item_id: int):
    try:
        item = next(item for item in items if item["item_id"] == item_id)
        return item
    except StopIteration:
        return {"error": "Item not found"}

# POST endpoint to update a specific item by item_id
@app.post("/items/update/{item_id}")
def update_item(item_id: int, item: Item):
    try:
        existing_item = next(item for item in items if item["item_id"] == item_id)
        existing_item["name"] = item.name
        existing_item["description"] = item.description
        existing_item["price"] = item.price
        existing_item["tax"] = item.tax
        return existing_item
    except StopIteration:
        return {"error": "Item not found"}

