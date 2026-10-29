import os
import sys

# Add the project root (sheep directory) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import TestClient to simulate API requests
from fastapi.testclient import TestClient

# Import the FastAPI app instance from the controller module
from main import app

# Create a TestClient instance for the FastAPI app
client = TestClient(app)


# Define a test function for reading a specific sheep
def test_read_sheep():
    # Send a GET request to the endpoint "/sheep/1"
    response = client.get("/sheep/1")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response JSON matches the expected data
    assert response.json() == {
        # Expected JSON structure
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe",
    }


# Define a test function for adding a new sheep
def test_add_sheep():
    # TODO: Prepare the new sheep data in a dictionary format.
    new_sheep = {
        "id": 7,
        "name": "Suzie",
        "breed": "Suffolk",
        "sex": "ewe",
    }
    response = client.post("/sheep/", json=new_sheep)

    assert response.status_code == 201
    assert response.json() == new_sheep
    get_response = client.get(f"/sheep/{new_sheep['id']}")
    assert get_response.status_code == 200
    assert get_response.json() == new_sheep


# ---------------- Extra credit tests ----------------

def test_delete_sheep():
    # Add a sheep we can safely delete
    sheep = {"id": 8, "name": "Dolly", "breed": "Babydoll", "sex": "ewe"}
    client.post("/sheep/", json=sheep)

    # Delete it
    response = client.delete("/sheep/8")
    assert response.status_code == 204

    # It should no longer be retrievable
    assert client.get("/sheep/8").status_code == 404

    # Deleting it again should return 404
    assert client.delete("/sheep/8").status_code == 404


def test_update_sheep():
    # Change Blondie (id 2) from a Polypay to an F1 cross
    updated = {"id": 2, "name": "Blondie", "breed": "F1", "sex": "ram"}

    response = client.put("/sheep/2", json=updated)
    assert response.status_code == 200
    assert response.json() == updated

    # Verify the change was saved
    assert client.get("/sheep/2").json() == updated

    # Updating a sheep that doesn't exist should return 404
    missing = {"id": 999, "name": "Ghost", "breed": "None", "sex": "ewe"}
    assert client.put("/sheep/999", json=missing).status_code == 404


def test_read_all_sheep():
    response = client.get("/sheep/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    # The original six sheep should all be present
    ids = [s["id"] for s in data]
    for sheep_id in range(1, 7):
        assert sheep_id in ids

    # Spice should be in the list with the right data
    assert {"id": 1, "name": "Spice", "breed": "Gotland", "sex": "ewe"} in data
