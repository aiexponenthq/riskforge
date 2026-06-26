import asyncio
from filelock import FileLock

async def main():
    lock = FileLock("test.lock")
    print("Acquiring...")
    await asyncio.to_thread(lock.acquire)
    print("Acquired. Releasing...")
    await asyncio.to_thread(lock.release)
    print("Released!")

asyncio.run(main())
