"""
    Shazam Telegram Bot
    Copyright (C) 2021 @ImJanindu
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import logging
import ffmpeg
import asyncio
from ShazamAPI import Shazam
from http import post
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from vars import API_ID, API_HASH, BOT_TOKEN

bot = Client(
    "Shazam",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

async def paste(content: str):
    resp = await post(f"{BASE}api/paste", data={"content": content})
    if not resp["status"]:
        return
    return BASE + resp["message"]

@bot.on_message(filters.private & filters.command("shazam"))
async def shazam(_, message):
    if not message.reply_to_message:
       return
    if not message.reply_to_message.audio:
       return
    a = await message.reply_to_message.download()
    
    mp3_file_content_to_recognize = open(a, 'rb').read()
    shazam = Shazam(mp3_file_content_to_recognize)
    recognize_generator = shazam.recognizeSong()
    text = await paste(next(recognize_generator))
    await message.reply(text)
    os.remove(a)

        
bot.start()
idle()    
