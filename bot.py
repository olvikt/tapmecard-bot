import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()

# Логгирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode="MarkdownV2")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Состояния
class Form(StatesGroup):
    choose_language = State()

# Команда /start
@dp.message_handler(commands='start', state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(
        "*👋 Приветствуем в Flawless Card\!* \n"
        "Следуйте инструкции бота и создайте свою стильную визитку всего за *2 минуты*\.\n\n"
        "*Для создания визитки* выполните 3 простых шага:\n"
        "1\\. Укажите своё имя и фото\;\n"
        "2\\. Добавьте контакты для связи\;\n"
        "3\\. Расскажите о бизнесе и прикрепите ссылку на сайт или презентацию\.\n\n"
        "🔗 *Посмотрите пример*: [fcard\.me/alex](https://fcard.me/alex)"
    )

    # Клавиатура для выбора языка
    lang_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    lang_keyboard.add(
        KeyboardButton("🇷🇺 Русский"),
        KeyboardButton("🇺🇦 Українська"),
        KeyboardButton("🇬🇧 English")
    )

    await Form.choose_language.set()
    await message.answer("🌐 *Выберите язык визитки:*", reply_markup=lang_keyboard)

# Обработка выбора языка
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

    # Удалим клавиатуру
    await message.answer("🚀 Продолжаем создание визитки... \(следующий шаг будет позже\)", reply_markup=types.ReplyKeyboardRemove())

# Запуск
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
