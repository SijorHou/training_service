import subprocess
from utils.logger import logger

def run_script(cmd):
    logger.info(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        logger.error(f"Command failed: {result.stderr.decode()}")
        raise RuntimeError("Script failed.")