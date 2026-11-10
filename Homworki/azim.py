import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


TOKEN = "9025497185:AAHRmegM4LaLdgCvao2vuI3_v4y-A7zZBJM"


bot = Bot(token=TOKEN)
dp = Dispatcher()