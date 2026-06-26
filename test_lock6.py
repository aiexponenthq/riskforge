import asyncio
from filelock import FileLock

async def main():
    await asyncio.to_thread(FileLock("test6.lock").acquire)
    print("Acquired lock 1")
    
    # Try to acquire with a NEW FileLock object in the same process
    # If this blocks, this is the deadlock!
    await asyncio.to_thread(FileLock("test6.lock").acquire)
    print("Acquired lock 2!")

asyncio.run(main())
