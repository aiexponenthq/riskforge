import asyncio
from filelock import FileLock
import os

async def main():
    lock = FileLock("test2.lock")
    await asyncio.to_thread(lock.acquire)
    print("Is locked:", lock.is_locked)
    await asyncio.to_thread(lock.release)
    print("Is locked after release:", lock.is_locked)

asyncio.run(main())
