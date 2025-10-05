from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Fake DB
fake_db = {
    1: {"name": "Alice", "age": 30},
    2: {"name": "Bob", "age": 25}
}

class User(BaseModel):
    name: str
    age: int

@app.get("/")
def read_root():
    return fake_db

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = fake_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/")
def create_user(user: User):
    new_id = max(fake_db.keys()) + 1
    fake_db[new_id] = user.dict()
    return {"id": new_id, "user": user}