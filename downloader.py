import asyncio
import traceback
from math import ceil
from os import path, stat

import aiohttp
import wget
from aiofile import async_open


async def download_partial(url, session, start, end):
    """downloads part of a file asynchronously

    Args:
        url (string): url to file
        session (aiohttp.ClientSession): session from which to generate request
        start (int): starting byte (inclusive)
        end (int): ending byte (inclusive)

    Returns:
        bytes: chunk of a file
    """
    headers = {"Range": f"bytes={start}-{end}"}
    async with session.get(url=url, headers=headers) as response:
        return await response.read()


async def download_file(pair, session):
    """downloads a file asynchronously with multiple simultaneous streams

    Args:
        pair (pair): pair of index and url from which to download a file
        session (aiohttp.ClientSession): session from which to generate request
    """
    file_path = "./files/" + wget.filename_from_url(pair[1])

    if path.isfile(file_path) and stat(file_path).st_size > 1:
        return

    try:

        length = 0
        chunk_size = 3000000

        async with session.head(url=pair[1]) as response:
            length = response.headers["content-length"]

        res = await asyncio.gather(
            *[
                download_partial(
                    pair[1], session, i * chunk_size, (i + 1) * chunk_size - 1
                )
                for i in range(0, ceil(int(length) / chunk_size))
            ]
        )

        async with async_open(file_path, "wb") as file:
            await file.write(b"".join(res))
            print(pair[0], response.status, pair[1], sep="\t")

    except BaseException:
        print(traceback.format_exc(), pair[1])


async def download_all_with_index(pairs, session):
    ret = await asyncio.gather(*[download_file(pair, session) for pair in pairs])
    print(f"Completed all {len(ret)} async calls")
