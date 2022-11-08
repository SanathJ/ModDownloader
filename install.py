from os import mkdir
import shutil
import csv
import asyncio
import time
from downloader import download_all_with_index
from links import create_links_csv
from util import cleanup, unzipper
import aiohttp


async def main():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector()) as session:
        start_time = time.time()
        filepath = input("Zip path: ")
        unzipper(filepath, "./unzipped")

        csv_filename = "links.csv"
        await create_links_csv("./unzipped", session, csv_filename)

        try:
            mkdir("./files")
        except FileExistsError:
            pass

        url_index_pairs = []

        with open(csv_filename, "r", encoding="UTF-8") as csvfile:
            reader = csv.reader(csvfile)
            i = 1
            for line in reader:
                url_index_pairs.append((i, line[0]))
                i = i + 1

        await download_all_with_index(url_index_pairs, session)

        try:
            mkdir("./final")
        except FileExistsError:
            shutil.rmtree("./final")

        shutil.copytree("./unzipped/overrides", "./final", dirs_exist_ok=True)
        shutil.copytree(
            "./files",
            "./final/mods",
            dirs_exist_ok=True,
        )

        cleanup()
        end_time = time.time()
        print(f"finished in {end_time - start_time}s")


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
