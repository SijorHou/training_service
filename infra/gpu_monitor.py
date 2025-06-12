# infra/gpu_monitor.py

import subprocess
import json
from schemas.gpu_info import GPUInfo, NodeGPUStatus
from typing import List

NODES = ["g5", "g6"]
mock_data: bool = True

async def get_all_node_gpu_status() -> List[NodeGPUStatus]:
    results = []
    
    if not mock_data:
        for node in NODES:
            try:
                # run the script remotely
                cmd = f"ssh {node} 'python3 ~/get_gpu_status.py'"
                raw_output = subprocess.check_output(cmd, shell=True).decode()
                gpu_list = json.loads(raw_output)

                gpus = [GPUInfo(**gpu) for gpu in gpu_list]
                results.append(NodeGPUStatus(host=node, gpus=gpus))

            except Exception as e:
                print(f"[Error] Failed to get GPU info from {node}: {e}")
    else:
        results = [
        NodeGPUStatus(
            host="g5",
            gpus=[
                GPUInfo(id=0, total_memory=24576, used_memory=4096, utilization=0.2, is_available=True),
                GPUInfo(id=1, total_memory=24576, used_memory=22000, utilization=0.95, is_available=False)
            ]
        ),
        NodeGPUStatus(
            host="g6",
            gpus=[
                GPUInfo(id=0, total_memory=24576, used_memory=1024, utilization=0.05, is_available=True),
                GPUInfo(id=1, total_memory=24576, used_memory=1024, utilization=0.1, is_available=True)
            ]
        )
    ]

    return results
