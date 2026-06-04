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

def main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📸 Fotoğraf Modelleri", callback_data="foto_menu")],
        [InlineKeyboardButton(text="🎥 Video Modelleri", callback_data="video_menu")],
        [InlineKeyboardButton(text="🔥 Soyunma / Nude", callback_data="nude_menu")],
        [InlineKeyboardButton(text="👙 Bikini", callback_data="bikini_menu")],
        [InlineKeyboardButton(text="🔄 Face Swap", callback_data="faceswap")]
    ])
    return keyboard

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply("🤖 **Hayaller Gerçekleşir NSFW Bot**\n\nNe yapmak istiyorsun?", reply_markup=main_menu())

# Face Swap
@dp.callback_query(lambda c: c.data == "faceswap")
async def faceswap(callback):
    await callback.message.edit_text("🔄 Face Swap aktif.\n\n1. Yüz fotoğrafı gönder\n2. Hedef video veya fotoğraf gönder")

# Diğer menüler (şimdilik placeholder)
@dp.callback_query(lambda c: c.data in ["foto_menu", "video_menu", "nude_menu", "bikini_menu"])
async def coming_soon(callback):
    await callback.message.edit_text("⚠️ Bu özellik yakında aktif olacak.\n\nŞu anda Face Swap çalışıyor.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
