# services/task_service.py

import asyncio
from typing import Dict
from datetime import datetime
from schemas.task_info import TaskStatus, TaskPhase, TaskProgress
from schemas.gpu_info import GPUAllocation
from schemas.training_request import TrainingRequest
from utils.logger import logger

_task_registry: Dict[str, TaskStatus] = {}

class TaskService:

    async def register_task(self, task_id: str, allocation: GPUAllocation, process: asyncio.subprocess.Process, request: TrainingRequest):
        logger.info(f"[{task_id}] Registering task for model {request.model_name_or_path}")
        
        # initialice a task status
        status = TaskStatus(
            task_id=task_id,
            model_name=request.model_name_or_path,
            phase=TaskPhase.RUNNING,
            start_time=datetime.now(),
            progress=TaskProgress(
                step=0,
                total_steps=request.training_config.training_arguments.steps,
                percent=0.0
            )
        )
        _task_registry[task_id] = status

    async def get_task(self, task_id: str) -> TaskStatus:
        return _task_registry.get(task_id)

    async def list_tasks(self) -> Dict[str, TaskStatus]:
        return _task_registry

    async def update_progress(self, task_id: str, step: int):
        status = _task_registry.get(task_id)
        if status and status.progress:
            total = status.progress.total_steps
            percent = (step / total) * 100.0
            status.progress.step = step
            status.progress.percent = round(percent, 2)

    async def mark_failed(self, task_id: str, reason: str):
        status = _task_registry.get(task_id)
        if status:
            status.phase = TaskPhase.FAILED
            status.message = reason
            status.end_time = datetime.utcnow()

    async def mark_succeeded(self, task_id: str):
        status = _task_registry.get(task_id)
        if status:
            status.phase = TaskPhase.SUCCEEDED
            status.end_time = datetime.utcnow()

task_service = TaskService()
