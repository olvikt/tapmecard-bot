import os
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.webhook import get_new_configured_app
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")  # Например: https://tapmecard-bot.onrender.com
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'  # для Render
WEBAPP_PORT = int(os.getenv('PORT', default=8000))  # Render сам задаёт PORT

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Хендлер на /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "*👋 Приветствуем в Flawless Card!* \n\n"
        "Следуйте инструкции бота и создайте свою стильную визитку всего за 2 минуты.\n\n"
        "Для создания визитки Вам необходимо выполнить 3 простых шага:\n"
        "1. Рассказать о себе и добавить фото;\n"
        "2. Указать контакты для связи;\n"
        "3. Рассказать о Вашем бизнесе, прикрепив ссылку на сайт, презентацию или вашу реферальную ссылку.\n\n"
        "Посмотрите, как может выглядеть ваша визитка: [Пример визитки](https://fcard.me/alex)"
    )
    await message.answer(welcome_text, parse_mode="Markdown")

# Webhook-приложение
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == '__main__':
    from aiogram import executor
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
