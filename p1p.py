import random
import asyncio
import time
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8479108013:AAEnntKsp2VHgke7_PvNx7oB-6V6WMjAlkQ"

channels = [
    {"name": "Channel 1", "id": -1003779626687, "link": "https://t.me/+9kE0KnkLKMNkMDhl"},
    {"name": "Channel 2", "id": -1003784798023, "link": "https://t.me/+N3-w5dHnc7U1MDI1"},
    {"name": "Channel 3", "id": -1002785963969, "link": "https://t.me/+01WJ0dy3rKI1NzFl"},
    {"name": "Channel 4", "id": -1002974901382, "link": "https://t.me/+jm2ZY3HZYYA5ODk1"},
    {"name": "Channel 5", "id": -1002768798055, "link": "https://t.me/+L0gRJO18rEQ4MmJl"},
    {"name": "Channel 6", "id": -1003293078621, "link": "https://t.me/+y5nC2bNQfrUyNWVl"},
    {"name": "Channel 7", "id": -1003220631921, "link": "https://t.me/+AkhiQEjHiwo3NGRl"},
    {"name": "Channel 8", "id": -1003569342555, "link": "https://t.me/+5B4wsdDjD_czZjQ1"},
]

IMAGE_URL = "https://files.catbox.moe/wcfmqd.jpg"

# 🔥 DATABASE (RAM)
user_keys = {}

# 🔑 KEY GENERATOR
def generate_key():
    return str(random.randint(1000000000, 9999999999))

# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for ch in channels:
        keyboard.append([InlineKeyboardButton(f"Join {ch['name']} 🔥", url=ch["link"])])
    keyboard.append([InlineKeyboardButton("✅ VERIFY", callback_data="verify")])

    await update.message.reply_photo(
        photo=IMAGE_URL,
        caption="""
𝗛𝗲𝗹𝗹𝗼 𝗨𝘀𝗲𝗿 👻 𝐁𝐎𝐓

𝗔𝗟𝗟 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 𝗝𝗢𝗜𝗡 🥰

👻 Sab channels join karo phir VERIFY dabao

𝐇𝐎𝐖 𝐓𝐎 𝐆𝐄𝐍𝐄𝐑𝐀𝐓𝐄 𝐊𝐄𝐘 💀
<a href="https://t.me/setupchanel_0/60">𝐂𝐋𝐈𝐂𝐊 𝐇𝐄𝐑𝐄</a>
""",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ⚡ VERIFY
async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # 🔍 JOIN CHECK
    async def check(ch):
        try:
            member = await context.bot.get_chat_member(ch["id"], user_id)
            if member.status in ["left", "kicked"]:
                return ch["name"]
        except:
            return ch["name"]
        return None

    results = await asyncio.gather(*[check(ch) for ch in channels])
    not_joined = [r for r in results if r]

    if not_joined:
        await query.message.reply_text(
            f"❌ Pehle join karo:\n{', '.join(not_joined)}"
        )
        return

    # 🔐 CHECK EXISTING KEY
    current_time = time.time()

    if user_id in user_keys:
        key_data = user_keys[user_id]
        # 24 hours = 86400 sec
        if current_time - key_data["time"] < 86400:
            await query.message.reply_text(
                f"""
⚠️ Tumhari key already bani hai

🔑 Key - {key_data["key"]}

⏳ Valid for 24 hours
"""
            )
            return

    # 🔑 NEW KEY
    key = generate_key()

    user_keys[user_id] = {
        "key": key,
        "time": current_time
    }

    await query.message.reply_text(
        f"""
🔑 Key - {key}

📥 DRIP SCINET APK:
https://www.mediafire.com/file/if3uvvwjbj87lo2/DRIPCLIENT_v6.2_GLOBAL_AP.apks/file

⚠️ APK open karne ke baad ye join karo:
https://t.me/+MkNcxGuk-w43MzBl

⏳ Key valid: 24 hours
"""
    )

# 🚀 RUN
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(verify_callback, pattern="verify"))

print("PRO Bot Running...")
app.run_polling(drop_pending_updates=True)
