# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import math
import time
import asyncio
import pyrogram
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message 
from config import API_ID, API_HASH, ERROR_MESSAGE, DEST_CHANNEL_ID
from database.db import db
from TechVJ.strings import HELP_TXT


class batch_temp(object):
    IS_BATCH = {}


# ---------------- PROGRESS UTILS ---------------- #

def humanbytes(size):
    if not size:
        return "0B"
    power = 1024
    n = 0
    Dic_powerN = {0: '', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return f"{round(size,2)} {Dic_powerN[n]}B"

def time_formatter(seconds: int) -> str:
    result = ""
    v_m = seconds // 60
    v_s = seconds % 60
    v_h = v_m // 60
    v_m = v_m % 60
    if v_h:
        result += f"{v_h}h "
    if v_m:
        result += f"{v_m}m "
    if v_s:
        result += f"{v_s}s"
    return result.strip()

async def progress(current, total, message, start_time, tag):
    now = time.time()
    diff = now - start_time
    if diff == 0:
        diff = 1
    percentage = current * 100 / total
    speed = current / diff
    eta = round((total - current) / speed)

    progress_str = "[{0}{1}]".format(
        ''.join(["█" for i in range(math.floor(percentage / 5))]),
        ''.join(["▒" for i in range(20 - math.floor(percentage / 5))])
    )

    tmp = (
        f"{'📥' if tag=='down' else '📤'} {'Downloading' if tag=='down' else 'Uploading'}\n"
        f"{progress_str} {percentage:.1f}%\n"
        f"{humanbytes(current)} of {humanbytes(total)}\n"
        f"Speed: {humanbytes(speed)}/s | ETA: {time_formatter(eta)}"
    )
    try:
        await message.edit_text(tmp)
    except:
        pass


# ---------------- BOT COMMANDS ---------------- #

@Client.on_message(filters.command(["start"]))
async def send_start(client: Client, message: Message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
    buttons = [[
        InlineKeyboardButton("❣️ Developer", url="https://t.me/kingvj01")
    ], [
        InlineKeyboardButton('🔍 Support Group', url='https://t.me/vj_bot_disscussion'),
        InlineKeyboardButton('🤖 Update Channel', url='https://t.me/vj_botz')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=message.chat.id,
        text=f"<b>👋 Hi {message.from_user.mention}, I am Save Restricted Content Bot, I can send you restricted content by its post link.\n\nFor downloading restricted content /login first.\n\nKnow how to use bot by - /help</b>",
        reply_markup=reply_markup,
        reply_to_message_id=message.id
    )


@Client.on_message(filters.command(["help"]))
async def send_help(client: Client, message: Message):
    await client.send_message(
        chat_id=message.chat.id,
        text=f"{HELP_TXT}"
    )


@Client.on_message(filters.command(["cancel"]))
async def send_cancel(client: Client, message: Message):
    batch_temp.IS_BATCH[message.from_user.id] = True
    await client.send_message(
        chat_id=message.chat.id,
        text="**Batch Successfully Cancelled.**"
    )


# ---------------- MAIN HANDLER ---------------- #

@Client.on_message(filters.text & filters.private)
async def save(client: Client, message: Message):
    if "https://t.me/" in message.text:
        if batch_temp.IS_BATCH.get(message.from_user.id) is False:
            return await message.reply_text("**One Task Is Already Processing. Wait For It To Complete. Use /cancel to stop it.**")

        datas = message.text.split("/")
        temp = datas[-1].replace("?single", "").split("-")
        fromID = int(temp[0].strip())
        try:
            toID = int(temp[1].strip())
        except:
            toID = fromID

        batch_temp.IS_BATCH[message.from_user.id] = False
        for msgid in range(fromID, toID + 1):
            if batch_temp.IS_BATCH.get(message.from_user.id): break
            user_data = await db.get_session(message.from_user.id)
            if not user_data:
                await message.reply("**For Downloading Restricted Content You Have To /login First.**")
                batch_temp.IS_BATCH[message.from_user.id] = True
                return
            try:
                acc = Client("saverestricted", session_string=user_data, api_hash=API_HASH, api_id=API_ID)
                await acc.connect()
            except:
                batch_temp.IS_BATCH[message.from_user.id] = True
                return await message.reply("**Your Login Session Expired. So /logout First Then /login Again.**")

            if "https://t.me/c/" in message.text:
                chatid = int("-100" + datas[4])
                try:
                    await handle_private(client, acc, message, chatid, msgid)
                except Exception as e:
                    if ERROR_MESSAGE:
                        await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)

            elif "https://t.me/b/" in message.text:
                username = datas[4]
                try:
                    await handle_private(client, acc, message, username, msgid)
                except Exception as e:
                    if ERROR_MESSAGE:
                        await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)

            else:
                username = datas[3]
                try:
                    msg = await client.get_messages(username, msgid)
                    await client.copy_message(message.chat.id, msg.chat.id, msg.id, reply_to_message_id=message.id)
                except UsernameNotOccupied:
                    await client.send_message(message.chat.id, "The username is not occupied by anyone", reply_to_message_id=message.id)
                except:
                    try:
                        await handle_private(client, acc, message, username, msgid)
                    except Exception as e:
                        if ERROR_MESSAGE:
                            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)

            await acc.disconnect()
            await asyncio.sleep(10)

        batch_temp.IS_BATCH[message.from_user.id] = True


