import os
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import (
    FloodWait, UserIsBlocked, InputUserDeactivated, UserAlreadyParticipant,
    InviteHashExpired, UsernameNotOccupied
)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import API_ID, API_HASH, ERROR_MESSAGE
from database.db import db

class BatchManager:
    # Task queues for each user
    USER_TASKS = {}

# Worker function to process tasks
async def worker(client, user_id):
    while True:
        if user_id not in BatchManager.USER_TASKS:
            await asyncio.sleep(1)
            continue

        queue = BatchManager.USER_TASKS[user_id]
        if queue.empty():
            await asyncio.sleep(1)
            continue

        # Process task
        task = await queue.get()
        await handle_task(client, user_id, task)

# Handles downloading and uploading tasks
async def handle_task(client, user_id, task):
    chat_id, msg_id, link = task
    try:
        smsg = await client.send_message(chat_id, f"**Processing your request (Message ID: {msg_id})...**")
        
        # Simulate download and upload progress (replace with actual logic)
        progress_file = f"{msg_id}_progress.txt"
        with open(progress_file, "w") as f:
            f.write("0%")
        
        # Simulate download
        await asyncio.sleep(3)
        with open(progress_file, "w") as f:
            f.write("50% Downloaded")
        
        # Simulate upload
        await asyncio.sleep(3)
        with open(progress_file, "w") as f:
            f.write("100% Uploaded")
        
        await client.edit_message_text(chat_id, smsg.id, f"**Message ID {msg_id} processed successfully!**")
        os.remove(progress_file)

    except Exception as e:
        await client.send_message(chat_id, f"Error processing message {msg_id}: {e}")

# Start command
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
        text=f"👋 Hi {message.from_user.mention}, I can help you download restricted content by its link.\n\n"
             f"Use /help to know how to use this bot.",
        reply_markup=reply_markup,
        reply_to_message_id=message.id
    )

# Help command
@Client.on_message(filters.command(["help"]))
async def send_help(client: Client, message: Message):
    await client.send_message(
        chat_id=message.chat.id,
        text=f"Send any restricted content link, and I will download it for you!\n\n"
             f"Commands:\n"
             f"/start - Start the bot\n"
             f"/cancel - Cancel all ongoing tasks\n"
             f"/help - Show this help message"
    )

# Cancel command
@Client.on_message(filters.command(["cancel"]))
async def cancel(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id in BatchManager.USER_TASKS:
        BatchManager.USER_TASKS[user_id] = asyncio.Queue()  # Clear the queue
        await message.reply_text("All tasks have been canceled.")
    else:
        await message.reply_text("No ongoing tasks to cancel.")

# Handles text messages (task creation)
@Client.on_message(filters.text & filters.private)
async def save(client: Client, message: Message):
    user_id = message.from_user.id

    # Initialize task queue for user
    if user_id not in BatchManager.USER_TASKS:
        BatchManager.USER_TASKS[user_id] = asyncio.Queue()
        asyncio.create_task(worker(client, user_id))

    # Add task to the user's queue
    await BatchManager.USER_TASKS[user_id].put((message.chat.id, message.id, message.text))
    await message.reply_text("Your task has been added to the queue.")

# Determines the message type for better handling
def get_message_type(msg: Message):
    if msg.document:
        return "Document"
    elif msg.video:
        return "Video"
    elif msg.photo:
        return "Photo"
    elif msg.audio:
        return "Audio"
    elif msg.voice:
        return "Voice"
    elif msg.text:
        return "Text"
    return None
