import asyncio
from config import Config
import pyrogram
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from typing import List, Union  # Import List and Union


async def ForceSub(c: Client, m: Message):
    """
    Force users to subscribe to one or more channels before using the bot.
    """

    if not Config.UPDATES_CHANNEL:
        return 200  # No force_sub channel(s) specified

    channels: List[Union[str, int]] = Config.UPDATES_CHANNEL  # Expect a list in Config
    if not isinstance(channels, list):
        channels = [channels]  # Ensure it's a list

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
                print(f"Uɴᴀʙʟᴇ ᴛᴏ ᴅᴏ ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ᴛᴏ {channel_id}\n\nError: {err}")
                return 200  # Or handle this differently

            try:
                user = await c.get_chat_member(chat_id=channel_id, user_id=user_id)
                if user.status == "kicked":
                    await c.send_message(
                        chat_id=user_id,
                        text="Sᴏʀʀʏ sɪʀ, ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ ɪɴ ᴏɴᴇ ᴏʀ ᴍᴏʀᴇ ᴄʜᴀɴɴᴇʟs. Cᴏɴᴛᴀᴄᴛ ᴍʏ ᴀᴅᴍɪɴ.",
                        disable_web_page_preview=True,
                        parse_mode="Markdown",
                    )
                    return 400
            except UserNotParticipant:
                all_subscribed = False
                join_buttons.append(InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=invite_link.invite_link))
            except Exception as e:
                print(f"Error checking channel {channel_id}: {e}")
                await c.send_message(
                    chat_id=user_id,
                    text="Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ. Cᴏɴᴛᴀᴄᴛ ᴍʏ ᴀᴅᴍɪɴ.",
                    disable_web_page_preview=True,
                    parse_mode="Markdown",
                )
                return 400
        except Exception as e:
            print(f"Error processing channel {channel_id}: {e}")
            return 400

    if all_subscribed:
        return 200
    else:
        keyboard_rows = [join_buttons[i:i + 2] for i in range(0, len(join_buttons), 2)]
        keyboard_rows.append([InlineKeyboardButton("↻ Tʀʏ Aɢᴀɪɴ", url=Config.BOT_START_LINK)]) # Use Config var

        await c.send_message(
            chat_id=user_id,
            text="**Pʟᴇᴀsᴇ ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟs ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ!**\n\n Oɴʟʏ ᴄʜᴀɴɴᴇʟ sᴜʙsᴄʀɪʙᴇʀs ᴄᴀɴ ᴜsᴇ ᴛʜᴇ ʙᴏᴛ!",
            reply_markup=InlineKeyboardMarkup(keyboard_rows)
        )
        return 400
