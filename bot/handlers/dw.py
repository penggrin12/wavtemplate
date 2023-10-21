from .. import db, pay, keyboards, states, config
from ..utils import misc as utils
from ..bot import bot, dp
from .start import start

from html import escape
from random import choice
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(text="deposit")
async def call_deposit(call: types.CallbackQuery):
    await states.Deposit.waiting_for_amount.set()
    await call.message.edit_text(
        f"💎 Введите сумму пополнения. (<b><i>минимум</i></b> <b>{config.DEPOSIT_MINIMUM} WAV</b>)",
        reply_markup=await keyboards.deposit(),
    )


@dp.message_handler(state=states.Deposit.waiting_for_amount)
async def state_deposit(message: types.Message, state: FSMContext):
    await state.finish()

    if ("." in message.text) or ("," in message.text):
        await message.answer("Пока-что нельзя использовать не целые числы!")
        return await start(message)

    try:
        amount = int(message.text)
    except ValueError:
        await message.answer("Это не число!")
        return await start(message)

    user_data = await db.users_db.get_user(message.from_user.id)
    overall_balance = await pay.stupidwallet_pay.get_balance()

    if (amount < config.DEPOSIT_MINIMUM) or (amount > config.DEPOSIT_MAXIMUM):
        await message.answer(
            f"Сумма не в диапазоне <b><i>от {int(config.DEPOSIT_MINIMUM)} до {int(config.DEPOSIT_MAXIMUM)}</i> WAV</b>!"
        )
        return await start(message)

    timer = 59

    msg = await message.answer("💎 " + choice(utils.HINTS))

    invoice = await pay.stupidwallet_pay.sw.create_invoice(
        pay.stupidwalletapi.WAV_COIN,
        amount,
        1,
        f"Пополнение баланса в @{config.BOT_NAME}. Погладьте Святоша.",
        f"https://t.me/{config.BOT_NAME}"
    )

    while timer > 0:
        invoice_data = await pay.stupidwallet_pay.sw.get_invoice_data(invoice.id)
        if len(invoice_data.pay_history) > 0:
            await db.users_db.exec_and_commit(
                """UPDATE users SET balance = balance + ? WHERE id = ?;""",
                (amount, message.from_id)
            )

            await msg.edit_text("💎 Баланс успешно пополнен!", reply_markup=await keyboards.deposit_end())

            await bot.send_message(
                config.ADMIN,
                (
                    f"🔔 Пополнение от <b>{escape(message.from_user.first_name)}</b> (<code>{message.from_user.id}</code>)"
                    f" на сумму <b>{amount} WAV</b> (Было всего: <b>{user_data[1]} WAV</b>)"
                    f"\nТеперь на балансе StupidWallet: <b>{overall_balance + amount} WAV</b> (Было всего: <b>{overall_balance} WAV</b>)"
                ),
            )

            return

        await msg.edit_text(f'<a href="https://t.me/stupidwallet_bot?start={invoice.id}">Оплатите счет.</a>\nОжидание оплаты... (Осталось {timer} сек.)')

        timer -= 3
        await sleep(3)

    await msg.edit_text("💎 Вы не успели!", reply_markup=await keyboards.deposit_end())
    return await start(message)


@dp.callback_query_handler(text="withdraw")
async def call_withdraw(call: types.CallbackQuery):
    withdraw_maximum = int(min([int(config.WITHDRAW_MAXIMUM), (await pay.stupidwallet_pay.get_balance()) / 2]))

    if (await db.users_db.get_balance(call.from_user.id)) > config.WITHDRAW_MINIMUM:
        await states.Withdraw.waiting_for_amount.set()
        await call.message.edit_text(
            f"💎 Введите сумму вывода в <b>WAV</b>\n\nМаксимум: <b>{withdraw_maximum} WAV</b>\nМинимум: <b>{config.WITHDRAW_MINIMUM} WAV</b>",
            reply_markup=await keyboards.withdraw(),
        )
    else:
        await call.message.edit_text(
            "⚠️ Не достаточно WAV для вывода!",
            reply_markup=await keyboards.withdraw(),
        )


@dp.message_handler(state=states.Withdraw.waiting_for_amount)
async def state_withdraw(message: types.Message, state: FSMContext):
    await state.finish()

    if ("." in message.text) or ("," in message.text):
        await message.answer("Пока-что нельзя использовать не целые числы!")
        return await start(message)

    try:
        amount = int(message.text)
    except ValueError:
        await message.answer("Это не число!")
        return await start(message)

    if amount < config.WITHDRAW_MINIMUM:
        await message.answer(f"Сейчас минимум для вывода: <b>{config.WITHDRAW_MINIMUM} WAV</b>!")
        return await start(message)

    overall_balance = await pay.stupidwallet_pay.get_balance()
    withdraw_maximum = min([int(config.WITHDRAW_MAXIMUM), overall_balance / 2])

    if amount > withdraw_maximum:
        await message.answer(f"Сейчас максимум для вывода: <b>{withdraw_maximum} WAV</b>!")
        return await start(message)

    user_data = await db.users_db.get_user(message.from_user.id)

    if user_data[1] < amount:
        await message.answer(f"Вам не хватает <b>{round(amount - user_data[1], 4)} WAV</b>!")
        return await start(message)

    await start(message)

    cheque = await pay.stupidwallet_pay.withdraw(message.from_user.id, int(amount))
    await message.answer(f"https://t.me/stupidwallet_bot?start={cheque.id}")

    await bot.send_message(
        config.ADMIN,
        (
            f"🔔 Вывод от <b>{escape(message.from_user.first_name)}</b> (<code>{message.from_user.id}</code>)"
            f" на сумму <b>{amount} WAV</b> (Было всего: <b>{user_data[1]} WAV</b>)"
            f"\nТеперь на балансе StupidWallet: <b>{overall_balance - amount} WAV</b> (Было всего: <b>{overall_balance} WAV</b>)"
        ),
    )
