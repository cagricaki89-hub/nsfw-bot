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
        [InlineKeyboardButton(text="🔥 Soyundurma / Nude", callback_data="nude_menu")],
        [InlineKeyboardButton(text="👙 Bikini", callback_data="bikini_menu")],
        [InlineKeyboardButton(text="🔄 Face Swap", callback_data="faceswap")]
    ])
    return keyboard

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply("🤖 **Hayaller Gerçekleşir NSFW Bot**\n\nNe yapmak istiyorsun?", reply_markup=main_menu())

@dp.callback_query(lambda c: c.data == "nude_menu")
async def nude_menu(callback):
    await callback.message.edit_text("🔥 **Soyundurma Modu Aktif**\n\nSoyundurmak istediğin fotoğrafı gönder.")

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    await message.reply("⏳ Soyundurma işlemi yapılıyor...")

    try:
        file = await bot.get_file(message.photo[-1].file_id)
        await bot.download_file(file.file_path, "input.jpg")

        # Daha uygun bir undress modeli (test için)
        output = replicate_client.run(
            "lucataco/clothoff:8a4265f3b4f6c4f4e9f6f8e8f6f8e8f6f8e8f6f8e8f6f8e8f6f8e8f6f8e8",
            input={"image": open("input.jpg", "rb")}
        )

        await message.reply_photo(types.BufferedInputFile(open(output[0], "rb"), filename="nude.jpg"))
    except Exception as e:
        await message.reply(f"❌ Hata: {str(e)[:200]}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
