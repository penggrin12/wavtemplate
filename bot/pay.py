"""
Payment related things
"""

from . import db, config
import stupidwalletapi
import typing


class StupidWalletPay:
    def __init__(self):
        self.sw = stupidwalletapi.StupidWalletAPI(config.STUPIDWALLET_TOKEN)

    async def withdraw(self, user_id: int, amount: int) -> typing.Optional[stupidwalletapi.api.Cheque]:
        if (await db.users_db.get_balance(user_id)) < amount:
            return None

        await db.users_db.exec_and_commit(
            """UPDATE users SET balance = balance - ? WHERE id = ?;""", (
                amount, user_id)
        )
        cheque = await self.sw.create_cheque(stupidwalletapi.WAV_COIN, int(amount))
        return cheque

    async def get_balance(self) -> int:
        return await self.sw.get_balance(stupidwalletapi.WAV_COIN)


stupidwallet_pay = StupidWalletPay()
