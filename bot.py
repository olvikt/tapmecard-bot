import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode="MarkdownV2")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    choose_language = State()

@dp.message_handler(commands='start', state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    # 1. Приветствие с изображением
    await bot.send_photo(
        message.chat.id,
        photo="https://fcard.me/static/fcard-preview.jpg",
        caption=(
            "*👋 Приветствуем в Flawless Card\!* \n"
            "Создайте визитку и делитесь контактами, соцсетями и презентациями всего за *2 минуты*\.\n\n"
            "✔️ Удобно\n✔️ Красиво\n✔️ Бесплатно\n\n"
            "🔗 [Пример визитки](https://fcard.me/alex)"
        )
    )

    # 2. Отдельное сообщение с клавиатурой
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇺🇦 Українська", callback_data="lang_uk"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
    )

    await message.answer("🌐 *Выберите язык визитки:*", reply_markup=keyboard)
    await Form.choose_language.set()

@dp.callback_query_handler(lambda c: c.data.startswith('lang_'), state=Form.choose_language)
async def process_language(callback_query: types.CallbackQuery, state: FSMContext):
    lang_code = callback_query.data.split('_')[1]
    lang_map = {'ru': 'Русский', 'uk': 'Українська', 'en': 'English'}

    await state.update_data(language=lang_code)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        f"✅ Вы выбрали *{lang_map[lang_code]} язык*\.",
        parse_mode="MarkdownV2"
    )

    await bot.send_message(callback_query.from_user.id, "🚀 Продолжаем создание визитки...")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
