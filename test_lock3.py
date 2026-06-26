import asyncio
from filelock import FileLock
import os

async def main():
    lock = FileLock("test3.lock")
    await asyncio.to_thread(lock.acquire)
    print("Acquired in thread.")
    
    # Try to acquire in a new thread, it should block if the lock wasn't released!
    await asyncio.to_thread(lock.release)
    print("Released in thread.")

    # Let's try to acquire it again in another thread with timeout
    try:
        await asyncio.to_thread(lambda: lock.acquire(timeout=1))
        print("Successfully acquired again!")
        await asyncio.to_thread(lock.release)
    except Exception as e:
        print("Failed to acquire again:", type(e))

asyncio.run(main())
