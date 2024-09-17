import asyncio

import aiohttp
import booru
import msgspec

from config import DEFAULT_BLOCK


class DanbooruSearcher:
    def __init__(self):
        self.dan = booru.Danbooru()
        self.decoder = msgspec.json.Decoder()

    async def search(self, query: str, block: str = '', limit: int = 100) -> list[dict]:
        res = await self.dan.search(
            query=query, block=(DEFAULT_BLOCK+block).strip(), limit=limit, random=False
        )
        return self.decoder.decode(res)


async def get_url_image(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.read()


async def main():
    # Example usage
    dan = DanbooruSearcher()
    # posts = await dan.search('hu_tao_(genshin_impact) 2girls rating:g')
    posts = await dan.search('id:7946030')
    print(posts)


if __name__ == "__main__":
    asyncio.run(main())
