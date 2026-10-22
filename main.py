import telebot, requests, os, time

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))
GEMINI_KEY = os.environ.get("GEMINI_KEY", "")

GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-flash-latest",
    "gemini-3.8-flash",
]

bot = telebot.TeleBot(BOT_TOKEN)

SYSTEM_PROMPT = "أنت TAKER — خبير برمجة. رد بالعربي + كود واضح."

def chat_ai(text):
    for model in GEMINI_MODELS:
        for attempt in range(2):
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
                r = requests.post(url,
                    headers={"x-goog-api-key": GEMINI_KEY, "Content-Type": "application/json"},
                    json={
                        "contents": [{"parts": [{"text": text}]}],
                        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
                        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2000}
                    }, timeout=30)
                data = r.json()
                if "candidates" in data:
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                err = data.get('error', {}).get('message', '?')[:60]
                if "rate" in err.lower():
                    time.sleep(2)
                    continue
                break
            except Exception as e:
                print(f"⚠️ {model}: {e}")
                break
    return "⚠️ جرب تاني بعد دقيقة"

@bot.message_handler(func=lambda m: True)
def handle(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "🔒 خاص")
    bot.send_chat_action(message.chat.id, 'typing')
    reply = chat_ai(message.text)
    bot.reply_to(message, reply)

print("🤖 TAKER شغال")
bot.infinity_polling()
