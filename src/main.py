import random

from vkbottle import PhotoMessageUploader
from vkbottle.bot import Bot, Message

from config import VK_API_KEY
from db import create_db, get_block_query, set_block_query
from utils import DanbooruSearcher, get_url_image

bot = Bot(VK_API_KEY)
upl = PhotoMessageUploader(bot.api)


@bot.on.message(text='!block <tags>')
async def tag_block_handler(message: Message, tags: str):
    await set_block_query(message.from_id, tags)
    return "done"


@bot.on.message(text='!dan <parameters>')
async def danbooru_handler(message: Message, parameters: str):
    splitted_parameters = parameters.split()
    try:
        posts_count = int(splitted_parameters[0])
        query = ' '.join(splitted_parameters[1:])
    except ValueError:
        posts_count = 3
        query = parameters

    block_query = await get_block_query(message.from_id)
    posts = await DanbooruSearcher().search(query, block_query, posts_count)
    post = random.choice(posts)
    post_url = post['large_file_url']
    image_bytes = await get_url_image(post_url)
    photo = await upl.upload(image_bytes, message.from_id)
    await message.answer(attachment=photo)


if __name__ == "__main__":
    bot.loop_wrapper.on_startup.append(create_db())
    bot.run_forever()
