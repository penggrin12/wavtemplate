from aiogram.dispatcher.filters.state import State, StatesGroup


class Deposit(StatesGroup):
    waiting_for_amount = State()


class Withdraw(StatesGroup):
    waiting_for_amount = State()
