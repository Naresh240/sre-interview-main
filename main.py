import time
import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
from models import Item
from prometheus_client import start_http_server, Summary, Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client.core import CollectorRegistry


class BaseApiModel(BaseModel):
    name: str


inventory = {}

app = FastAPI()

REQUEST_COUNT = Counter('request_count', 'Total number of requests')
INVENTORY_ITEMS = Gauge('inventory_items', 'Number of items in inventory')


@app.post("/items/")
async def create_item(item: Item):
    if item.name in inventory:
        raise HTTPException(status_code=400, detail="Item already exists")
    inventory[item.name] = item
    INVENTORY_ITEMS.set(len(inventory))
    return item


@app.get("/items/{item_name}")
async def read_item(item_name: str):
    if item_name not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    return inventory[item_name]


@app.put("/items/{item_name}")
async def update_item(item_name: str, item: Item):
    if item_name not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    existing_item = inventory[item_name]
    existing_item.quantity += item.quantity
    if item.price:
        existing_item.price = item.price
    if item.description:
        existing_item.description = item.description
    return existing_item


@app.delete("/items/{item_name}")
async def delete_item(item_name: str):
    if item_name not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    del inventory[item_name]
    INVENTORY_ITEMS.set(len(inventory))
    return {"detail": "Item deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
