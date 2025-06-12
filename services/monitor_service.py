import asyncio
from utils.logger import logger
from services import task_service

class MonitorService:
    def __init__(self, poll_interval=5):
        self.poll_interval = poll_interval
        self.running = False
        self.monitored_tasks = {}  # task_id -> asyncio.subprocess.Process

    async def add_task(self, task_id: str, process: asyncio.subprocess.Process):
        self.monitored_tasks[task_id] = process
        logger.info(f"Monitor: Added task {task_id} for monitoring")

    async def start(self):
        if self.running:
            logger.warning("MonitorService is already running")
            return
        self.running = True
        logger.info("MonitorService started")
        while self.running:
            await self.check_tasks()
            await asyncio.sleep(self.poll_interval)

    async def check_tasks(self):
        to_remove = []
        for task_id, process in list(self.monitored_tasks.items()):
            retcode = process.returncode
            if retcode is not None:
                # 进程已结束，处理结果
                if retcode == 0:
                    await task_service.mark_succeeded(task_id)
                    logger.info(f"[{task_id}] Training process completed successfully.")
                else:
                    await task_service.mark_failed(task_id, reason=f"Process exited with code {retcode}")
                    logger.error(f"[{task_id}] Training process failed with code {retcode}.")
                to_remove.append(task_id)
            else:
                logger.debug(f"[{task_id}] Training process running.")
        for task_id in to_remove:
            self.monitored_tasks.pop(task_id, None)

    async def stop(self):
        self.running = False
        logger.info("MonitorService stopped")

monitor_service = MonitorService()
