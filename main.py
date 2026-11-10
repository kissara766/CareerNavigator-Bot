import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from database import init_db, populate_initial_data, get_careers_by_category
from config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class UserState(StatesGroup):
    track = State()
    category = State()


def main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀 Подобрать профессию"), KeyboardButton(text="ℹ️ О боте")]
        ],
        resize_keyboard=True
    )


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        f"Здарова, {message.from_user.first_name}! Я бот-помощник по выбору профессии. "
        f"Помогу определиться со стартом или свитчнуть сферу.",
        reply_markup=main_kb()
    )


@dp.message(F.text == "ℹ️ О боте")
async def about_cmd(message: types.Message):
    await message.answer(
        "Это демо нашего бота для профориентации. "
        "Отвечай на пару вопросов — и получишь персональную подборку профессий."
    )


@dp.message(F.text == "🚀 Подобрать профессию")
async def choose_track(message: types.Message, state: FSMContext):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨‍🎓 Я новичок / подросток", callback_data="track_teen")],
        [InlineKeyboardButton(text="🔄 Хочу сменить работу", callback_data="track_adult")]
    ])
    await message.answer("Для кого ищем направление?", reply_markup=kb)
    await state.set_state(UserState.track)


@dp.callback_query(F.data.startswith("track_"), UserState.track)
async def set_track(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(track=callback.data.split("_")[1])

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💻 IT", callback_data="cat_IT")],
        [InlineKeyboardButton(text="🎨 Дизайн", callback_data="cat_Design")],
        [InlineKeyboardButton(text="📊 Менеджмент", callback_data="cat_Management")]
    ])
    await callback.message.edit_text("Какая сфера больше привлекает?", reply_markup=kb)
    await state.set_state(UserState.category)
    await callback.answer()


@dp.callback_query(F.data.startswith("cat_"), UserState.category)
async def show_results(callback: types.CallbackQuery, state: FSMContext):
    cat = callback.data.split("_")[1]

    # Достаём сохранённый трек, чтобы персонализировать выдачу
    data = await state.get_data()
    audience = data.get("track", "all")

    items = await get_careers_by_category(cat, audience)

    if not items:
        await callback.message.answer("Пока тут пусто, скоро добавим 👀")
        await callback.answer()
        await state.clear()
        return

    await callback.message.edit_text("Вот что я подобрал под тебя")
    for title, desc, salary, steps in items:
        text = (
            f"🔹 <b>{title}</b>\n\n"
            f"📝 {desc}\n"
            f"Зарплата: {salary}\n\n"
            f"Первые шаги:\n{steps}"
        )
        await callback.message.answer(text, parse_mode="HTML")

    await callback.answer()
    await state.clear()

 

async def main():
    logging.basicConfig(level=logging.INFO)
    await init_db()
    await populate_initial_data()
    print("Бот успешно запущен!")
    await dp.start_polling(bot)





if __name__ == "__main__":
    asyncio.run(main())
