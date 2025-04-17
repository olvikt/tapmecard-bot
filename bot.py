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
    await message.answer("👋 Привет! Это Tapme Card бот. Давай создадим твою визитку!")

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
