import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import qrcode
from io import BytesIO
import os

TOKEN = "8058737012:AAFnlLMyHRug4k0hps3SfMfEMy50vnKJ3eY"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Matn, rasm, video yoki musiqa yuboring, men sizga QR kod yaratib beraman.")

@dp.message_handler(content_types=types.ContentType.TEXT)
async def generate_qr_text(message: types.Message):
    text = message.text
    qr = qrcode.make(text)
    bio = BytesIO()
    qr.save(bio, format="PNG")
    bio.seek(0)

    await message.reply_photo(bio, caption="Sizning QR kodingiz!")

@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.VIDEO, types.ContentType.AUDIO, types.ContentType.DOCUMENT])
async def generate_qr_file(message: types.Message):
    file_id = None
    if message.photo:
        file_id = message.photo[-1].file_id
    elif message.video:
        file_id = message.video.file_id
    elif message.audio:
        file_id = message.audio.file_id
    elif message.document:
        file_id = message.document.file_id

    if file_id:
        file = await bot.get_file(file_id)
        file_path = file.file_path
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

        qr = qrcode.make(file_url)
        bio = BytesIO()
        qr.save(bio, format="PNG")
        bio.seek(0)

        await message.reply_photo(bio, caption="Faylingiz uchun QR kod!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
