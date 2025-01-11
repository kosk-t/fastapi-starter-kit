from fastapi.testclient import TestClient
from app.main import app
from app.schemas import ItemCreate
from app.database import SessionLocal
from app.models import Item, Score

client = TestClient(app)

def test_create_item():
    # Arrange
    item_data = {"name": "Test Item"}
    db = SessionLocal()
    db.query(Item).delete()  # Clear the table before test
    db.commit()

    # Act
    response = client.post("/items/", json=item_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == item_data["name"]
    assert "id" in data

    # Clean up
    db.query(Item).delete()
    db.commit()

def test_hello_world():
    assert 1 + 1 == 2

def test_submit_score():
    # Arrange
    score_data = {"score": 100}
    db = SessionLocal()
    db.query(Score).delete()  # Clear the table before test
    db.commit()

    # Act
    response = client.post("/submit_score/", json=score_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == score_data["score"]
    assert "id" in data

    # Clean up
    db.query(Score).delete()
    db.commit()
