import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import replicate
import asyncio

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# Ana Menü
def main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📸 Fotoğraf Modelleri", callback_data="foto_menu")],
        [InlineKeyboardButton(text="🎥 Video Modelleri", callback_data="video_menu")],
        [InlineKeyboardButton(text="🔄 Face Swap", callback_data="faceswap")]
    ])
    return keyboard

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply("🤖 **Sumka Tarzı NSFW Bot**\n\nNe yapmak istiyorsun?", reply_markup=main_menu())

@dp.callback_query(lambda c: c.data == "foto_menu")
async def foto_menu(callback):
    await callback.message.edit_text("📸 Fotoğraf Modelleri:\n\nSeçenekler yakında eklenecek...")

@dp.callback_query(lambda c: c.data == "video_menu")
async def video_menu(callback):
    await callback.message.edit_text("🎥 Video Modelleri:\n\nSeçenekler yakında eklenecek...")

@dp.callback_query(lambda c: c.data == "faceswap")
async def faceswap(callback):
    await callback.message.edit_text("🔄 Face Swap aktif.\nYüz fotoğrafı + Video gönder.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
