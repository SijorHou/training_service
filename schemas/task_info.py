from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TaskPhase(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class TaskProgress(BaseModel):
    step: int = Field(..., description="当前训练步数")
    total_steps: int = Field(..., description="总训练步数")
    percent: float = Field(..., description="当前进度百分比（0-100）")


class TaskStatus(BaseModel):
    task_id: str
    model_name: str
    phase: TaskPhase
    message: Optional[str] = None   
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    progress: Optional[TaskProgress] = None  
