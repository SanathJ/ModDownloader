import json
import asyncio


async def find_CDN_link(mod, session):
    async with session.get(
        f"https://api.curse.tools/v1/cf/mods/{mod['projectID']}/files/{mod['fileID']}"
    ) as res:

        link = ""
        try:
            link = (await res.json())["data"]["downloadUrl"].replace(
                "https://edge", "https://media"
            )
        except KeyError:
            print(res)

        link = link.replace("+", "%2B")
        return link


async def create_links_csv(manifest_directory, session, outfile):
    with open(manifest_directory + "//manifest.json", "r", encoding="UTF-8") as f:
        manifest = json.load(f)

        links = await asyncio.gather(
            *[find_CDN_link(mod, session) for mod in manifest["files"]]
        )

        with open(outfile, "w", encoding="UTF-8") as out:
            out.write(",\n".join(links))
