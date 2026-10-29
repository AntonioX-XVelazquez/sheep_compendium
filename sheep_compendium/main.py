from typing import List

from fastapi import FastAPI, HTTPException, status

from models.db import db
from models.models import Sheep

app = FastAPI()


@app.get("/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    sheep = db.get_sheep(id)
    if sheep is None:
        raise HTTPException(status_code=404, detail="Sheep not found")
    return sheep


@app.post("/sheep/", response_model=Sheep, status_code=status.HTTP_201_CREATED)
def add_sheep(sheep: Sheep):
    # Check if the sheep ID already exists to avoid duplicates
    if sheep.id in db.data:
        raise HTTPException(status_code=400, detail="Sheep with this ID already exists")

    # Add the new sheep to the database
    db.data[sheep.id] = sheep
    return sheep  # Return the newly added sheep data

@app.delete("/sheep/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sheep(id: int):
    if not db.delete_sheep(id):
        raise HTTPException(status_code=404, detail="Sheep not found")
    return None


@app.put("/sheep/{id}", response_model=Sheep)
def update_sheep(id: int, sheep: Sheep):
    # The ID in the URL must match the ID in the body
    if sheep.id != id:
        raise HTTPException(status_code=400, detail="ID in path and body must match")
    updated = db.update_sheep(id, sheep)
    if updated is None:
        raise HTTPException(status_code=404, detail="Sheep not found")
    return updated


@app.get("/sheep/", response_model=List[Sheep])
def read_all_sheep():
    return db.get_all_sheep()
