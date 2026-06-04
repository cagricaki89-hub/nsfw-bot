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
        [InlineKeyboardButton(text="🔄 Face Swap", callback_data="swap")],
        [InlineKeyboardButton(text="👙 Bikini", callback_data="bikini")]
    ])
    return keyboard

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply("🤖 **Hayaller Gerçekleşir NSFW Bot**\n\nNe yapmak istiyorsun?", reply_markup=main_menu())

@dp.callback_query(F.data == "nude")
async def nude(callback):
    await callback.message.edit_text("🔥 Soyundurma aktif.\nFotoğraf gönder.")

@dp.callback_query(F.data == "swap")
async def swap(callback):
    await callback.message.edit_text("🔄 Face Swap aktif.\nYüz fotoğrafı + hedef gönder.")

@dp.callback_query(F.data == "bikini")
async def bikini(callback):
    await callback.message.edit_text("👙 Bikini modu aktif.\nFotoğraf gönder.")

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    await message.reply("⏳ İşleniyor...")

    try:
        file = await bot.get_file(message.photo[-1].file_id)
        await bot.download_file(file.file_path, "input.jpg")

        # Basit test
        output = replicate_client.run(
            "arabyai-replicate/roop_face_swap:11b6bf0f4e14d808f655e87e5448233cceff10a45f659d71539cafb7163b2e84",
            input={
                "swap_image": open("input.jpg", "rb"),
                "target_image": open("input.jpg", "rb")
            }
        )
        await message.reply_photo(types.BufferedInputFile(open(output[0], "rb"), filename="result.jpg"))
    except Exception as e:
        await message.reply(f"❌ Hata: {str(e)[:150]}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
