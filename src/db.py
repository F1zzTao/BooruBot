# Hu Tao Art Searcher
# Copyright (C) 2024  F1zzTao

# This file is part of Hu Tao Art Searcher.
# Hu Tao Art Searcher is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Hu Tao Art Searcher.  If not, see <https://www.gnu.org/licenses/>.

# You may contact F1zzTao by this email address: timurbogdanov2008@gmail.com

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
