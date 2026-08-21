import os
import time
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

api_id = 38739119
api_hash = '76fd508f4878e8d77cd68e88ba65bc85'

client = TelegramClient('my_userbot_session', api_id, api_hash)

mute_rights = ChatBannedRights(
    until_date=None,
    send_messages=True, send_media=True, send_stickers=True,
    send_gifs=True, send_games=True, send_inline=True, embed_links=True
)

@client.on(events.NewMessage(outgoing=True, pattern='(?i)^ping$'))
async def ping_cmd(event):
    start = time.time()
    await event.edit("جاري قياس السرعة...")
    end = time.time()
    ms = round((end - start) * 1000)
    await event.edit(f"• **Pong! 🏓**\n• السرعة: `{ms}ms`")

@client.on(events.NewMessage(outgoing=True, pattern='(?i)^cpu$'))
async def cpu_cmd(event):
    await event.edit("• **حالة المعالج:** يعمل بكفاءة عالية 🟢\n• السيرفر مستقر 100%")

@client.on(events.NewMessage(outgoing=True, pattern='(?i)^(time|الساعة)$'))
async def time_cmd(event):
    t = time.strftime("%I:%M:%S %p")
    await event.edit(f"• **الوقت الحالي:** `{t}`")

@client.on(events.NewMessage(outgoing=True, pattern='(?i)^(id|ايدي)$'))
async def id_cmd(event):
    user = await event.get_sender()
    await event.edit(f"• **معلومات الحساب:**\n- الاسم: `{user.first_name}`\n- الايدي: `{user.id}`\n- اليوزر: `@{user.username}`")

@client.on(events.NewMessage(outgoing=True, pattern='(?i)^setprofile$'))
async def set_profile_photo(event):
    if not event.is_reply:
        return await event.edit("الرجاء الرد على صورة!")
    reply_msg = await event.get_reply_message()
    if reply_msg.photo:
        path = await client.download_media(reply_msg.photo)
        file = await client.upload_file(path)
        await client(UploadProfilePhotoRequest(file=file))
        os.remove(path)
        await event.edit('×تم التغير بنجاح!')
    else:
        await event.edit('الرسالة المحددة ليست صورة!')

@client.on(events.NewMessage(outgoing=True, pattern='(?i)^delprofile$'))
async def del_profile_photo(event):
    photos = await client.get_profile_photos('me')
    if photos:
        await client(DeletePhotosRequest(id=[photos[0]]))
        await event.edit("• تم حذف الصورة الشخصية بنجاح!")
    else:
        await event.edit("• لا توجد صور شخصية لحذفها.")

@client.on(events.NewMessage(outgoing=True, pattern='(?i)^كتم$'))
async def mute_user(event):
    if not event.is_reply or not event.is_group:
        return await event.edit("يجب الرد على رسالة عضو في مجموعة!")
    reply_msg = await event.get_reply_message()
    try:
        await client(EditBannedRequest(entity=event.chat_id, user_id=reply_msg.sender_id, banned_rights=mute_rights))
        await event.edit('تم الكتم بنجاح!')
    except Exception as e:
        await event.edit(f'خطأ في الصلاحيات:\n{str(e)}')

@client.on(events.NewMessage(outgoing=True, pattern='(?i)^(ban|حظر)$'))
async def ban_user(event):
    if not event.is_reply or not event.is_group:
        return await event.edit("يجب الرد على عضو!")
    reply_msg = await event.get_reply_message()
    try:
        ban_rights = ChatBannedRights(until_date=None, view_messages=True)
        await client(EditBannedRequest(entity=event.chat_id, user_id=reply_msg.sender_id, banned_rights=ban_rights))
        await event.edit('• تم حظر المستخدم بنجاح!')
    except Exception as e:
        await event.edit(f'خطأ:\n{str(e)}')

@client.on(events.NewMessage(outgoing=True, pattern='(?i)^reload$'))
async def reload_anim(event):
    anim = ["▰▱▱▱▱ 20%", "▰▰▰▱▱ 60%", "▰▰▰▰▰ 100%", "✨ تم الانتهاء من إعادة التحميل بنجاح!"]
    for x in anim:
        await event.edit(x)
        await asyncio.sleep(0.8)

@client.on(events.NewMessage(outgoing=True, pattern='(?i)^(love|حب)$'))
async def love_anim(event):
    await event.edit("❤️ جاري حساب نسبة الحب...")
    await asyncio.sleep(1)
    await event.edit("██████████ 100%\n💖 حبك مكتسح الدنيا يا غالي!")

print("SOUCE HUDA IS RUNNING...")
client.start()
client.run_until_disconnected()

    
