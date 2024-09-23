from vkbottle import PhotoMessageUploader
from vkbottle.bot import Bot, Message

from config import VK_API_KEY
from db import create_db, get_block_query, set_block_query
from utils import (
    DanbooruSearcher,
    SafeBooruSearcher,
    Rule34Searcher,
    bad_words_in_text,
    vk_booru_search
)

bot = Bot(VK_API_KEY)
upl = PhotoMessageUploader(bot.api)


@bot.on.message(text='!block <tags>')
async def tag_block_handler(message: Message, tags: str):
    if '.' in message or bad_words_in_text(tags):
        return 'nah'
    await set_block_query(message.from_id, tags)
    return "done"


@bot.on.message(text='!blocks')
async def get_block_handler(message: Message):
    blocks = await get_block_query(message.from_id)
    if not blocks:
        return "u don't have them"
    return f"your blocks: {blocks}"


@bot.on.message(text=('!remove block', '!blockrm'))
async def remove_block_handler(message: Message):
    await set_block_query(message.from_id)
    return "done, removed your blocks"


@bot.on.message(text=('!dan <parameters>', '!danbooru <parameters>'))
async def danbooru_handler(message: Message, parameters: str):
    msg_id = (await message.answer("ща сек")).conversation_message_id
    result = await vk_booru_search(DanbooruSearcher(), message.from_id, parameters, upl)
    if isinstance(result, str):
        await bot.api.messages.edit(
            peer_id=message.peer_id,
            message=result,
            conversation_message_id=msg_id
        )

    await bot.api.messages.edit(
        peer_id=message.peer_id,
        attachment=','.join(result),
        conversation_message_id=msg_id
    )


@bot.on.message(text=('!sfwbooru <parameters>', '!safebooru <parameters>'))
async def safe_booru_handler(message: Message, parameters: str):
    msg_id = (await message.answer("ща сек")).conversation_message_id
    result = await vk_booru_search(SafeBooruSearcher(), message.from_id, parameters, upl)
    if isinstance(result, str):
        await bot.api.messages.edit(
            peer_id=message.peer_id,
            message=result,
            conversation_message_id=msg_id
        )

    await bot.api.messages.edit(
        peer_id=message.peer_id,
        attachment=','.join(result),
        conversation_message_id=msg_id
    )


@bot.on.message(text=('!r34 <parameters>', '!rule34 <parameters>'))
async def rule34_handler(message: Message, parameters: str):
    msg_id = (await message.answer("ща сек")).conversation_message_id
    result = await vk_booru_search(Rule34Searcher(), message.from_id, parameters, upl)
    if isinstance(result, str):
        await bot.api.messages.edit(
            peer_id=message.peer_id,
            message=result,
            conversation_message_id=msg_id
        )

    await bot.api.messages.edit(
        peer_id=message.peer_id,
        attachment=','.join(result),
        conversation_message_id=msg_id
    )


if __name__ == "__main__":
    bot.loop_wrapper.on_startup.append(create_db())
    bot.run_forever()
