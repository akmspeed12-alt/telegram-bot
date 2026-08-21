import os
from telethon import TelegramClient, events
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

# البيانات المستخرجة من صورتك
api_id = 38739119
api_hash = '76fd508f4878e8d77cd68e88ba65bc85'

# إنشاء جلسة اليوزر بوت
client = TelegramClient('my_userbot_session', api_id, api_hash)

# حقوق الحظر التام (كتم كامل حتى لو كان لديه رتبة)
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
        # تحميل الصورة المؤقتة
        photo_path = await client.download_media(reply_msg.photo)
        
        # رفعها كصورة شخصية للحساب
        file = await client.upload_file(photo_path)
        await client(UploadProfilePhotoRequest(file=file))
        
        # حذف الملف من التخزين المؤقت
        os.remove(photo_path)
        
        # الرد بالرسالة المطلوبة
        await event.reply('×تم التغير بنجاح!')
    else:
        await event.reply('الرجاء الرد على صورة لتغييرها!')


@client.on(events.NewMessage(outgoing=True, pattern='(?i)^كتم$'))
async def mute_user(event):
    if not event.is_reply:
        return
    
    if not event.is_group:
        await event.reply('هذا الأمر يعمل في المجموعات فقط!')
        return

    reply_msg = await event.get_reply_message()
    target_user = reply_msg.sender_id
    
    try:
        # كتم المستخدم حتى لو كان مشرفاً (يتخطى الرتب)
        await client(EditBannedRequest(
            peer=event.chat_id,
            user_id=target_user,
            banned_rights=mute_rights
        ))
        await event.reply('تم الكتم بنجاح!')
    except Exception as e:
        await event.reply(f'حدث خطأ: تأكد من أن لديك صلاحية حظر المشرفين/الأعضاء.\n{str(e)}')

print("Userbot is running...")
client.start()
client.run_until_disconnected()
        
