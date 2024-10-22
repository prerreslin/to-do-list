from fastapi import FastAPI,HTTPException
from db import Session,Tasks
from sqlalchemy import select,update
from schemas import TasksData
from uvicorn import run

app = FastAPI()

@app.get("/get_tasks")
def get_tasks():
    with Session.begin() as session:
        tasks = session.query(Tasks).all()
        tasks = [TasksData.model_validate(task.__dict__) for task in tasks]
        return tasks

@app.post("/add_task")
def add_task(data:TasksData):
    with Session.begin() as session:
        task = Tasks(**data.model_dump())
        session.add(task)
        return {"Task":"Created"}

@app.delete("/delete_task")
def delete_task(id:int):
    with Session.begin() as session:
        task = session.scalar(select(Tasks).where(Tasks.id == id))
        if task:
            session.delete(task)
            return {"Task":"Deleted"}
        return HTTPException(status_code=404,detail="Not found")
        
@app.put("/change_task")
def change_task(data:TasksData):
    with Session.begin() as session:
        task = session.scalar(select(Tasks).where(Tasks.id == data.id))
        if task:
            updated = update(Tasks).where(Tasks.id == data.id).values(task = data.task)
            session.execute(updated)
            return {"Task":"Changed"}
        return HTTPException(status_code=404,detail="Not found")
    
if __name__ == "__main__":
    run(app=app, port=8000)