import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.messages import DeleteHistory
from AnieXEricaMusic import userbot as us, app
from AnieXEricaMusic.core.userbot import assistants
from AnieXEricaMusic.misc import SUDOERS

@app.on_message(filters.command(["fstat"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def sg(client: Client, message: Message):
    if len(message.text.split()) < 1 and not message.reply_to_message:
        return await message.reply("fstat username/id/reply")
    if message.reply_to_message:
        args = message.reply_to_message.from_user.id
    else:
        args = message.text.split()[1]
    lol = await message.reply("<code>Checking Fstats...</code>")
    if args:
        try:
            user = await client.get_users(f"{args}")
        except Exception:
            return await lol.edit("<code>Please specify a valid user!</code>")
    bo = ["MissRose_bot", "MissRose_bot"]
    sg = random.choice(bo)
    if 1 in assistants:
        ubot = us.one
    
    try:
        a = await ubot.send_message(sg, f"/fstat {user.id}")
        await a.delete()
    except Exception as e:
        return await lol.edit(e)
    await asyncio.sleep(1)
    
    async for stalk in ubot.search_messages(a.chat.id):
        if stalk.text == None:
            continue
        if not stalk:
            await message.reply("botnya ngambek")
        elif stalk:
            await message.reply(f"{stalk.text}")
            break  # Exit the loop after displaying one message
    
    try:
        user_info = await ubot.resolve_peer(sg)
        await ubot.send(DeleteHistory(peer=user_info, max_id=0, revoke=True))
    except Exception:
        pass
    
    await lol.delete()
    

@app.on_message(filters.command(["fedinfo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def sg(client: Client, message: Message):
    lol = await message.reply("<code>Checking FedInfo...</code>")
    bo = ["MissRose_bot", "MissRose_bot"]
    sg = random.choice(bo)
    if 1 in assistants:
        ubot = us.one
    
    try:
        text = message.text.split(' ', 1)[1]
        a = await ubot.send_message(sg, f"/fedInfo {text}")
        await a.delete()
    except IndexError:
        return await lol.edit("<code>Please specify a valid fedId!.</code>")
    except Exception as e:
        return await lol.edit(str(e))
    
    await asyncio.sleep(1)
    
    async for stalk in ubot.search_messages(a.chat.id):
        if stalk.text is None:
            continue
        if stalk:
            await message.reply(f"{stalk.text}")
            break  
    
    try:
        user_info = await ubot.resolve_peer(sg)
        await ubot.send(DeleteHistory(peer=user_info, max_id=0, revoke=True))
    except Exception:
        pass
    
    await lol.delete()
