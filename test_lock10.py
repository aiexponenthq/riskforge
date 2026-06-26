import asyncio
from filelock import FileLock

async def main():
    lock = FileLock("test10.lock")
    await asyncio.to_thread(lock.acquire)
    print("Acquired in A")
    
    # No release at all!
    
    # Try to acquire with NEW FileLock!
    await asyncio.to_thread(FileLock("test10.lock").acquire)
    print("Acquired with NEW FileLock!")

asyncio.run(main())
