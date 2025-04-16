from aiogram import Bot, Dispatcher, types, executor
import logging
import config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("👋 Добро пожаловать в Tapme Card! Ваша визитка начинается здесь.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
