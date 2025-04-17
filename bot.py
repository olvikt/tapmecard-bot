import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv
from texts import texts

# Загрузка .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")

# Webhook настройки
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 5000))

# Логгирование
logging.basicConfig(level=logging.INFO)

# Инициализация
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Состояния
class Form(StatesGroup):
    choose_language = State()
    full_name = State()
    photo = State()

# /start
@dp.message_handler(commands='start', state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    lang_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    lang_keyboard.add(
        KeyboardButton("\U0001F1F7\U0001F1FA Русский"),
        KeyboardButton("\U0001F1FA\U0001F1E6 Українська"),
        KeyboardButton("\U0001F1EC\U0001F1E7 English")
    )

    await Form.choose_language.set()
    await message.answer("🌐 <b>Выберите язык визитки:</b>", reply_markup=lang_keyboard)

# Выбор языка
@dp.message_handler(state=Form.choose_language)
async def process_language(message: types.Message, state: FSMContext):
    lang_input = message.text.strip().lower()

    if "рус" in lang_input:
        lang = 'ru'
    elif "укр" in lang_input:
        lang = 'uk'
    elif "eng" in lang_input or "english" in lang_input:
        lang = 'en'
    else:
        await message.answer(texts['invalid_language']['ru'])
        return

    await state.update_data(language=lang)
    await message.answer(texts['language_selected'][lang])
    await Form.full_name.set()
    await message.answer(texts['ask_name'][lang], reply_markup=ReplyKeyboardRemove())

# Получение имени
@dp.message_handler(state=Form.full_name)
async def process_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    data = await state.get_data()
    lang = data.get("language", "ru")
    await Form.photo.set()
    await message.answer(texts['ask_photo'][lang])

# Получение фото
@dp.message_handler(content_types=types.ContentType.PHOTO, state=Form.photo)
async def process_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)

    data = await state.get_data()
    name = data.get("full_name")
    lang = data.get("language", "ru")

    await message.answer(
        texts['confirm'][lang].format(name=name),
        parse_mode="MarkdownV2"
    )

    await state.finish()

# Запуск webhook
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info("Webhook установлен.")

async def on_shutdown(dp):
    await bot.delete_webhook()
    logging.info("Webhook удалён.")

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
