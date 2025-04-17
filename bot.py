import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
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

    await Form.choose_language.set()
    await message.answer(
        "🌐 *Выберите язык визитки:*\n"
        "1\\. Русский\n"
        "2\\. Українська\n"
        "3\\. English"
    )

# Обработка выбора языка
@dp.message_handler(state=Form.choose_language)
async def process_language(message: types.Message, state: FSMContext):
    lang = message.text.strip().lower()

    if lang in ['1', 'русский', 'ru']:
        await state.update_data(language='ru')
        await message.answer("Вы выбрали *Русский язык*\.", parse_mode="MarkdownV2")
    elif lang in ['2', 'українська', 'uk']:
        await state.update_data(language='uk')
        await message.answer("Ви обрали *Українську мову*\.", parse_mode="MarkdownV2")
    elif lang in ['3', 'english', 'en']:
        await state.update_data(language='en')
        await message.answer("You selected *English* language\.", parse_mode="MarkdownV2")
    else:
        await message.answer("Пожалуйста, выберите язык, отправив *1*, *2* или *3*\.", parse_mode="MarkdownV2")
        return

    # Здесь будет следующий шаг анкеты
    await message.answer("🚀 Продолжаем создание визитки... \(следующий шаг будет позже\)")

# Запуск
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
