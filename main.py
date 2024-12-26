from fastapi import FastAPI, APIRouter, HTTPException

from base.configurations import todo_data, db
from database.schemas import all_tasks
from database.models import Todo
from bson.objectid import ObjectId

from base.configurations import MONGO_URI
from datetime import datetime

app = FastAPI()
router = APIRouter()
@router.get("/")
async def get_all_todos():
    # print(db)
    
    data = todo_data.find( )
    return all_tasks(data)
@router.post("/")
async def create_task(new_task: Todo):
    try:
        resp = todo_data.insert_one(dict(new_task))
        return {"status_code": 200, "id":str(resp.inserted_id)}

    except Exception as e:
        return HTTPException(status_code= 500, detail=f"some error eoccured {e}")
    
@router.put("/{task_id}")
async def update_task(task_id: str, updated_task: Todo):
    try:
        id = ObjectId(task_id)
        existing_doc = todo_data.find_one({"_id": id, "is_deleted": False})
        if not existing_doc:
            return HTTPException(status_code=404, detail="Task not found")
        updated_task.updated_at = datetime.now()
        resp= todo_data.update_one({"_id": id}, {"$set": dict(updated_task)})
        return {"status_code": 200, "message": "Task updated successfully"} 
    except Exception as e:
        return HTTPException(status_code= 500, detail=f"some error eoccured {e}")
@router.delete("/{task_id}")
async def delete_task(task_id: str):
    try:
        id = ObjectId(task_id)
        existing_doc = todo_data.find_one({"_id": id, "is_deleted": False})
        if not existing_doc:
            return HTTPException(status_code=404, detail="Task does not exist")
        resp= todo_data.update_one({"_id": id}, {"$set": {"is_deleted": True}})
        return {"status_code": 200, "message": "Task deleted successfully"} 
    except Exception as e:
        return HTTPException(status_code= 500, detail=f"some error eoccured {e}")


app.include_router(router)



