from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8058105739:AAGYQ2goMQqS1KOTaHQ9e6zTIfcTDJv1MiA"
WEBAPP_URL = "https://meltlabz.us/"  # ← Remplace par ton vrai lien

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("🧪 Voir les Produits", web_app=WebAppInfo(url=WEBAPP_URL))
    ]]
    await update.message.reply_text(
        "👋 *Bienvenue sur MeltLabz !*\\nClique sur le bouton ci-dessous pour voir les produits 🔬",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
