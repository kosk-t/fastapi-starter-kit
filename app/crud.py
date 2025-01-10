from app.models import Item
from app.schemas import ItemCreate, ItemUpdate
from sqlalchemy.orm import Session


def create_item(db: Session, item: ItemCreate):
    db_item = Item(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def read_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def update_item(db: Session, item_id: int, item: ItemUpdate):
    db_item: Item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db_item.name = item.name
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item