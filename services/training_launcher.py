import asyncio
from infra.shell_runner import run_ssh_command
from typing import List
from schemas.gpu_info import GPUAllocation
from schemas.training_request import TrainingRequest
import logging

logger = logging.getLogger(__name__)

class TrainingLauncher:

    async def launch(self, allocation: GPUAllocation, request: TrainingRequest) -> asyncio.subprocess.Process:
        """
        According to the scheduled GPU resource allocation and training request, 
        construct the start command and execute it remotely asynchronously.
        
        Return the asyncio.subprocess.Process object for subsequent monitoring.
        """

        host = allocation.host
        gpu_ids = allocation.gpus

        gpu_str = ",".join(str(gpu_id) for gpu_id in gpu_ids)
        train_cmd = (
            f"CUDA_VISIBLE_DEVICES={gpu_str} "
            f"python train.py "
            f"--model {request.model_name_or_path} "
            f"--lr {request.training_config.training_arguments.lr} "
            f"--optim {request.training_config.training_arguments.optim} "
            f"--steps {request.training_config.training_arguments.steps} "
        )

        logger.info(f"Launching training on host {host} with GPUs {gpu_str}")
        process = await run_ssh_command(host, train_cmd)
        return process

training_launcher = TrainingLauncher()
