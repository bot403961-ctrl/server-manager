import telebot, requests, os, time

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))
GEMINI_KEY = os.environ.get("GEMINI_KEY", "")

GEMINI_MODELS = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3-flash-preview",
    "gemini-flash-lite-latest",
]

bot = telebot.TeleBot(BOT_TOKEN)

def chat_ai(text):
    for model in GEMINI_MODELS:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            r = requests.post(url,
                headers={"x-goog-api-key": GEMINI_KEY, "Content-Type": "application/json"},
                json={"contents": [{"parts": [{"text": text}]}]},
                timeout=20)

            data = r.json()
            if "candidates" in data:
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except:
            continue
    return "⚠️ Google مشغولة — جرب بعد شوية"

@bot.message_handler(func=lambda m: True)
def handle(message):
    if message.from_user.id != ADMIN_ID:
        return
    bot.send_chat_action(message.chat.id, 'typing')
    reply = chat_ai(message.text)
    bot.reply_to(message, reply)

print("🤖 شغال")
bot.infinity_polling()
