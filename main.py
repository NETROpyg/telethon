import asyncio
import os
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

from telethon import TelegramClient, functions

API_ID = 23988357 # ضع API_ID هنا
API_HASH = '25bee10ac433f3dc16a2c0d78bb579de'  # ضع API_HASH هنا

client = TelegramClient('my_session', API_ID, API_HASH)

CHANGE_EVERY = 60  # عدد الثواني بين التحديثات
BASE_IMAGE = 'base.jpg'  # صورة الخلفية الأساسية (يجب أن تكون موجودة)

async def update_name():
    while True:
        now = datetime.now().strftime("%I:%M")
        try:
            await client(functions.account.UpdateProfileRequest(first_name=f"{now} 🕒"))
            print(f"[✔] تم تحديث الاسم إلى {now}")
        except Exception as e:
            print(f"[!] خطأ في تحديث الاسم: {e}")
        await asyncio.sleep(CHANGE_EVERY)

async def update_bio():
    while True:
        now = datetime.now().strftime("%I:%M")
        try:
            await client(functions.account.UpdateProfileRequest(about=f"الوقت الآن ⏰ {now}"))
            print(f"[✔] تم تحديث البايو إلى {now}")
        except Exception as e:
            print(f"[!] خطأ في تحديث البايو: {e}")
        await asyncio.sleep(CHANGE_EVERY)

async def update_photo():
    while True:
        try:
            if not os.path.exists(BASE_IMAGE):
                print(f"[!] صورة الخلفية '{{BASE_IMAGE}}' غير موجودة!")
                return

            now = datetime.now().strftime("%I:%M")
            img = Image.open(BASE_IMAGE)
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 60)
            draw.text((50, 50), now, font=font, fill="white")
            img.save("current.png")

            file = await client.upload_file("current.png")
            await client(functions.photos.UploadProfilePhotoRequest(file))
            print(f"[✔] تم تحديث الصورة إلى {now}")
            os.remove("current.png")

        except Exception as e:
            print(f"[!] خطأ في تحديث الصورة: {e}")
        await asyncio.sleep(CHANGE_EVERY)

async def main():
    await client.start()
    await asyncio.gather(update_name(), update_bio(), update_photo())

with client:
    client.loop.run_until_complete(main())
