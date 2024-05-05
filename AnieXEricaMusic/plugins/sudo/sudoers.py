from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.types import Message
from strings import get_string, helpers
from AnieXEricaMusic import app
from AnieXEricaMusic.misc import SUDOERS
from AnieXEricaMusic.utils.database import add_sudo, remove_sudo
from AnieXEricaMusic.utils.decorators.language import language
from AnieXEricaMusic.utils.extraction import extract_user
from AnieXEricaMusic.utils.inline import close_markup
from config import BANNED_USERS, OWNER_ID, START_IMG_URL, OWNER



@app.on_message(filters.command(["addsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER))
@language
async def useradd(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id in SUDOERS:
        return await message.reply_text(_["sudo_1"].format(user.mention))
    added = await add_sudo(user.id)
    if added:
        SUDOERS.add(user.id)
        await message.reply_text(_["sudo_2"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])


@app.on_message(filters.command(["delsudo", "rmsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER))
@language
async def userdel(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id not in SUDOERS:
        return await message.reply_text(_["sudo_3"].format(user.mention))
    removed = await remove_sudo(user.id)
    if removed:
        SUDOERS.remove(user.id)
        await message.reply_text(_["sudo_4"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])


@app.on_message(filters.command(["sudolist"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & ~BANNED_USERS)
async def sudoers_list(client, message: Message):
    keyboard = [[InlineKeyboardButton("𝗚𝗲𝘁 𝗦𝘂𝗱𝗼𝗹𝗶𝘀𝘁", callback_data="check_sudo_list")]]
    reply_markups = InlineKeyboardMarkup(keyboard)
    await message.reply_photo(photo=START_IMG_URL, caption="» ᴄʜᴇᴄᴋ sᴜᴅᴏ ʟɪsᴛ ʙʏ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ.\n\n» ɴᴏᴛᴇ:  ᴏɴʟʏ sᴜᴅᴏ ᴜsᴇʀs ᴄᴀɴ ᴠɪᴇᴡ.", reply_markup=reply_markups)

@app.on_callback_query(filters.regex("^check_sudo_list$"))
async def check_sudo_list(client, callback_query: CallbackQuery):
    keyboard = []
    if callback_query.from_user.id not in SUDOERS:
        return await callback_query.answer("Baby 😘 Sudolist Dekh ke Kya Karoge 🌝���😂", show_alert=True)
    else:
        user = await app.get_users(OWNER_ID)
        AMBOT = user.first_name
        user_mention = (user.first_name if not user.mention else user.mention)
        caption = f"ʟɪsᴛ ᴏғ ʙᴏᴛ ᴍᴏᴅᴇʀᴀᴛᴏʀs˼\n\n💕Oᴡɴᴇʀ  ➥ {user_mention}\n\n"

        keyboard.append([InlineKeyboardButton(AMBOT, url=f"tg://openmessage?user_id={OWNER_ID}")])
        
        count = 1
        for user_id in SUDOERS:
            if user_id != OWNER_ID:
                try:
                    user = await app.get_users(user_id)
                    AMBOT = user.first_name
                    user_mention = user.mention if user else f"💌 Sᴜᴅᴏ {count} ɪᴅ:** {user_id}"
                    caption += f"💌 Sᴜᴅᴏ {count} » {user_mention}\n"
                    button_text = f"{count}. {AMBOT}"
                    keyboard.append([InlineKeyboardButton(button_text, url=f"tg://openmessage?user_id={user_id}")]
                    )
                    count += 1
                except:
                    continue

        # Add a "Back" button at the end
        keyboard.append([InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_to_main_menu")])

        if keyboard:
            reply_markup = InlineKeyboardMarkup(keyboard)
            await callback_query.message.edit_caption(caption=caption, reply_markup=reply_markup)

@app.on_callback_query(filters.regex("^back_to_main_menu$"))
async def back_to_main_menu(client, callback_query: CallbackQuery):
    keyboard = [[InlineKeyboardButton("𝗚𝗲𝘁 𝗦𝘂𝗱𝗼𝗹𝗶𝘀𝘁", callback_data="check_sudo_list")]]
    reply_markupes = InlineKeyboardMarkup(keyboard)
    await callback_query.message.edit_caption(caption="» ᴄʜᴇᴄᴋ sᴜᴅᴏ ʟɪsᴛ ʙʏ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ.\n\n» ɴᴏᴛᴇ:  ᴏɴʟʏ sᴜᴅᴏ ᴜsᴇʀs ᴄᴀɴ ᴠɪᴇᴡ. ", reply_markup=reply_markupes)
