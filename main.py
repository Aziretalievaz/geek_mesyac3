import logging
import asyncio 
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message


BOT_TOKEN = "8848875465:AAF45jv4NHguEbWSWS5f1Z-_Gz8Df2G5L8Q"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Assalam Aleikym ya tvoi bot")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    