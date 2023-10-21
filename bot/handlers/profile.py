from ..bot import dp
from .. import db, keyboards, utils, config

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(text="profile")
async def call_profile(call: types.CallbackQuery):
    user_data = await db.users_db.get_user(call.from_user.id)

    await call.message.edit_text(
        (
            f"💎 <b>Профиль</b>"
            f"\n\nНик: <b>{utils.generate_username(call.from_user.id)}</b>"
            f"\nБаланс: <b>{user_data[1]} WAV</b>"
            f"\nОпыт: <b>{user_data[3]} 🔋</b>"
            f"\n\nРеферальная ссылка: <b>https://t.me/{config.BOT_NAME}?start=RF{call.from_user.id}</b>"
            f"\n(1 приглашённый пользователь = <b>{config.INVITE_REWARD_WAV} WAV</b> & <b>{config.INVITE_REWARD_XP} 🔋</b>)"
        ),
        reply_markup=await keyboards.profile(),
    )


@dp.callback_query_handler(text="profile", state="*")
async def call_profile_from_state(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call_profile(call)
