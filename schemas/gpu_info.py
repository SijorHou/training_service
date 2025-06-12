# schemas/gpu_info.py

from pydantic import BaseModel
from typing import List

# 每张 GPU 的状态信息
class GPUInfo(BaseModel):
    id: int                     # GPU 编号
    total_memory: int           # 总显存（单位 MB）
    used_memory: int            # 已用显存（单位 MB）
    utilization: float          # 利用率（0.0 ~ 1.0）
    is_available: bool          # 是否可以调度

# 单个节点 GPU 情况
class NodeGPUStatus(BaseModel):
    host: str
    gpus: List[GPUInfo]

class GPUAllocation(BaseModel):
    host: str
    gpus: List[int]
