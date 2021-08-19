from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Path, Query, HTTPException, status

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

root = {
  "name": "FastAPI REST Testing",
  "Framework": "FastAPI",
  "language": "Python3.9"
}

# inventory = {
#     1: {"name": "Foo"},
#     2: {"name": "Bar",
#         "parent": [
#             "C++",
#             "go",
#             "node"
#         ]},
#     3: {
#         "name": "Bar2",
#         "children": {
#             "Framework1": {"name": "Flask"},
#             "Framework2": {"name": "Django"},
#             "Framework3": {"name": "Pyramid"},
#         }
#     }
# }

inventory = {}

@app.get("/")
def root_project():
    return root

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/hello")
def read_root():
    return {"Hello": "World"}

@app.get("/inv/{item_val}")
def read_inventory(item_val: int = Path(None, description="The inventroy item stash no.", gt=0)):
    return inventory[item_val]

@app.get("/inv-by-name")
def read_inventory_by_name(item_val_name: str):
    for item_val in inventory:
        if inventory[item_val]["name"] == item_val_name:
            return inventory[item_val]
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@app.post("/create-item/{item_id}")
def create_item(item_id:int, item: Item):
    if item_id in inventory:
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Item already Exists")

    inventory[item_id] = item
    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    if item.name != None:
        inventory[item_id].name = item.name

    if item.description != None:
        inventory[item_id].description = item.description

    if item.price != None:
        inventory[item_id].price = item.price

    if item.brand != None:
        inventory[item_id].brand = item.brand
    
    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The inventory item stash no.", gt=0)):
    if item_id not in inventory:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    del inventory[item_id]
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Item Deleted Successfully")
