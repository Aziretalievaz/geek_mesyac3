import asyncio
import logging
from aiogram import F
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command


BOT_TOKEN = "8848875465:AAF45jv4NHguEbWSWS5f1Z-_Gz8Df2G5L8Q"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()     # обработчик входящих обновлений


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет {message.from_user.full_name}, я твой бот!"
    )
    print(f"Пользователь {message.from_user.full_name} написал команду /start!")


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "/start - команда для запуска\n"
        "/help - список команд"
    )

@dp.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer(
        "ya prosto bot, rodilsya v4era.\n"
        "menya propisali v pythone.\n"
        "no sna4ala nado bilo ustanovit ubuntu.\n"
        "esli ubuntu net to obratis k teh.mentory"
    )


@dp.message(F.text.lower() == "группа")
async def cmd_group(message: Message):
    await message.answer("Твоя группа 71-1!")

@dp.message(F.text.lower() == "пока")
async def cmd_bye(message: Message):
    await message.answer("Davai do svidaniya")


# @dp.message(F.from_user.id == 1288365917)
# async def cmd_group(message: Message):
#     await message.answer("Привет мой создатель!!!")


@dp.message()
async def echo(message: Message):
    await message.answer(f"Ты написал: {message.text}")


async def main():
    await dp.start_polling(bot)     # отправляет запросы на тг-сервер


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())