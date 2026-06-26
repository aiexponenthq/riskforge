with open("src/riskforge/storage/filesystem.py", "r") as f:
    content = f.read()

content = content.replace("        self._audit_lock = asyncio.Lock()\n", "        self._async_lock = None\n")
content = content.replace("self._async_lock is None:", "getattr(self, '_async_lock', None) is None:")

with open("src/riskforge/storage/filesystem.py", "w") as f:
    f.write(content)
