from fastapi import APIRouter, HTTPException
from typing import List
from schemas.task_info import TaskStatus
from services import task_service

router = APIRouter()

@router.get("/tasks/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str):
    status = await task_service.get_task_status(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
    return status

@router.get("/tasks", response_model=List[TaskStatus])
async def list_all_tasks():
    statuses = await task_service.list_all_task_statuses()
    return list(statuses.values())
