from AnieXEricaMusic import app
from config import OWNER_ID
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import Message
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.errors import MessageDeleteForbidden, RPCError
from asyncio import sleep

BOT_ID = app.id
USE_AS_BOT = True

async def generate_join_link(chat_id: int):
    invite_link = await app.export_chat_invite_link(chat_id)
    return invite_link

def ordinal(n):
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix
    
async def admin_check(message: Message) -> bool:
    if not message.from_user:
        return False

    if message.chat.type not in [ChatType.SUPERGROUP, ChatType.CHANNEL]:
        return False

    if message.from_user.id in [
        777000,  # Telegram Service Notifications
        1087968824,  # GroupAnonymousBot
    ]:
        return True

    client = message._client
    chat_id = message.chat.id
    user_id = message.from_user.id

    check_status = await client.get_chat_member(chat_id=chat_id, user_id=user_id)
    if check_status.status not in [
        ChatMemberStatus.OWNER,
        ChatMemberStatus.ADMINISTRATOR
    ]:
        return False
    else:
        return True
      

def f_sudo_filter(filt, client, message):
    return bool(
        (
            (message.from_user and message.from_user.id in SUDO_USERS)
            or (message.sender_chat and message.sender_chat.id in SUDO_USERS)
        )
        and
        # t, lt, fl 2013
        not message.edit_date
    )


sudo_filter = filters.create(func=f_sudo_filter, name="SudoFilter")


def onw_filter(filt, client, message):
    if USE_AS_BOT:
        return bool(
            True
            and  # message.from_user.id in SUDO_USERS
            # t, lt, fl 2013
            not message.edit_date
        )
    else:
        return bool(
            message.from_user
            and message.from_user.is_self
            and
            # t, lt, fl 2013
            not message.edit_date
        )


f_onw_fliter = filters.create(func=onw_filter, name="OnwFilter")


async def admin_filter_f(filt, client, message):
    return (
        # t, lt, fl 2013
        not message.edit_date
        and await admin_check(message)
    )


admin_filter = filters.create(func=admin_filter_f, name="AdminFilter")


