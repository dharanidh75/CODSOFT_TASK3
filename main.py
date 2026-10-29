from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI(title="To-Do List Backend")
db = {}

class TaskModel(BaseModel):
    title: str
    description: str
    completed: bool = False

class TaskOut(TaskModel):
    id: str

@app.post("/tasks/", response_model=TaskOut)
def create_task(task: TaskModel):
    tid = str(uuid4())
    db[tid] = {"id": tid, **task.model_dump()}
    return db[tid]

@app.get("/tasks/", response_model=List[TaskOut])
def get_tasks():
    return list(db.values())

@app.put("/tasks/{tid}/complete", response_model=TaskOut)
def mark_task_complete(tid: str):
    if tid not in db: raise HTTPException(status_code=404, detail="Not found")
    db[tid]["completed"] = True
    return db[tid]

@app.delete("/tasks/{tid}")
def delete_task(tid: str):
    if tid not in db: raise HTTPException(status_code=404, detail="Not found")
    del db[tid]
    return {"message": "Task deleted"}