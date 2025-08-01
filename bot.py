from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from keep_alive import keep_alive

TOKEN = "8058105739:AAGYQ2goMQqS1KOTaHQ9e6zTIfcTDJv1MiA"
WEBAPP_URL = "https://meltlabz.us/"
CHAT_URL = "https://t.me/MeltLabz"
CONTACT_URL = "https://t.me/MeltLabz"

descriptions = {
    "en": "🔬 MeltLabz brings you the finest modern extracts and authentic verified strains.\nQuality. Transparency. Melt only.",
    "fr": "🔬 MeltLabz sélectionne pour vous les meilleurs extraits modernes, certifiés et traçables.\nQualité. Transparence. Zéro compromis.",
    "es": "🔬 MeltLabz ofrece los mejores extractos modernos, verificados y auténticos.\nCalidad. Confianza. Sólo Melt."
}

buttons = {
    "en": "🧪 See Products",
    "fr": "🧪 Voir les Produits",
    "es": "🧪 Ver Productos"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_animation(chat_id=chat_id, animation="https://meltlabz.us/assets/loader.gif")

    keyboard = [
        [
            InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"),
            InlineKeyboardButton("🇫🇷 Français", callback_data="lang_fr"),
            InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es")
        ]
    ]
    await context.bot.send_message(chat_id=chat_id, text="🌐 Please select your language :", reply_markup=InlineKeyboardMarkup(keyboard))

async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = query.data.split("_")[1]
    text = descriptions.get(lang, descriptions["en"])
    btn_label = buttons.get(lang, buttons["en"])

    keyboard = [
        [
            InlineKeyboardButton("💬 Chat", url=CHAT_URL),
            InlineKeyboardButton("📞 Contact", url=CONTACT_URL)
        ],
        [
            InlineKeyboardButton(btn_label, web_app=WebAppInfo(url=WEBAPP_URL))
        ]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

def main():
    keep_alive()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(select_language, pattern="^lang_"))
    app.run_polling()

if __name__ == "__main__":
    main()
