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
        [InlineKeyboardButton(text="🔥 Soyundurma", callback_data="nude")],
        [InlineKeyboardButton(text="🔄 Face Swap", callback_data="swap")]
    ])
    return keyboard

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply("🤖 **Hayaller Gerçekleşir NSFW Bot**\n\nNe yapmak istiyorsun?", reply_markup=main_menu())

@dp.callback_query(F.data == "swap")
async def swap(callback):
    await callback.message.edit_text("🔄 Face Swap aktif.\nYüz fotoğrafı + hedef fotoğraf gönder.")

@dp.callback_query(F.data == "nude")
async def nude(callback):
    await callback.message.edit_text("🔥 Soyundurma aktif.\nFotoğraf gönder.")

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    await message.reply("⏳ İşleniyor...")

    try:
        file = await bot.get_file(message.photo[-1].file_id)
        await bot.download_file(file.file_path, "input.jpg")

        # Fotoğraf için uygun model
        output = replicate_client.run(
            "codeplugtech/face-swap:6a2c3f8f8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e",
            input={
                "source": open("input.jpg", "rb"),
                "target": open("input.jpg", "rb")
            }
        )
        await message.reply_photo(types.BufferedInputFile(open(output[0], "rb"), filename="result.jpg"))
    except Exception as e:
        await message.reply(f"❌ Hata: {str(e)[:200]}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
