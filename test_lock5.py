import asyncio
from filelock import FileLock

async def main():
    lock = FileLock("test5.lock")
    await asyncio.to_thread(lock.acquire)
    print("Acquired in Thread A")
    
    # Release in Thread B
    await asyncio.to_thread(lambda: lock.release(force=True))
    print("Released in Thread B with force=True")
    
    # Try to acquire in Thread C
    await asyncio.to_thread(lock.acquire)
    print("Acquired in Thread C! No deadlock!")
    await asyncio.to_thread(lambda: lock.release(force=True))

asyncio.run(main())
