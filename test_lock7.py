import asyncio
from filelock import FileLock

async def main():
    lock = FileLock("test7.lock")
    await asyncio.to_thread(lock.acquire)
    print("Acquired in A")
    # See if release does anything
    await asyncio.to_thread(lambda: lock.release(force=True))
    print("Is locked after B release?", lock.is_locked)

asyncio.run(main())
