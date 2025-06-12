# services/training_dispatcher.py

import uuid
from schemas.training_request import TrainingRequest
from schemas.task_info import TaskStatus
from services import resource_service, scheduler_service, training_launcher, task_service
from utils.logger import logger

class TrainingDispatcher:

    async def dispatch(self, request: TrainingRequest) -> TaskStatus:
        """
        Receive Training request, schedule resources and start training services
        
            resource_service.get_available_resources() -> List[GPUInfo]
            scheduler_service.schedule(gpu_list, request) -> SchedulerPlan
            training_launcher.launch(plan, request) -> subprocess.Popen
            task_service.register_task(task_id, plan, process)
        """
        # Step 1: generate task_id
        task_id = str(uuid.uuid4())
        logger.info(f"[{task_id}] get training request")

        # Step 2: get current GPU resource info
        gpu_resources = await resource_service.get_available_resources()
        logger.debug(f"[{task_id}] avaiable gpu resources: {gpu_resources}")

        # Step 3: schedule resources
        schedule_plan = await scheduler_service.schedule(gpu_resources, request)
        logger.info(f"[{task_id}] schedule plan: {schedule_plan}")

        # Step 4: start training service
        process = await training_launcher.launch(schedule_plan, request)
        logger.info(f"[{task_id}] start training process: PID={process.pid}")

        # Step 5: regist task
        await task_service.register_task(task_id, schedule_plan, process, request)

        # Step 6: return task status
        return TaskStatus(
            task_id=task_id,
            status="running",
            progress=0.0,
            message="training task start"
        )
