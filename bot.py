from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters, CommandHandler
import os
import re
import random
from datetime import time
from zoneinfo import ZoneInfo

TOKEN = os.getenv("TOKEN")

BOT_PAUSED = False
MORNING_PAUSED = False

async def pause_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BOT_PAUSED
    BOT_PAUSED = True
    await update.message.reply_text("Замовкаю")

async def resume_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BOT_PAUSED
    BOT_PAUSED = False
    await update.message.reply_text("Балакаю")

async def morning_pause_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global MORNING_PAUSED
    MORNING_PAUSED = True
    await update.message.reply_text("Ранкове привітання off")

async def morning_resume_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global MORNING_PAUSED
    MORNING_PAUSED = False
    await update.message.reply_text("Ранкове привітанна on")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Самі собі поможіть 🙄\n\n"
        "Ладно, жартую, я ж норм бот \n"
        "Що роблю:\n"
        "- нормально реагую на 'норм'\n"
        "- реагую, коли нормально кличуть: @norm_again_bot\n"
        "- кола краще пепсі\n"
        "- бити дітей не норм\n"
        "/help - показати це повідомлення"
    )

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Хааай 👋\n"
        "Я норм бот\n\n"
        "Я існую щоб вирішувати — норм чи не норм\n\n"
        "Напиши мені:\n"
        "- 'норм'\n"
        "- чи пепсі краще коли\n"
        "- можеш мене тегнути @norm_again_bot\n"
        "Якщо нічого неясно — /help"
    )
    
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text is None:
        return

    if BOT_PAUSED:
        return
    
    text = update.message.text.lower()

    def send_norm():
        if random.random() < 0.65:
            return "Норм"

        rare_answers = [
            "Нормас",
            "Не норм... А, ні\nНорм",
            "Та норм норм",
            "Абсолютно норм",
            "Сертифіковано як норм ✅",
            "Точно норм",
            "Норм++",
            "Норм, 10/10",
            "Норм, зуб даю",
            "Норм\nБез питань",
            "Мега норм",
            "Перевірила, норм",
            "На 100% норм",
            "Ну і що ти хочеш почути? Норм"
        ]
        return random.choice(rare_answers)

    # не реагує на себе
    if update.message.from_user.id == context.bot.id:
        return

    # згадка бота
    if "@norm_again_bot" in text:
        answers = [
            "Шо?",
            "Ну ну?",
            "Шо треба?",
            "Я тут",
            "Кажи",
            "Так?",
            "Хто кликав?",
            "Слухаю",
            "Мене?",
            "Норм чи не норм?",
            "На зв'язку",
            "Га?"
        ]
        await update.message.reply_text(random.choice(answers))
        return

    # reply на бота + дякую
    if update.message.reply_to_message:
        replied_to_bot = update.message.reply_to_message.from_user.id == context.bot.id

        if replied_to_bot:
            thanks_words = [
                "дякую", "дяк", "спасибі", "спс", "thanks", "thx", "дяки", "дяка", "спасибо"
            ]

            if any(word in text for word in thanks_words):
                answers = [
                    "Прошу",
                    "Будь ласка",
                    "На здоров'я",
                    "Бо то є база",
                    "Завжди рада допомогти",
                    "Звертайся"
                ]
                await update.message.reply_text(random.choice(answers))
                return

            if re.search(r"(?<!\w)норм(?!\w)", text):
                await update.message.reply_text(send_norm())
                return

    # токсичні слова
    toxic_words = [
        "підорас", "пидорас", "бити дітей", "російський реп",
        "геї підораси", "геи пидарасы", "пирадас", "пидарасы",
        "педик", "пєдік", "педік",
        "гомофоб", "гомофобія", "гомофобия", "підар"
    ]

    if any(word in text for word in toxic_words):
        await update.message.reply_text("Не норм.")
        return

    # Coca-Cola > Pepsi → Норм
    cola_better = (
        "кола краще пепсі" in text
        or "кока кола краще пепсі" in text
        or "кока-кола краще пепсі" in text
        or "coca cola better than pepsi" in text
        or "coca-cola better than pepsi" in text
    )

    if cola_better:
        await update.message.reply_text(send_norm())
        return

    # Pepsi погано
    pepsi_bad = (
        "пепсі краще" in text
        or "пепси краще" in text
        or "пепси лучше" in text
        or "pepsi better" in text
        or "pepsi is better" in text
        or "пепсі топ" in text
        or "пепси топ" in text
        or "пепсі найкраща" in text
        or "пепси найкраща" in text
    )

    if pepsi_bad:
        await update.message.reply_text("Не норм.")
        return

    # кола вибір
    has_cola = ("кол" in text or "кока" in text or "cola" in text or "coca" in text)

    asks_choice = any(word in text for word in [
        "яку", "яка", "який", "які",
        "купити", "взяти", "обрати", "вибрати",
        "порадь", "порадьте", "рекомендуєш",
        "краща", "найкраща", "топ"
    ])

    if has_cola and asks_choice:
        await update.message.reply_text("Кокакола нормаааль")
        return

    # норм
    if re.search(r"(?<!\w)норм(?!\w)", text):
        await update.message.reply_text(send_norm())
        return
        
# повідомлення о 7:00
async def morning_message(context: ContextTypes.DEFAULT_TYPE):
    if MORNING_PAUSED:
        return
    chat_id = -5458919378
    await context.bot.send_message(
        chat_id=chat_id,
        text="Всім нормального ранку 👋"
    )
async def pause_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BOT_PAUSED

    if BOT_PAUSED:
        await update.message.reply_text("Я і так мовчу")
        return

    BOT_PAUSED = True
    await update.message.reply_text("Замовкаю")

async def resume_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BOT_PAUSED

    if not BOT_PAUSED:
        await update.message.reply_text("Я і так балакаю")
        return

    BOT_PAUSED = False
    await update.message.reply_text("Балакаю")
    
app = Application.builder().token(TOKEN).build()

# звичайні повідомлення
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("start", start_cmd))
# планування
app.job_queue.run_daily(
    morning_message,
    time=time(hour=7, minute=0, tzinfo=ZoneInfo("Europe/Kyiv"))
)
app.add_handler(CommandHandler("pause", pause_cmd))
app.add_handler(CommandHandler("play", resume_cmd))
app.add_handler(CommandHandler("morning_off", morning_pause_cmd))
app.add_handler(CommandHandler("morning_on", morning_resume_cmd))

app.run_polling()
