import asyncio

import aiosqlite

from config import DB_PATH

SQL_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY UNIQUE,
    user_id INTEGER UNIQUE,
    block_query TEXT
);"""


async def create_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(SQL_USERS_TABLE)
        await db.commit()


async def get_block_query(user_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute('SELECT block_query FROM users WHERE user_id=?', (user_id,))
        result = await cursor.fetchone()
        return result[0] if result else ''


async def set_block_query(user_id: int, block_query: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            'INSERT OR REPLACE INTO users (user_id, block_query) VALUES (?, ?)',
            (user_id, block_query)
        )
        await db.commit()


async def main():
    await create_db()


if __name__ == '__main__':
    asyncio.run(main())
