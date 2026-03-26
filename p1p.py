import random
import string
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8479108013:AAEnntKsp2VHgke7_PvNx7oB-6V6WMjAlkQ"

channels = [
    {"name": "Channel 1", "id": -1003779626687, "link": "https://t.me/+9kE0KnkLKMNkMDhl"},
    {"name": "Channel 2", "id": -1003784798023, "link": "https://t.me/+N3-w5dHnc7U1MDI1"}
]

IMAGE_URL = "https://files.catbox.moe/wcfmqd.jpg"

# 🔥 Fake Web Server (PORT FIX)
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_web():
    import os
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

# 🔑 Key Generator
def generate_key():
    return "DARK-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# 🚀 Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 Join Channel 1", url=channels[0]["link"])],
        [InlineKeyboardButton("🔥 Join Channel 2", url=channels[1]["link"])],
        [InlineKeyboardButton("✅ VERIFY", callback_data="verify")]
    ]

    await update.message.reply_photo(
        photo=IMAGE_URL,
        caption="👻 Sab channels join karo phir VERIFY dabao",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ✅ Verify सिस्टम (FAST + NO ERROR)
async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

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
        await query.message.reply_text(f"❌ Join first: {', '.join(not_joined)}")
        return

    key = generate_key()

    await query.message.reply_text(
        f"✅ VERIFIED!\n\n🔑 KEY:\n`{key}`",
        parse_mode="Markdown"
    )

# 🤖 BOT START
def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify_callback, pattern="verify"))

    print("Bot Running...")
    app.run_polling(drop_pending_updates=True)

# 🔥 RUN BOTH (WEB + BOT)
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    run_bot()
