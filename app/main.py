from typing import List
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.models import Item, Score
from app.schemas import ItemCreate, ItemResponse, ScoreCreate, ScoreResponse
from app.database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/submit_score/", response_model=ScoreResponse)
async def submit_score(score: ScoreCreate) -> Score:
    db = SessionLocal()
    db_score = Score(score=score.score)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score

if __name__ == "__main__":
    import uvicorn
    logging.info("Starting Uvicorn server...")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)