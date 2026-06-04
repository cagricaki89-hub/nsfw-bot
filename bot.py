import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
import asyncio

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

def main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📸 Fotoğraf Modelleri", callback_data="foto_menu")],
        [InlineKeyboardButton(text="🎥 Video Modelleri", callback_data="video_menu")],
        [InlineKeyboardButton(text="🔥 Soyundurma / Nude", callback_data="nude_menu")],
        [InlineKeyboardButton(text="👙 Bikini & İç Çamaşırı", callback_data="bikini_menu")],
        [InlineKeyboardButton(text="🔄 Face Swap", callback_data="faceswap")],
        [InlineKeyboardButton(text="💎 VIP Paketler", callback_data="vip_menu")]
    ])
    return keyboard

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply(
        "🤖 **Hayaller Gerçekleşir NSFW Bot**\n\n"
        "Ne yapmak istiyorsun?", 
        reply_markup=main_menu()
    )

@dp.callback_query(lambda c: c.data == "vip_menu")
async def vip_menu(callback):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 100 Kredi - 900 Stars", callback_data="buy_100")],
        [InlineKeyboardButton(text="💰 300 Kredi - 2500 Stars", callback_data="buy_300")],
        [InlineKeyboardButton(text="👑 VIP Aylık - 8000 Stars", callback_data="buy_vip")]
    ])
    await callback.message.edit_text("💎 **VIP Paketler**\n\nKaç kredi almak istiyorsun?", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "buy_100")
async def buy_100(callback):
    prices = [LabeledPrice(label="100 Kredi Paketi", amount=900)]
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title="100 Kredi Paketi",
        description="Yaklaşık 30-35 görsel + 5-7 video",
        payload="vip_100",
        provider_token=os.getenv("PAYMENT_TOKEN"),
        currency="XTR",
        prices=prices
    )

@dp.callback_query(lambda c: c.data == "buy_300")
async def buy_300(callback):
    prices = [LabeledPrice(label="300 Kredi Paketi", amount=2500)]
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title="300 Kredi Paketi",
        description="Yaklaşık 90-100 görsel + 15-20 video",
        payload="vip_300",
        provider_token=os.getenv("PAYMENT_TOKEN"),
        currency="XTR",
        prices=prices
    )

@dp.callback_query(lambda c: c.data == "buy_vip")
async def buy_vip(callback):
    prices = [LabeledPrice(label="VIP Aylık Paket", amount=8000)]
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title="VIP Aylık Paket",
        description="3000 kredi + öncelikli kullanım",
        payload="vip_aylik",
        provider_token=os.getenv("PAYMENT_TOKEN"),
        currency="XTR",
        prices=prices
    )

# Diğer menüler (şimdilik)
@dp.callback_query(lambda c: c.data in ["foto_menu", "video_menu", "nude_menu", "bikini_menu", "faceswap"])
async def coming_soon(callback):
    await callback.message.edit_text("⚠️ Bu özellik yakında aktif olacak.\n\nVIP paket alarak öncelik kazanabilirsiniz.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