@app.on_message(filters.command("unbanall") & admin_filter)
async def unban_all(_, msg):
    mystic = await msg.reply_text(f"✫ ᴜɴʙᴀɴᴀʟʟ ᴄʜᴀᴛs ᴍᴇᴍʙᴇʀꜱ... ✫", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('✯ ᴄʟᴏsᴇ ✯', callback_data=f"close")]]))
    chat_id = msg.chat.id
    x = 0
    bot = await app.get_chat_member(chat_id, BOT_ID)
    bot_permission = bot.privileges.can_restrict_members == True
    if bot_permission:
        banned_users = []
        async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED):
            banned_users.append(m.user.id)
        
        if not banned_users:
            await mystic.edit_text("ᴛʜᴇʀᴇ ᴀʀᴇ ɴᴏ ʙᴀɴɴᴇᴅ ᴜꜱᴇʀꜱ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('✯ ᴄʟᴏsᴇ ✯', callback_data=f"close")]]))
        else:
            try:
                for user_id in banned_users:
                    await app.unban_chat_member(chat_id, user_id)
                    print(f"ᴜɴʙᴀɴɪɴɢ ᴀʟʟ ᴍᴄ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ {user_id}")
                    x += 1
                await mystic.edit_text(f"✫ ᴀʟʟ ᴜꜱᴇʀꜱ ʜᴀᴠᴇ ʙᴇᴇɴ ᴜɴʙᴀɴɴᴇᴅ.\nᴛᴏᴛᴀʟ ᴜɴʙᴀɴɴᴇᴅ ᴜꜱᴇʀꜱ : {x} ✫", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('✯ ᴄʟᴏsᴇ ✯', callback_data=f"close")]]))
            except Exception:
                await mystic.edit_text("ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴜɴʙᴀɴɴɪɴɢ ᴜꜱᴇʀꜱ.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('✯ ᴄʟᴏsᴇ ✯', callback_data=f"close")]]))
    else:
        await msg.reply_text("ᴇɪᴛʜᴇʀ ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ʀᴇsᴛʀɪᴄᴛ ᴜsᴇʀs ᴏʀ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ɪɴ sᴜᴅᴏ ᴜsᴇʀs")


@app.on_callback_query(filters.regex("^stop$"))
async def stop_callback(_, query):
    await query.message.delete()


@app.on_message(filters.command("purge") & admin_filter)
async def purge(app: app, msg: Message):
    
    if msg.chat.type != ChatType.SUPERGROUP:
        await msg.reply_text(text="**ɪ ᴄᴀɴ'ᴛ ᴘᴜʀɢᴇ ᴍᴇssᴀɢᴇs ɪɴ ᴀ ʙᴀsɪᴄ ɢʀᴏᴜᴘ ᴍᴀᴋᴇ sᴜᴘᴇʀ ɢʀᴏᴜᴘ.**")
        return

    if msg.reply_to_message:
        message_ids = list(range(msg.reply_to_message.id, msg.id))

        def divide_chunks(l: list, n: int = 100):
            for i in range(0, len(l), n):
                yield l[i : i + n]

        
        m_list = list(divide_chunks(message_ids))

        try:
            for plist in m_list:
                await app.delete_messages(chat_id=msg.chat.id, message_ids=plist, revoke=True)
                
            await msg.delete()
        except MessageDeleteForbidden:
            await msg.reply_text(text="**ɪ ᴄᴀɴ'ᴛ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴍᴇssᴀɢᴇs. ᴛʜᴇ ᴍᴇssᴀɢᴇs ᴍᴀʏ ʙᴇ ᴛᴏᴏ ᴏʟᴅ, ɪ ᴍɪɢʜᴛ ɴᴏᴛ ʜᴀᴠᴇ ᴅᴇʟᴇᴛᴇ ʀɪɢʜᴛs, ᴏʀ ᴛʜɪs ᴍɪɢʜᴛ ɴᴏᴛ ʙᴇ ᴀ sᴜᴘᴇʀɢʀᴏᴜᴘ.**")
            return
            
        except RPCError as ef:
            await msg.reply_text(text=f"**sᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ, ʀᴇᴘᴏʀᴛ ɪᴛ ᴜsɪɴɢ** `/bug`<b>ᴇʀʀᴏʀ:</b> <code>{ef}</code>")
        count_del_msg = len(message_ids)
        sumit = await msg.reply_text(text=f"ᴅᴇʟᴇᴛᴇᴅ <i>{count_del_msg}</i> ᴍᴇssᴀɢᴇs")
        await sleep(3)
        await sumit.delete()
        return
    await msg.reply_text("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴛᴀʀᴛ ᴘᴜʀɢᴇ !**")
    return


@app.on_message(filters.command("spurge") & admin_filter)
async def spurge(app: app, msg: Message):

    if msg.chat.type != ChatType.SUPERGROUP:
        await msg.reply_text(text="**ɪ ᴄᴀɴ'ᴛ ᴘᴜʀɢᴇ ᴍᴇssᴀɢᴇs ɪɴ ᴀ ʙᴀsɪᴄ ɢʀᴏᴜᴘ ᴍᴀᴋᴇ sᴜᴘᴇʀ ɢʀᴏᴜᴘ.**")
        return

    if msg.reply_to_message:
        message_ids = list(range(msg.reply_to_message.id, msg.id))

        def divide_chunks(l: list, n: int = 100):
            for i in range(0, len(l), n):
                yield l[i : i + n]

        m_list = list(divide_chunks(message_ids))

        try:
            for plist in m_list:
                await app.delete_messages(chat_id=msg.chat.id, message_ids=plist, revoke=True)
            await msg.delete()
        except MessageDeleteForbidden:
            await msg.reply_text(text="**ɪ ᴄᴀɴ'ᴛ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴍᴇssᴀɢᴇs. ᴛʜᴇ ᴍᴇssᴀɢᴇs ᴍᴀʏ ʙᴇ ᴛᴏᴏ ᴏʟᴅ, ɪ ᴍɪɢʜᴛ ɴᴏᴛ ʜᴀᴠᴇ ᴅᴇʟᴇᴛᴇ ʀɪɢʜᴛs, ᴏʀ ᴛʜɪs ᴍɪɢʜᴛ ɴᴏᴛ ʙᴇ ᴀ sᴜᴘᴇʀɢʀᴏᴜᴘ.**")
            return
            
        except RPCError as ef:
            await msg.reply_text(text=f"**sᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ, ʀᴇᴘᴏʀᴛ ɪᴛ ᴜsɪɴɢ** `/bug`<b>ᴇʀʀᴏʀ:</b> <code>{ef}</code>")           
            return        
    await msg.reply_text("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴛᴀʀᴛ ᴘᴜʀɢᴇ !**")
    return


@app.on_message(filters.command("del") & admin_filter)
async def del_msg(app: app, msg: Message):
    if msg.chat.type != ChatType.SUPERGROUP:
        await msg.reply_text(text="**ɪ ᴄᴀɴ'ᴛ ᴘᴜʀɢᴇ ᴍᴇssᴀɢᴇs ɪɴ ᴀ ʙᴀsɪᴄ ɢʀᴏᴜᴘ ᴍᴀᴋᴇ sᴜᴘᴇʀ ɢʀᴏᴜᴘ.**")
        return        
    if msg.reply_to_message:
        await msg.delete()
        await app.delete_messages(chat_id=msg.chat.id, message_ids=msg.reply_to_message.id)
    else:
        await msg.reply_text(text="**ᴡʜᴀᴛ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ.**")
        return