# ---------------- PRIVATE MESSAGE HANDLER ---------------- #

async def handle_private(client: Client, acc, message: Message, chatid: int, msgid: int):
    msg: Message = await acc.get_messages(chatid, msgid)
    if not msg: return
    msg_type = get_message_type(msg)
    if not msg_type: return
    chat = message.chat.id
    if batch_temp.IS_BATCH.get(message.from_user.id): return

    if msg_type == "Text":
        try:
            await client.send_message(chat, msg.text, entities=msg.entities, reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
            return
        except Exception as e:
            if ERROR_MESSAGE:
                await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
            return

    smsg = await client.send_message(message.chat.id, "📥 Starting Download...", reply_to_message_id=message.id)
    start_time = time.time()
    try:
        file = await acc.download_media(msg, progress=progress, progress_args=[smsg, start_time, "down"])
    except Exception as e:
        if ERROR_MESSAGE:
            await smsg.edit_text(f"❌ Download Error: {e}")
        return

    # upload to user
    start_time = time.time()
    try:
        if msg_type == "Document":
            await client.send_document(chat, file, caption=msg.caption or "", reply_to_message_id=message.id,
                                       progress=progress, progress_args=[smsg, start_time, "up"])
        elif msg_type == "Video":
            await client.send_video(chat, file, caption=msg.caption or "", duration=msg.video.duration if msg.video else 0,
                                    width=msg.video.width if msg.video else 0, height=msg.video.height if msg.video else 0,
                                    reply_to_message_id=message.id, supports_streaming=True,
                                    progress=progress, progress_args=[smsg, start_time, "up"])
        elif msg_type == "Photo":
            await client.send_photo(chat, file, caption=msg.caption or "", reply_to_message_id=message.id,
                                    progress=progress, progress_args=[smsg, start_time, "up"])
        elif msg_type == "Audio":
            await client.send_audio(chat, file, caption=msg.caption or "", duration=msg.audio.duration if msg.audio else 0,
                                    performer=msg.audio.performer if msg.audio else None, title=msg.audio.title if msg.audio else None,
                                    reply_to_message_id=message.id, progress=progress, progress_args=[smsg, start_time, "up"])
        else:
            await client.send_document(chat, file, caption=msg.caption or "", reply_to_message_id=message.id,
                                       progress=progress, progress_args=[smsg, start_time, "up"])
    except Exception as e:
        if ERROR_MESSAGE:
            await smsg.edit_text(f"❌ Upload Error: {e}")
        return

    # ✅ also send to channel (same format as original)
    try:
        if msg_type == "Document":
            await client.send_document(DEST_CHANNEL_ID, file, caption=msg.caption or "")
        elif msg_type == "Video":
            await client.send_video(DEST_CHANNEL_ID, file, caption=msg.caption or "",
                                    duration=msg.video.duration if msg.video else 0,
                                    width=msg.video.width if msg.video else 0,
                                    height=msg.video.height if msg.video else 0,
                                    supports_streaming=True)
        elif msg_type == "Photo":
            await client.send_photo(DEST_CHANNEL_ID, file, caption=msg.caption or "")
        elif msg_type == "Audio":
            await client.send_audio(DEST_CHANNEL_ID, file, caption=msg.caption or "",
                                    duration=msg.audio.duration if msg.audio else 0,
                                    performer=msg.audio.performer if msg.audio else None,
                                    title=msg.audio.title if msg.audio else None)
        else:
            await client.send_document(DEST_CHANNEL_ID, file, caption=msg.caption or "")
    except Exception as e:
        if ERROR_MESSAGE:
            await client.send_message(message.chat.id, f"❌ Error sending to channel: {e}")

    # cleanup
    if os.path.exists(file):
        os.remove(file)
    await smsg.delete()

# ---------------- MESSAGE TYPE DETECTOR ---------------- #

def get_message_type(msg: pyrogram.types.Message):
    if msg.document: return "Document"
    if msg.video: return "Video"
    if msg.animation: return "Animation"
    if msg.sticker: return "Sticker"
    if msg.voice: return "Voice"
    if msg.audio: return "Audio"
    if msg.photo: return "Photo"
    if msg.text: return "Text"
    return None
