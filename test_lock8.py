import asyncio
from filelock import FileLock

async def main():
    lock = FileLock("test8.lock")
    await asyncio.to_thread(lock.acquire)
    print("Acquired in A")
    # See if release does anything
    await asyncio.to_thread(lambda: lock.release(force=True))
    
    # Try to acquire with NEW FileLock!
    await asyncio.to_thread(FileLock("test8.lock").acquire)
    print("Acquired with NEW FileLock!")

asyncio.run(main())
