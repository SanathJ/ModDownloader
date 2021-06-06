import asyncio
import csv
import time
import traceback
from math import ceil
from os import path, stat, mkdir

import aiohttp
import wget
from aiofile import async_open


async def downloadPartial(url, session, start, end):
    headers = {'Range': f'bytes={start}-{end}'}
    async with session.get(url=url, headers=headers) as response:
        return await response.read()


async def downloadFile(pair, session):
    filePath = "./files/" + wget.filename_from_url(pair[1])

    if path.isfile(filePath) and stat(filePath).st_size > 1:
        return

    try:

        length = 0
        chunk_size = 3000000

        async with session.head(url=pair[1]) as response:
            length = response.headers['content-length']

        res = await asyncio.gather(*[downloadPartial(pair[1], session, i * chunk_size, (i + 1) * chunk_size - 1) for i in range(0, ceil(int(length) / chunk_size))])

        async with async_open(filePath, 'wb') as fd:
            await fd.write(b''.join(res))
            print(pair[0], response.status, pair[1], sep='\t')

    except:
        print(traceback.format_exc(), pair[1])


async def main(pairs):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=None)) as session:
        ret = await asyncio.gather(*[downloadFile(pair, session) for pair in pairs])
        print(f"Completed all {len(ret)} async calls")

startTime = time.time()

try:
    mkdir("./files")
except FileExistsError:
    pass

URLIndexPairs = []

with open("links.csv") as csvfile:
    reader = csv.reader(csvfile)
    i = 1
    for line in reader:
        URLIndexPairs.append((i, line[0]))
        i = i + 1

loop = asyncio.get_event_loop()
loop.set_debug(True)
loop.slow_callback_duration = 0.3
loop.run_until_complete(main(URLIndexPairs))

endTime = time.time()
print(f"finished in {endTime - startTime}s")
