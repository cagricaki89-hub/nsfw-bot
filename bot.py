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
        [InlineKeyboardButton(text="👙 Bikini & İç Çamaşırı", callback_data="bikini_menu")],
        [InlineKeyboardButton(text="🔄 Face Swap", callback_data="faceswap")]
    ])
    return keyboard

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply(
        "🤖 **Hayaller Gerçekleşir NSFW Bot**\n\n"
        "Ne yapmak istiyorsun?", 
        reply_markup=main_menu()
    )

# Face Swap
@dp.callback_query(lambda c: c.data == "faceswap")
async def faceswap(callback):
    await callback.message.edit_text("🔄 **Face Swap Aktif**\n\n1. Yüz fotoğrafı gönder\n2. Hedef video veya fotoğraf gönder")

# Soyundurma
@dp.callback_query(lambda c: c.data == "nude_menu")
async def nude_menu(callback):
    await callback.message.edit_text("🔥 **Soyundurma Modu Aktif**\n\nSoyundurmak istediğin fotoğrafı gönder.")

# Bikini
@dp.callback_query(lambda c: c.data == "bikini_menu")
async def bikini_menu(callback):
    await callback.message.edit_text("👙 **Bikini & İç Çamaşırı Modu Aktif**\n\nFotoğrafı gönder.")

# Fotoğraf İşleme (Soyundurma ve Bikini için)
@dp.message(F.photo)
async def handle_photo(message: types.Message):
    await message.reply("⏳ İşleniyor...")

    try:
        file = await bot.get_file(message.photo[-1].file_id)
        await bot.download_file(file.file_path, "input.jpg")

        # Basit Face Swap (şu an test için)
        output = replicate_client.run(
            "arabyai-replicate/roop_face_swap:11b6bf0f4e14d808f655e87e5448233cceff10a45f659d71539cafb7163b2e84",
            input={
                "swap_image": open("input.jpg", "rb"),
                "target_image": open("input.jpg", "rb")
            }
        )
        await message.reply_photo(types.BufferedInputFile(open(output[0], "rb"), filename="result.jpg"))
    except Exception as e:
        await message.reply(f"❌ Hata: {str(e)[:150]}\n\nKredi yetersiz olabilir.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
