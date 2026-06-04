import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

def main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Soyundurma", callback_data="nude")],
        [InlineKeyboardButton(text="🔄 Face Swap", callback_data="swap")],
        [InlineKeyboardButton(text="👙 Bikini", callback_data="bikini")]
    ])
    return keyboard

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply("🤖 **Hayaller Gerçekleşir Bot**\n\nNe yapmak istiyorsun?", reply_markup=main_menu())

@dp.callback_query(lambda c: True)
async def button_handler(callback):
    await callback.message.edit_text("⚙️ Bu özellik yakında aktif edilecek.\n\nŞu an test aşamasındayız.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
