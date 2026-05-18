import json
import asyncio
import time
import random
import logging

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

BOT_TOKEN = "8734837398:AAFoSnyZYQx8pD-huYgAc3XNG_nYaB5mvVY"
OWNER_ID = 8722144519
DATA_FILE = "data.json"

# ================= START PANEL =================

BOT_USERNAME = "@Miyamuramusic_bot"

HOME_LINK = "https://t.me/+Yu4K5-9LHH1mM2Zl"

PHOTO_URL = "AQADaxJrG3fwYFR-"

# ================= LOGGING =================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

log = logging.getLogger(__name__)

SPAM_RUNNING = {}

# ================= DATA =================

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)

    except:
        data = {
            "sudo_users": [],
            "mute_delete": [],
            "tmute": {},
            "stickers": [],
            "shayari": {
                "love": [],
                "sad": [],
                "birthday": []
            }
        }

        save_data(data)

        return data


def save_data(data):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    except:
        pass

# ================= UTILS =================

def is_sudo(uid, data):
    return uid == OWNER_ID or uid in data.get("sudo_users", [])


def get_mention(user):

    try:
        if user.username:
            return "@" + user.username

        return user.first_name or "User"

    except:
        return "User"

# ================= START =================

async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    buttons = [

        [
            InlineKeyboardButton(
                "➕ Add Me Group",
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
        ]
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    caption = """
✨ Welcome To My Bot ✨

⚡ Fast • Stable • Powerful

Click Buttons Below 👇
"""

    await update.message.reply_photo(
        photo=PHOTO_URL,
        caption=caption,
        reply_markup=keyboard
    )

# ================= BUTTONS =================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if query.data == "help":

        help_text = """
📚 BOT COMMANDS

.alive
.ping

.spam 5 hello
.spamstop

Reply User:
.mute
.unmute
.tmute 60

Owner:
.addsudo
.sudolist
.mutelist
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
            caption=help_text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif query.data == "back":

        buttons = [

            [
                InlineKeyboardButton(
                    "➕ Add Me Group",
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
            ]
        ]

        await query.message.edit_caption(
            caption="""
✨ Welcome To My Bot ✨

⚡ Fast • Stable • Powerful

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

    if uid == OWNER_ID or is_sudo(uid, data):
        return

    if uid in data["mute_delete"]:

        try:
            await msg.delete()

        except:
            pass

# ================= MAIN HANDLER =================

async def handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    global SPAM_RUNNING

    msg = update.message

    if not msg:
        return

    data = load_data()

    uid = msg.from_user.id if msg.from_user else 0

    chat_id = msg.chat.id

    txt = msg.text.lower().strip() if msg.text else ""

    target = (
        msg.reply_to_message.from_user
        if msg.reply_to_message else None
    )

    await auto_delete(update, context, data)

    # ================= BASIC =================

    if txt == ".alive":

        await msg.reply_text("✅ Online")

        return

    if txt == ".ping":

        await msg.reply_text("🏓 PONG!")

        return

    # ================= SPAM =================

    if txt == ".spamstop":

        SPAM_RUNNING[chat_id] = False

        await msg.reply_text("✅ Stopped!")

        return

    if txt.startswith(".spam ") and is_sudo(uid, data):

        try:
            parts = txt.split(" ", 2)

            count = int(parts[1])

            text = parts[2]

            SPAM_RUNNING[chat_id] = True

            for i in range(count):

                if not SPAM_RUNNING.get(chat_id):
                    break

                await context.bot.send_message(
                    chat_id,
                    text
                )

                await asyncio.sleep(0.5)

            SPAM_RUNNING[chat_id] = False

        except:

            await msg.reply_text(
                ".spam 10 hello"
            )

        return

    # ================= MUTE =================

    if txt == ".mute" and target and is_sudo(uid, data):

        if target.id not in data["mute_delete"]:

            data["mute_delete"].append(target.id)

            save_data(data)

        await msg.reply_text(
            get_mention(target) + " muted!"
        )

        return

    if txt == ".unmute" and target and is_sudo(uid, data):

        if target.id in data["mute_delete"]:

            data["mute_delete"].remove(target.id)

            save_data(data)

        await msg.reply_text(
            get_mention(target) + " unmuted!"
        )

        return

    # ================= EVERYONE =================

    if txt == ".everyone" and is_sudo(uid, data):

        await msg.reply_text("@everyone")

        return

    # ================= OWNER =================

    if uid == OWNER_ID:

        if txt == ".sudolist":

            slist = (
                "Sudo: " +
                ", ".join(map(str, data["sudo_users"]))
            )

            await msg.reply_text(slist or "Empty")

            return

        if txt == ".mutelist":

            mlist = (
                "Mute: " +
                ", ".join(map(str, data["mute_delete"]))
            )

            await msg.reply_text(mlist or "Empty")

            return

        if txt == ".addsudo" and target:

            if target.id not in data["sudo_users"]:

                data["sudo_users"].append(target.id)

                save_data(data)

            await msg.reply_text(
                get_mention(target) + " sudo added"
            )

            return

# ================= MAIN =================

def main():

    print("Starting bot...")

    app = Application.builder().token(
        BOT_TOKEN
    ).build()

    # Start Panel
    app.add_handler(
        CommandHandler(
            "start",
            start_command
        )
    )

    # Buttons
    app.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    # Main Handler
    app.add_handler(
        MessageHandler(
            filters.ALL,
            handler
        )
    )

    print("Bot running!")

    app.run_polling(
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
