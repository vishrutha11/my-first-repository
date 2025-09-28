from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Fake in-memory DB
fake_db = []

# Schema
class User(BaseModel):
    id: int
    name: str
    email: str

@app.get("/users")
def get_users():
    return {"name":"John Doe", "age":3, "gender":"Male"}

@app.post("/users")
def create_user(user: User):
    fake_db.append(user)
    return user

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in fake_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for i, user in enumerate(fake_db):
        if user.id == user_id:
            return fake_db.pop(i)
    raise HTTPException(status_code=404, detail="User not found")
