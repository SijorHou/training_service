from fastapi import APIRouter, BackgroundTasks
from schemas.training_request import TrainingRequest
from services.task_manager import start_training_task

router = APIRouter()

@router.post("/start_training")
async def start_training(request: TrainingRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(start_training_task, request)
    return {"status": "started", "model": request.model_name_or_path}
