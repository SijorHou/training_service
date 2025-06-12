# services/resource_service.py

from infra.gpu_monitor import get_all_node_gpu_status
from schemas.gpu_info import NodeGPUStatus
from typing import List


async def get_available_resources() -> List[NodeGPUStatus]:
    return get_all_node_gpu_status()
