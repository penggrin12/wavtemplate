"""
Main data storage file
"""

from .loops import loop
import aiosqlite
import asyncio
from time import time


class BasicDB:
    """Base DB class"""

    def __init__(self, name: str):
        self.conn = None
        self.cur = None

        asyncio.get_event_loop().run_until_complete(self.init(name))
        asyncio.get_event_loop().run_until_complete(self.make())

    async def exec_and_commit(self, *args):
        await self.cur.execute(*args)
        await self.conn.commit()

    async def close(self):
        await self.conn.close()

    async def init(self, name: str) -> None:
        self.conn = await aiosqlite.connect(name, loop=loop)
        self.cur = await self.conn.cursor()

    async def make(self) -> None:
        """Make sure that we have the needed sqlite file"""
        pass


class UsersDB(BasicDB):
    def __init__(self):
        super().__init__("dbs/users.db")

    async def make(self) -> None:
        await self.exec_and_commit(
            """
            CREATE TABLE IF NOT EXISTS users(
                "id"        INT     NOT NULL UNIQUE,
                "balance"   INT     DEFAULT 0,
                "deposited" INT     DEFAULT 0,
                "xp"        INT     DEFAULT 0,
                "invites"   INT     DEFAULT 0,
                PRIMARY KEY("id")
            );
            """
        )

    async def make_sure_valid(self, user_id: int) -> None:
        """Make sure that user is in this db"""
        await self.exec_and_commit(
            """INSERT INTO users (id) SELECT ? WHERE NOT EXISTS (SELECT id FROM users WHERE id = ?);""",
            (user_id, user_id),
        )

    async def get_user(self, user_id: int) -> list:
        """Returns a user db list, see `make` to know the order"""
        return await (await self.cur.execute("""SELECT * FROM users WHERE id = ?""", (user_id,))).fetchone()

    async def get_balance(self, user_id: int) -> int:
        return (await (await self.cur.execute("""SELECT balance FROM users WHERE id = ?""", (user_id,))).fetchone())[0]


users_db = UsersDB()
