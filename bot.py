import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode="MarkdownV2")
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await bot.send_photo(
        message.chat.id,
        photo="https://fcard.me/static/fcard-preview.jpg",
        caption="*👋 Приветствуем в Flawless Card\!*"
    )

    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇺🇦 Українська", callback_data="lang_uk"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
    )

    await message.answer("🌐 *Выберите язык визитки:*", reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
