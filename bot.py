# ================= CONFIG =================

import json
import asyncio
import time
import random
import logging
import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
    CommandHandler,
    CallbackQueryHandler
)

BOT_TOKEN = "8873480138:AAEYCP_Tbvo3blS9uOS5OOxz01uO6REOm3k"

OWNER_ID = 8722144519

BOT_USERNAME = "@Newmuteauto_bot"

MASTER_USERNAME = "@ll_DARK_GETO_ll"

HOME_LINK = "https://t.me/+Yu4K5-9LHH1mM2Zl"

PHOTO_URL = "https://ibb.co/Fqg7q2Hf"

DATA_FILE = "data.json"

# ================= LOGGING =================

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

SPAM_RUNNING = {}

# ================= DATA =================

def load_data():

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    except:

        data = {
            "sudo_users": [],
            "mute_delete": [],
            "stickers": []
        }

        save_data(data)

        return data


def save_data(data):

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ================= UTILS =================

def is_sudo(uid, data):

    return (
        uid == OWNER_ID or
        uid in data["sudo_users"]
    )


def get_mention(user):

    if user.username:
        return f"@{user.username}"

    return user.first_name

# ================= START =================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    buttons = [

        [
            InlineKeyboardButton(
                "➕ Add Me Your Group",
                url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
            )
        ],

        [
            InlineKeyboardButton(
                "📚 Help",
                callback_data="help"
            ),

            InlineKeyboardButton(
                "🏠 My Home",
                url=HOME_LINK
            )
        ],

        [
            InlineKeyboardButton(
                "👑 My Master",
                url=f"https://t.me/{MASTER_USERNAME}"
            )
        ]
    ]

    text = f"""
✨ Welcome To My Bot ✨

⚡ Fast • Stable • Powerful

👑 Master: @{MASTER_USERNAME}

Only sudo users can use admin commands.

Click Buttons Below 👇
"""

    await update.message.reply_photo(
        photo=PHOTO_URL,
        caption=text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ================= BUTTON =================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    if query.data == "help":

        txt = """
📚 COMMANDS

.ping
.speed
.info

Reply User:
.mute
.unmute
.ban

Owner Only:
.addsudo
.delsudo
.addsticker

Reply Sticker:
.addsticker

.sticker 5

Spam:
.spam 10
.stopspam
"""

        buttons = [
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="back"
                )
            ]
        ]

        await query.message.edit_caption(
            caption=txt,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif query.data == "back":

        buttons = [

            [
                InlineKeyboardButton(
                    "➕ Add Me Your Group",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
                )
            ],

            [
                InlineKeyboardButton(
                    "📚 Help",
                    callback_data="help"
                ),

                InlineKeyboardButton(
                    "🏠 My Home",
                    url=HOME_LINK
                )
            ],

            [
                InlineKeyboardButton(
                    "👑 My Master",
                    url=f"https://t.me/{MASTER_USERNAME}"
                )
            ]
        ]

        await query.message.edit_caption(
            caption=f"""
✨ Welcome To My Bot ✨

⚡ Fast • Stable • Powerful

👑 Master: @{MASTER_USERNAME}

Only sudo users can use admin commands.

Click Buttons Below 👇
""",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

# ================= AUTO DELETE =================

async def auto_delete(update, context, data):

    msg = update.message

    if not msg or not msg.from_user:
        return

    uid = msg.from_user.id

    if uid in data["mute_delete"]:

        try:
            await msg.delete()

        except:
            pass

# ================= MAIN HANDLER =================

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.message

    if not msg:
        return

    data = load_data()

    uid = msg.from_user.id

    chat_id = msg.chat.id

    txt = msg.text.lower().strip() if msg.text else ""

    target = (
        msg.reply_to_message.from_user
        if msg.reply_to_message else None
    )

    await auto_delete(update, context, data)

    # ================= PING =================

    if txt == ".ping" or txt == ".speed":

        start = time.time()

        m = await msg.reply_text("⚡ Checking speed...")

        end = time.time()

        speed = round((end - start) * 1000)

        await m.edit_text(
            f"⚡ Bot Speed: {speed} ms"
        )

        return

    # ================= INFO =================

    if txt == ".info":

        if not target:

            await msg.reply_text(
                "Reply to a user with .info"
            )

            return

        user = target

        user_id = user.id

        first_name = user.first_name or "None"

        last_name = user.last_name or "None"

        username = (
            f"@{user.username}"
            if user.username else "None"
        )

        is_bot = user.is_bot

        language = getattr(user, "language_code", "Unknown")

        profile_link = f"tg://user?id={user_id}"

        text_info = f"""
👤 USER INFO

🆔 User ID: `{user_id}`
👤 First Name: {first_name}
👥 Last Name: {last_name}
🔗 Username: {username}
🤖 Bot: {is_bot}
🌐 Language: {language}
📎 Profile: {profile_link}
"""

        try:

            photos = await context.bot.get_user_profile_photos(
                user_id,
                limit=1
            )

            if photos.total_count > 0:

                photo = photos.photos[0][-1].file_id

                await msg.reply_photo(
                    photo=photo,
                    caption=text_info,
                    parse_mode="Markdown"
                )

            else:

                await msg.reply_text(
                    text_info,
                    parse_mode="Markdown"
                )

        except:

            await msg.reply_text(
                text_info,
                parse_mode="Markdown"
            )

        return

    # ================= MUTE =================

    if txt == ".mute" and target and is_sudo(uid, data):

        if target.id not in data["mute_delete"]:

            data["mute_delete"].append(target.id)

            save_data(data)

        await msg.reply_text(
            f"{get_mention(target)} muted!"
        )

        return

    # ================= UNMUTE =================

    if txt == ".unmute" and target and is_sudo(uid, data):

        if target.id in data["mute_delete"]:

            data["mute_delete"].remove(target.id)

            save_data(data)

        await msg.reply_text(
            f"{get_mention(target)} unmuted!"
        )

        return

    # ================= BAN =================

    if txt == ".ban" and target and is_sudo(uid, data):

        try:

            await context.bot.ban_chat_member(
                chat_id,
                target.id
            )

            await msg.reply_text(
                f"{get_mention(target)} banned!"
            )

        except Exception as e:

            await msg.reply_text(
                f"Error: {e}"
            )

        return

    # ================= ADD STICKER =================

    if txt == ".addsticker" and uid == OWNER_ID:

        if (
            msg.reply_to_message and
            msg.reply_to_message.sticker
        ):

            sticker_id = (
                msg.reply_to_message.sticker.file_id
            )

            if sticker_id not in data["stickers"]:

                data["stickers"].append(sticker_id)

                save_data(data)

            await msg.reply_text(
                "✅ Sticker saved!"
            )

        else:

            await msg.reply_text(
                "Reply sticker first"
            )

        return

    # ================= SEND STICKERS =================

    if txt.startswith(".sticker"):

        try:

            count = int(txt.split(" ")[1])

        except:

            count = 1

        stickers = data["stickers"]

        if not stickers:

            await msg.reply_text(
                "No stickers saved"
            )

            return

        for i in range(count):

            sticker = random.choice(stickers)

            await context.bot.send_sticker(
                chat_id,
                sticker
            )

            await asyncio.sleep(0.3)

        return

    # ================= ADD SUDO =================

    if txt == ".addsudo" and target and uid == OWNER_ID:

        if target.id not in data["sudo_users"]:

            data["sudo_users"].append(target.id)

            save_data(data)

        await msg.reply_text(
            f"{get_mention(target)} added as sudo"
        )

        return

    # ================= DEL SUDO =================

    if txt == ".delsudo" and target and uid == OWNER_ID:

        if target.id in data["sudo_users"]:

            data["sudo_users"].remove(target.id)

            save_data(data)

        await msg.reply_text(
            f"{get_mention(target)} removed from sudo"
        )

        return

    # ================= SPAM =================

    if txt.startswith(".spam") and is_sudo(uid, data):

        if not target:

            await msg.reply_text(
                "Reply user with .spam 10"
            )

            return

        try:

            count = int(txt.split(" ")[1])

        except:

            await msg.reply_text(
                "Usage: .spam 10"
            )

            return

        SPAM_RUNNING[chat_id] = True

        mention_text = (
            f"[{target.first_name}](tg://user?id={target.id})"
        )

        for i in range(count):

            if not SPAM_RUNNING.get(chat_id):

                break

            await context.bot.send_message(
                chat_id,
                mention_text,
                parse_mode="Markdown"
            )

            await asyncio.sleep(0.4)

        SPAM_RUNNING[chat_id] = False

        return

    # ================= STOP SPAM =================

    if txt == ".stopspam" and is_sudo(uid, data):

        SPAM_RUNNING[chat_id] = False

        await msg.reply_text(
            "✅ Spam stopped"
        )

        return

# ================= MAIN =================

def main():

    print("Bot running!")

    app = Application.builder().token(
        BOT_TOKEN
    ).build()

    app.add_handler(
        CommandHandler(
            "start",
            start_command
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    app.add_handler(
        MessageHandler(
            filters.ALL,
            handler
        )
    )

    app.run_polling(
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
