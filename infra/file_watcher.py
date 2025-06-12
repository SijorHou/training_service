# infra/file_watcher.py

import asyncio
import json
import os
from utils.logger import logger
from services import task_service

STATUS_FILE_ROOT = "/home/user/task_logs"  # mock 根目录（未来可配置）

class FileWatcher:

    def __init__(self, poll_interval=5):
        self.poll_interval = poll_interval  # per seconds do polling
        self.running = False

    async def start(self):
        """backend process, periodically poll all status files """
        self.running = True
        while self.running:
            await self.check_all_task_statuses()
            await asyncio.sleep(self.poll_interval)

    async def check_all_task_statuses(self):
        """traverse all tasks, check status files, and update task_service status"""
        tasks = await task_service.task_service.list_tasks()
        for task_id, status in tasks.items():
            try:
                file_path = os.path.join(STATUS_FILE_ROOT, task_id, "train_status.json")
                if os.path.exists(file_path):
                    with open(file_path, "r") as f:
                        content = json.load(f)
                    step = content.get("step", 0)
                    total = content.get("total_steps", 1000)

                    await task_service.task_service.update_progress(task_id, step)

                     
                    if content.get("status") == "failed":
                        await task_service.task_service.mark_failed(task_id, reason="Train script failed")
                    elif step >= total:
                        await task_service.task_service.mark_succeeded(task_id)

            except Exception as e:
                logger.warning(f"[{task_id}] Failed to read progress: {e}")

    def stop(self):
        self.running = False

file_watcher = FileWatcher()
