import os
import future
import asyncio
import requests
import wget
import time
import yt_dlp
from urllib.parse import urlparse
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
from AnieXEricaMusic import app, YouTube
from pyrogram import filters
from pyrogram import Client, filters
from pyrogram.types import Message
from youtubesearchpython import VideosSearch
from youtubesearchpython import SearchVideos
import re
from pykeyboard import InlineKeyboard
from pyrogram.enums import ChatAction
from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaAudio,
                            InputMediaVideo, Message)

###### INSTAGRAM REELS DOWNLOAD

@app.on_message(filters.command(["ig"], ["/", "!", "."]))
async def download_instareels(c: app, m: Message):
    try:
        reel_ = m.command[1]
    except IndexError:
        await m.reply_text("ɢɪᴠᴇ ᴍᴇ ᴀɴ ʟɪɴᴋ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ɪᴛ...")
        return
    if not reel_.startswith("https://www.instagram.com/reel/"):
        await m.reply_text("ɪɴ ᴏʀᴅᴇʀ ᴛᴏ ᴏʙᴛᴀɪɴ ᴛʜᴇ ʀᴇQᴜᴇꜱᴛᴇᴅ ʀᴇᴇʟ, ᴀ ᴠᴀʟɪᴅ ʟɪɴᴋ ɪꜱ ɴᴇᴄᴇꜱꜱᴀʀʏ. ᴋɪɴᴅʟʏ ᴘʀᴏᴠɪᴅᴇ ᴍᴇ ᴡɪᴛʜ ᴛʜᴇ ʀᴇQᴜɪʀᴇᴅ ʟɪɴᴋ.")
        return
    OwO = reel_.split(".",1)
    Reel_ = ".dd".join(OwO)
    try:
        await m.reply_video(Reel_)
        return
    except Exception:
        try:
            await m.reply_photo(Reel_)
            return
        except Exception:
            try:
                await m.reply_document(Reel_)
                return
            except Exception:
                await m.reply_text("ɪ ᴀᴍ ᴜɴᴀʙʟᴇ ᴛᴏ ʀᴇᴀᴄʜ ᴛᴏ ᴛʜɪꜱ ʀᴇᴇʟ.")

@app.on_message(filters.command(["reel"], ["/", "!", "."]))
async def instagram_reel(client, message):
    if len(message.command) == 2:
        url = message.command[1]
        response = requests.post(f"https://lexica-api.vercel.app/download/instagram?url={url}")
        data = response.json()

        if data['code'] == 2:
            media_urls = data['content']['mediaUrls']
            if media_urls:
                video_url = media_urls[0]['url']
                await message.reply_video(f"{video_url}")
            else:
                await message.reply("ɴᴏ ᴠɪᴅᴇᴏ ꜰᴏᴜɴᴅ ɪɴ ᴛʜᴇ ʀᴇꜱᴘᴏɴꜱᴇ. ᴍᴀʏ ʙᴇ ᴀᴄᴄᴏᴜɴᴛʙɪꜱ ᴘʀɪᴠᴀᴛᴇ.")
        else:
            await message.reply("ʀᴇQᴜᴇꜱᴛ ᴡᴀꜱ ɴᴏᴛ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ.")
    else:
        await message.reply("ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ɪɴꜱᴛᴀɢʀᴀᴍ ᴜʀʟ ᴜꜱɪɴɢ ᴛʜᴇ /ʀᴇᴇʟꜱ ᴄᴏᴍᴍᴀɴᴅ.")
