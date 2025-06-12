
import asyncio
import logging

logger = logging.getLogger(__name__)

async def run_ssh_command(host: str, command: str) -> asyncio.subprocess.Process:
    ssh_cmd = ["ssh", host, command]
    logger.info(f"Running SSH command asynchronously on {host}: {command}")

    try:
        process = await asyncio.create_subprocess_exec(
            *ssh_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        return process
    except Exception as e:
        logger.error(f"Failed to run SSH command on {host}: {e}")
        raise

async def run_ssh_command_and_get_output(host: str, command: str) -> str:
    proc = await asyncio.create_subprocess_exec(
        "ssh", host, command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"SSH command failed: {stderr.decode()}")
    return stdout.decode()