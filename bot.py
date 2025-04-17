import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv

# Загрузка переменных среды
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

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.MARKDOWN_V2)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Состояния
class Form(StatesGroup):
    choose_language = State()

# /start
@dp.message_handler(commands='start', state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(
        "*👋 Приветствуем в Tapme Card\!* \n"
        "Следуйте инструкции бота и создайте свою стильную визитку всего за *2 минуты*\.\n\n"
        "*Для создания визитки* выполните 3 простых шага:\n"
        "1\\. Укажите своё имя и фото\;\n"
        "2\\. Добавьте контакты для связи\;\n"
        "3\\. Расскажите о бизнесе и прикрепите ссылку на сайт или презентацию\.\n\n"
        "🔗 *Посмотрите пример*: [fcard\.me/alex](https://fcard.me/alex)"
    )

    lang_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    lang_keyboard.add(
        KeyboardButton("🇷🇺 Русский"),
        KeyboardButton("🇺🇦 Українська"),
        KeyboardButton("🇬🇧 English")
    )

    await Form.choose_language.set()
    await message.answer("🌐 *Выберите язык визитки:*", reply_markup=lang_keyboard)

# Обработка языка
@dp.message_handler(state=Form.choose_language)
async def process_language(message: types.Message, state: FSMContext):
    lang_input = message.text.strip().lower()

    if "рус" in lang_input:
        await state.update_data(language='ru')
        await message.answer("Вы выбрали *Русский язык*\.", parse_mode="MarkdownV2")
    elif "укр" in lang_input:
        await state.update_data(language='uk')
        await message.answer("Ви обрали *Українську мову*\.", parse_mode="MarkdownV2")
    elif "eng" in lang_input or "english" in lang_input:
        await state.update_data(language='en')
        await message.answer("You selected *English* language\.", parse_mode="MarkdownV2")
    else:
        await message.answer("Пожалуйста, выберите язык, нажав на одну из кнопок\.", parse_mode="MarkdownV2")
        return

    await message.answer("🚀 Продолжаем создание визитки... \(следующий шаг будет позже\)", reply_markup=ReplyKeyboardRemove())

# Webhook запуск
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
