import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from openai import OpenAI
from gtts import gTTS
# =====================================
# GROQ AI CLIENT
# =====================================

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# =====================================
# TELEGRAM BOT TOKEN
# =====================================

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# =====================================
# START COMMAND
# =====================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Hello. I am Shubh AI. Your futuristic assistant is online."
    )

# =====================================
# AI CHAT FUNCTION
# =====================================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": "You are Shubh AI, a futuristic assistant like Jarvis. Speak smartly and naturally."
                },

                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        answer = response.choices[0].message.content

        # SEND TEXT REPLY
        await update.message.reply_text(answer)

        # CONVERT TO VOICE
        tts = gTTS(text=answer, lang='en')

        audio_file = "reply.mp3"

        tts.save(audio_file)

        # SEND VOICE MESSAGE
        with open(audio_file, 'rb') as voice:

            await update.message.reply_voice(voice)

    except Exception as e:

        print(e)

        await update.message.reply_text(
            "Error happened while contacting AI."
        )

# =====================================
# MAIN BOT
# =====================================

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
)

print("Shubh GROQ AI Bot Running...")

app.run_polling()