from ..bot import bot, dp
from .. import db, keyboards, config

from html import escape

from aiogram import types
from aiogram.dispatcher import FSMContext


async def start(message: types.Message) -> types.Message:
    keyboard = await keyboards.start()
    text = "🐻 Bot template by https://github.com/penggrin12"

    if not message.from_user.is_bot:
        return await message.answer(text, reply_markup=keyboard)
    else:
        return await message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(text="start", state="*")
async def call_start_from_state(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call_start(call)


@dp.callback_query_handler(text="start")
async def call_start(call: types.CallbackQuery):
    await start(call.message)


@dp.message_handler(commands=["start", "help"])
async def cmd_start(message: types.Message):
    await start(message)

    args = message.get_args()
    user_data = await db.users_db.get_user(message.from_id)

    if args.startswith("RF") and user_data[3] == 0:
        user_id = int(args.strip("RF"))

        await bot.send_message(
            user_id,
            f"💎 Кто-то зарегистрировался по твоей ссылке!\n\n+<b>{config.INVITE_REWARD_WAV} WAV</b>!\n+<b>{config.INVITE_REWARD_XP} 🔋</b>",
        )
        await db.users_db.exec_and_commit(
            """UPDATE users SET balance = balance + ? WHERE id = ?;""", (config.INVITE_REWARD_WAV, user_id)
        )
        await db.users_db.exec_and_commit(
            """UPDATE users SET xp = xp + ? WHERE id = ?;""", (config.INVITE_REWARD_XP, user_id)
        )

        await db.users_db.exec_and_commit("""UPDATE users SET invites = invites + 1 WHERE id = ?;""", (user_id,))

    if args.startswith("stupidwallet") and user_data[3] == 0:
        await bot.send_message(
            config.ADMIN,
            f"💎 Новый пользователь с ЭкоСистемы <b>{escape(message.from_user.first_name)}</b> (<code>{message.from_user.id}</code>)"
        )

        await db.users_db.exec_and_commit(
            """UPDATE users SET balance = balance + ? WHERE id = ?;""", (5, message.from_id)
        )
        await db.users_db.exec_and_commit(
            """UPDATE users SET xp = xp + ? WHERE id = ?;""", (150, message.from_id)
        )

        await message.answer("За регистрацию с ЭкоСистемы вы получили небольшой бонус! <3")

    if user_data[3] == 0:
        # To check if user just registered we just see if their xp is 0.
        # So we should set it to atleast 1 here.
        await db.users_db.exec_and_commit(
            """UPDATE users SET xp = 1 WHERE id = ?;""", (message.from_id,)
        )
