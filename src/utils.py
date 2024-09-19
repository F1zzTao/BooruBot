import asyncio

import aiohttp
import booru
import msgspec
import random

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


async def vk_booru_search(booru, parameters: str, uploader) -> list[str] | str:
    splitted_parameters = parameters.split()
    try:
        posts_count = int(splitted_parameters[0])
        query = ' '.join(splitted_parameters[1:])
    except ValueError:
        posts_count = 3
        query = parameters

    if post_count >= 6:
        return "5 posts max"

    block_query = await get_block_query(message.from_id)
    posts = await booru.search(query, block_query, posts_count)
    post = random.choice(posts)
    post_url = post['large_file_url']
    image_bytes = await get_url_image(post_url)
    photo = await uploader.upload(image_bytes, message.from_id)
    return [photo]


async def main():
    # Example usage
    dan = DanbooruSearcher()
    # posts = await dan.search('hu_tao_(genshin_impact) 2girls rating:g')
    posts = await dan.search('id:7946030')
    print(posts)


if __name__ == "__main__":
    asyncio.run(main())
