from fastapi import FastAPI, HTTPException
from .models import Item
from .schemas import ItemCreate, ItemResponse
from .database import SessionLocal

app = FastAPI()

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: ItemCreate) -> Item:
    db = SessionLocal()
    db_item = Item(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int) -> Item:
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item