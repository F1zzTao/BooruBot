from vkbottle import PhotoMessageUploader
from vkbottle.bot import Bot, Message

from config import VK_API_KEY
from db import create_db, set_block_query
from utils import DanbooruSearcher, SafeBooruSearcher, vk_booru_search

bot = Bot(VK_API_KEY)
upl = PhotoMessageUploader(bot.api)


@bot.on.message(text='!block <tags>')
async def tag_block_handler(message: Message, tags: str):
    await set_block_query(message.from_id, tags)
    return "done"


@bot.on.message(text='!dan <parameters>')
async def danbooru_handler(message: Message, parameters: str):
    result = await vk_booru_search(DanbooruSearcher(), message.from_id, parameters, upl)
    if isinstance(result, str):
        return result

    await message.answer(attachment=','.join(result))


@bot.on.message(text='!sfwbooru <parameters>')
async def safe_booru_handler(message: Message, parameters: str):
    result = await vk_booru_search(SafeBooruSearcher(), message.from_id, parameters, upl)
    if isinstance(result, str):
        return result

    await message.answer(attachment=','.join(result))


if __name__ == "__main__":
    bot.loop_wrapper.on_startup.append(create_db())
    bot.run_forever()
