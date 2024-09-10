import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

from models import Item  # Import from models.py

inventory = {}

app = FastAPI()

# Define metrics
REQUEST_COUNT = Counter('request_count', 'Total number of requests')
ERROR_COUNT = Counter('error_count', 'Total number of errors')
INVENTORY_ITEMS = Gauge('inventory_items', 'Number of items in inventory')
PRODUCT_QUANTITY = Gauge('product_quantity', 'Quantity of each product in inventory', ['product_name'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Histogram of request latency', ['method', 'endpoint'])

@app.middleware("http")
async def record_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(latency)
    return response

@app.post("/items/")
async def create_item(item: Item):
    REQUEST_COUNT.inc()  # Increment the request count
    try:
        if item.name in inventory:
            raise HTTPException(status_code=400, detail="Item already exists")
        if item.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be a positive number")
        
        inventory[item.name] = item
        INVENTORY_ITEMS.set(len(inventory))
        PRODUCT_QUANTITY.labels(product_name=item.name).set(item.quantity)
        return item
    except HTTPException:
        ERROR_COUNT.inc()
        raise

@app.get("/items/{item_name}")
async def read_item(item_name: str):
    REQUEST_COUNT.inc()  # Increment the request count
    if item_name not in inventory:
        ERROR_COUNT.inc()
        raise HTTPException(status_code=404, detail="Item not found")
    return inventory[item_name]

@app.put("/items/{item_name}")
async def update_item(item_name: str, item: Item):
    REQUEST_COUNT.inc()  # Increment the request count
    if item_name not in inventory:
        ERROR_COUNT.inc()
        raise HTTPException(status_code=404, detail="Item not found")
    
    if item.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be a positive number")

    existing_item = inventory[item_name]
    existing_item.quantity = item.quantity  # Replace current quantity with the new one
    if item.price:
        existing_item.price = item.price
    if item.description:
        existing_item.description = item.description
    
    PRODUCT_QUANTITY.labels(product_name=item_name).set(existing_item.quantity)
    return existing_item

@app.delete("/items/{item_name}")
async def delete_item(item_name: str):
    REQUEST_COUNT.inc()  # Increment the request count
    if item_name not in inventory:
        ERROR_COUNT.inc()
        raise HTTPException(status_code=404, detail="Item not found")
    
    del inventory[item_name]
    INVENTORY_ITEMS.set(len(inventory))
    PRODUCT_QUANTITY.remove(item_name)  # Remove the label if item is deleted
    return {"detail": "Item deleted"}

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
