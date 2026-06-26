import asyncio
from filelock import FileLock
import os
import subprocess

async def main():
    lock = FileLock("test4.lock")
    await asyncio.to_thread(lock.acquire)
    print("Acquired in thread A.")
    
    # Release in thread B
    await asyncio.to_thread(lock.release)
    print("Released in thread B.")

    # Try to acquire in a new process!
    print("Trying to acquire in new process...")
    proc = subprocess.run(["python", "-c", "from filelock import FileLock; FileLock('test4.lock').acquire(timeout=1)"], capture_output=True, text=True)
    print("Process return code:", proc.returncode)
    print("Process stdout:", proc.stdout)
    print("Process stderr:", proc.stderr)

asyncio.run(main())
