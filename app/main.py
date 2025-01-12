from typing import List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .models import Item, Shot
from .schemas import ItemCreate, ItemResponse
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# データベースセッションを取得する依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: ItemCreate) -> Item:
    db = SessionLocal()
    db_item = Item(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/", response_model=List[ItemResponse])
async def read_items() -> List[Item]:
    db = SessionLocal()
    items = db.query(Item).all()
    return items

@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int) -> Item:
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.get("/game", response_class=HTMLResponse)
async def get_game():
    game_html = Path("templates/game.html").read_text(encoding='utf-8')
    return HTMLResponse(content=game_html)

@app.post("/shots/")
def create_shot(db: Session = Depends(get_db)):
    shot = Shot(first_shot_time=datetime.utcnow())
    db.add(shot)
    db.commit()
    db.refresh(shot)
    return shot