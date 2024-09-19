import asyncio

import aiohttp
import booru
import msgspec
from vkbottle import PhotoMessageUploader

from config import DEFAULT_BLOCK
from db import get_block_query


class DanbooruSearcher:
    def __init__(self):
        self.dan = booru.Danbooru()
        self.decoder = msgspec.json.Decoder()

    async def search(self, query: str, block: str = '', limit: int = 100) -> list[dict]:
        res = await self.dan.search(
            query=query, block=(DEFAULT_BLOCK+block).strip(), limit=limit
        )
        return self.decoder.decode(res)


class SafeBooruSearcher:
    def __init__(self):
        self.dan = booru.Safebooru()
        self.decoder = msgspec.json.Decoder()

    async def search(self, query: str, block: str = '', limit: int = 100) -> list[dict]:
        res = await self.dan.search(
            query=query, block=(DEFAULT_BLOCK+block).strip(), limit=limit
        )
        return self.decoder.decode(res)


async def get_url_image(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.read()


async def vk_booru_search(
    booru: DanbooruSearcher, from_id: int, parameters: str, uploader: PhotoMessageUploader
) -> list[str] | str:
    splitted_parameters = parameters.split()
    try:
        posts_count = int(splitted_parameters[0])
        query = ' '.join(splitted_parameters[1:])
    except ValueError:
        posts_count = 3
        query = parameters

    if posts_count > 5:
        return "5 posts max"

    block_query = await get_block_query(from_id)
    posts_all = await booru.search(query, block_query, 100)
    posts = posts_all[:posts_count]

    photos = []
    for post in posts:
        post_url = post.get('large_file_url') or post.get('sample_url') or post.get('file_url')
        image_bytes = await get_url_image(post_url)
        photo = await uploader.upload(image_bytes, peer_id=from_id)
        photos.append(photo)

    return photos


async def main():
    # Example usage
    dan = DanbooruSearcher()
    # posts = await dan.search('hu_tao_(genshin_impact) 2girls rating:g')
    posts = await dan.search('id:7946030')
    print(posts)


if __name__ == "__main__":
    asyncio.run(main())
