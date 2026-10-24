import telebot, requests, os, time

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))
GEMINI_KEY = os.environ.get("GEMINI_KEY", "")

# الأقوى → الأضعف
MODELS = [
    "gemini-3.6-flash",
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.5-flash",
    "gemini-3-flash-preview",
    "gemini-3.1-pro-preview",
]

bot = telebot.TeleBot(BOT_TOKEN)

SYSTEM_PROMPT = "أنت TAKER — خبير برمجة. رد بالعربي + كود واضح."

def chat_ai(text):
    for model in MODELS:
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

                err = data.get("error", {}).get("message", "?")[:60]
                print(f"⚠️ {model}: {err}")
                if "429" in str(data.get("error", {}).get("code", "")) or "rate" in err.lower():
                    time.sleep(2)
                    continue
                break
            except Exception as e:
                print(f"⚠️ {model}: {e}")
                break

    return "⚠️ جرب تاني"

@bot.message_handler(func=lambda m: True)
def handle(message):
    if message.from_user.id != ADMIN_ID:
        return
    bot.send_chat_action(message.chat.id, 'typing')
    reply = chat_ai(message.text)
    bot.reply_to(message, reply)

print("🤖 TAKER شغال")
bot.infinity_polling()
