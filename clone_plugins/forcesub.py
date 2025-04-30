from dbusers import clonedb

import json
import os
import asyncio
from config import *
import pyrogram
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from typing import List, Union  # Import List and Union

FORCESUB_FILE = "forcesub.json"

async def load_forcesub_channels():
    data = await clonedb.find_one("forcesub", {"_id": "force_sub_channels"})
    return data["channels"] if data and "channels" in data else []

async def save_forcesub_channels(channels):
    await clonedb.update_one(
        "forcesub",
        {"_id": "force_sub_channels"},
        {"$set": {"channels": channels}},
        upsert=True
    )

async def ForceSub(c: Client, m: Message):
    """
    Force users to subscribe to one or more channels before using the bot.
    """

    channels: List[Union[str, int]] = await load_forcesub_channels()
    if not channels:
        return 200  # No channels set for force-subscribe

    user_id = m.from_user.id
    join_buttons = []
    all_subscribed = True

    for channel_id in channels:
        channel_id = int(channel_id) if isinstance(channel_id, str) and channel_id.startswith("-100") else channel_id
        try:
            try:
                invite_link = await c.create_chat_invite_link(chat_id=channel_id)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                invite_link = await c.create_chat_invite_link(chat_id=channel_id)
            except Exception as err:
                print(f"Failed to create invite link for {channel_id}\nError: {err}")
                return 200

            try:
                user = await c.get_chat_member(chat_id=channel_id, user_id=user_id)
                if user.status == "kicked":
                    await c.send_message(
                        chat_id=user_id,
                        text="You are banned from one or more required channels. Contact the admin.",
                        disable_web_page_preview=True,
                        parse_mode="Markdown",
                    )
                    return 400
            except UserNotParticipant:
                all_subscribed = False
                join_buttons.append(
                    InlineKeyboardButton("Join Channel", url=invite_link.invite_link)
                )
            except Exception as e:
                print(f"Error checking membership for {channel_id}: {e}")
                await c.send_message(
                    chat_id=user_id,
                    text="Something went wrong. Please contact the admin.",
                    disable_web_page_preview=True,
                    parse_mode="Markdown",
                )
                return 400
        except Exception as e:
            print(f"Unexpected error: {e}")
            return 400

    if all_subscribed:
        return 200
    else:
        keyboard_rows = [join_buttons[i:i + 2] for i in range(0, len(join_buttons), 2)]
        keyboard_rows.append([
            InlineKeyboardButton("↻ Try Again", url=BOT_START_LINK)  # You must define BOT_START_LINK in config
        ])

        await c.send_message(
            chat_id=user_id,
            text="**Please join the required update channel(s) to use this bot!**",
            reply_markup=InlineKeyboardMarkup(keyboard_rows)
        )
        return 400
