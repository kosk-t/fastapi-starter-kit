from fastapi.testclient import TestClient
from app.main import app
from app.schemas import ItemCreate
from app.database import SessionLocal
from app.models import Item

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
    def test_read_items():
        # Arrange
        db = SessionLocal()
        db.query(Item).delete()  # Clear the table before test
        db.commit()
        item_data = {"name": "Test Item"}
        client.post("/items/", json=item_data)

        # Act
        response = client.get("/items/")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == item_data["name"]

        # Clean up
        db.query(Item).delete()
        db.commit()
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

        def test_read_items():
            # Arrange
            db = SessionLocal()
            db.query(Item).delete()  # Clear the table before test
            db.commit()
            item_data = {"name": "Test Item"}
            client.post("/items/", json=item_data)

            # Act
            response = client.get("/items/")

            # Assert
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["name"] == item_data["name"]

            # Clean up
            db.query(Item).delete()
            db.commit()

        def test_read_item():
            # Arrange
            db = SessionLocal()
            db.query(Item).delete()  # Clear the table before test
            db.commit()
            item_data = {"name": "Test Item"}
            response = client.post("/items/", json=item_data)
            item_id = response.json()["id"]

            # Act
            response = client.get(f"/items/{item_id}")

            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == item_data["name"]
            assert data["id"] == item_id

            # Clean up
            db.query(Item).delete()
            db.commit()

        def test_update_item():
            # Arrange
            db = SessionLocal()
            db.query(Item).delete()  # Clear the table before test
            db.commit()
            item_data = {"name": "Test Item"}
            response = client.post("/items/", json=item_data)
            item_id = response.json()["id"]
            updated_item_data = {"name": "Updated Test Item"}

            # Act
            response = client.put(f"/items/{item_id}", json=updated_item_data)

            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == updated_item_data["name"]
            assert data["id"] == item_id

            # Clean up
            db.query(Item).delete()
            db.commit()

        def test_delete_item():
            # Arrange
            db = SessionLocal()
            db.query(Item).delete()  # Clear the table before test
            db.commit()
            item_data = {"name": "Test Item"}
            response = client.post("/items/", json=item_data)
            item_id = response.json()["id"]

            # Act
            response = client.delete(f"/items/{item_id}")

            # Assert
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Item deleted successfully"

            # Clean up
            db.query(Item).delete()
            db.commit()

        def test_create_item_boundary_value():
            # Arrange
            item_data = {"name": "A" * 255}  # Assuming 255 is the max length for the name
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

        def test_create_item_exceeding_boundary_value():
            # Arrange
            item_data = {"name": "A" * 256}  # Assuming 255 is the max length for the name
            db = SessionLocal()
            db.query(Item).delete()  # Clear the table before test
            db.commit()

            # Act
            response = client.post("/items/", json=item_data)

            # Assert
            assert response.status_code == 422  # Unprocessable Entity

            # Clean up
            db.query(Item).delete()
            db.commit()

