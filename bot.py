import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
import replicate
import asyncio

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply("🤖 **Video Face Swap Botu**\n\n1. Bir yüz fotoğrafı gönder\n2. Bir video gönder")

@dp.message(F.video)
async def handle_video(message: types.Message):
    await message.reply("⏳ Video işleniyor... Lütfen bekleyin (30-90 saniye)")

    try:
        # Video indir
        file = await bot.get_file(message.video.file_id)
        await bot.download_file(file.file_path, "target.mp4")

        # Face Swap
        output = replicate_client.run(
            "arabyai-replicate/roop_face_swap:11b6bf0f4e14d808f655e87e5448233cceff10a45f659d71539cafb7163b2e84",
            input={
                "target_video": open("target.mp4", "rb"),
                "swap_image": "https://picsum.photos/id/64/512/512",
                "fps": 15
            }
        )

        await message.reply_video(
            types.BufferedInputFile(open(output[0], "rb"), filename="swapped.mp4")
        )
    except Exception as e:
        await message.reply(f"❌ Hata: {str(e)[:200]}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
