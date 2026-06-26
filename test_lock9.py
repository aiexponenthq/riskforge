import asyncio
from filelock import FileLock
import time
import fcntl

async def main():
    f1 = open("test9.lock", "w")
    fcntl.flock(f1.fileno(), fcntl.LOCK_EX)
    print("Acquired lock 1")

    f2 = open("test9.lock", "w")
    print("Trying to acquire lock 2...")
    fcntl.flock(f2.fileno(), fcntl.LOCK_EX)
    print("Acquired lock 2!")

asyncio.run(main())
