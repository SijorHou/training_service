# services/scheduler_service.py

from schemas.gpu_info import GPUAllocation, NodeGPUStatus
from typing import List, Optional

# simple scheduler: it's prior to select free GPU on the same node 
async def schedule(
    nodes: List[NodeGPUStatus], 
    required_gpus: int
) -> Optional[GPUAllocation]:
    for node in nodes:
        available_gpu_ids = [gpu.id for gpu in node.gpus if gpu.is_available]
        
        if len(available_gpu_ids) >= required_gpus:
            return GPUAllocation(
                host=node.host,
                gpus=available_gpu_ids[:required_gpus]
            )
    return None  # no enough resource
