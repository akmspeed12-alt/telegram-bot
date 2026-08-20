import os
os.system("pip install telethon")

from telethon import TelegramClient, events
from telethon.tl.functions.photos import UploadProfilePhotoRequest

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]

client = TelegramClient("my_userbot", api_id, api_hash)

@client.on(events.NewMessage(outgoing=True, pattern=r"^setprofile$"))
async def set_profile(event):
    reply = await event.get_reply_message()
    if not reply or not reply.photo:
        await event.edit("❌ اعمل Reply على صورة الأول.")
        return
    await event.edit("⏳ جاري تغيير صورة البروفايل...")
    file_path = await reply.download_media()
    uploaded_file = await client.upload_file(file_path)
    await client(UploadProfilePhotoRequest(file=uploaded_file))
    await event.edit("✅ تم تغيير صورتك الشخصية بنجاح!")
    os.remove(file_path)

print("Userbot is running...")
client.start()
client.run_until_disconnected()
