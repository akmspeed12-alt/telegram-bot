import os
from telethon import TelegramClient, events
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

# قراءة البيانات من الـ Secrets بأمان
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
api_id = int(api_id)

client = TelegramClient('my_userbot_session', api_id, api_hash)

# حقوق الكتم التام
mute_rights = ChatBannedRights(
    until_date=None,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)

@client.on(events.NewMessage(outgoing=True, pattern='(?i)^setprofile$'))
async def set_profile_photo(event):
    if not event.is_reply:
        return
    
    reply_msg = await event.get_reply_message()
    if reply_msg.photo:
        photo_path = await client.download_media(reply_msg.photo)
        file = await client.upload_file(photo_path)
        await client(UploadProfilePhotoRequest(file=file))
        os.remove(photo_path)
        # الرد بتعديل نفس الرسالة الأصلية
        await event.edit('×تم التغير بنجاح!')
    else:
        await event.edit('الرجاء الرد على صورة لتغييرها!')


@client.on(events.NewMessage(outgoing=True, pattern='(?i)^كتم$'))
async def mute_user(event):
    if not event.is_reply:
        return
    
    if not event.is_group:
        await event.edit('هذا الأمر يعمل في المجموعات فقط!')
        return

    reply_msg = await event.get_reply_message()
    target_user = reply_msg.sender_id
    
    try:
        # استخدام entity لتجنب خطأ الـ peer وكتم العضو حتى لو كان مشرفاً
        await client(EditBannedRequest(
            entity=event.chat_id,
            user_id=target_user,
            banned_rights=mute_rights
        ))
        await event.edit('تم الكتم بنجاح!')
    except Exception as e:
        await event.edit(f'حدث خطأ: تأكد من أن لديك صلاحية حظر المشرفين/الأعضاء.\n{str(e)}')

print("Userbot is running and connected...")
client.start()
client.run_until_disconnected()
