from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from keep_alive import keep_alive

# === CONFIG ===============================================================
TOKEN = "8058105739:AAGYQ2goMQqS1KOTaHQ9e6zTIfcTDJv1MiA"

# Liens généraux
CHAT_URL    = "https://t.me/MeltLabz"
CONTACT_URL = "https://t.me/MeltLabzUS"

# WebApp (page produits) par langue
WEBAPP_URLS = {
    "fr": "https://meltlabz.us/?lang=fr",
    "en": "https://meltlabz.us/?lang=en",
    "es": "https://meltlabz.us/?lang=es",
}

# Page d’informations par langue
INFO_URLS = {
    "fr": "https://meltlabz.us/info.php?lang=fr",
    "en": "https://meltlabz.us/info.php?lang=en",
    "es": "https://meltlabz.us/info.php?lang=es",
}
# ==========================================================================

descriptions = {
    "fr": """🔥 *Bienvenue chez MeltLabz 🔥*

🥶 Nos hash d’exception sont extraits exclusivement à l’eau et aux glaçons 🧊  
Chaque gramme est un concentré de *terpènes explosifs* et de *THC massif*, pensé *uniquement pour les vrais connaisseurs* 👨‍🔬

📦 Expéditions *super stealth & discrètes* partout dans le monde (*sauf Russie*).  
💰 Paiement *uniquement en cryptomonnaie*.  
⏱️ Livraison en *5 à 14 jours ouvrés*.

🤖 Notre BOT a été conçu pour vous *faciliter la vie* : tout est *automatisé*, jusqu’à la commande.  
ℹ️ Cliquez sur le bouton « Informations » pour connaître tous les détails importants avant de commander.  
🕵️‍♂️ Après votre commande, notre *secrétaire vous contactera rapidement* pour valider manuellement votre paiement.""",

    "en": """🔥 *Welcome to MeltLabz 🔥*

🥶 Our exceptional hash is extracted exclusively using ice water 🧊  
Every gram is packed with *explosive terpenes* and *massive THC*, made *only for real connoisseurs* 👨‍🔬

📦 *Super stealth & discreet* worldwide shipping (*except Russia*).  
💰 *Crypto payments only*.  
⏱️ Delivery within *5 to 14 business days*.

🤖 This BOT was built to *make your life easier*: everything is *fully automated*, all the way to checkout.  
ℹ️ Click the “Information” button for all the important details before ordering.  
🕵️‍♂️ After you order, our *secretary will contact you shortly* to manually confirm your payment.""",

    "es": """🔥 *Bienvenido a MeltLabz 🔥*

🥶 Nuestro hash de excepción se extrae exclusivamente con agua y hielo 🧊  
Cada gramo está cargado de *terpenos explosivos* y *THC masivo*, creado *solo para verdaderos conocedores* 👨‍🔬

📦 Envíos *súper stealth y discretos* a todo el mundo (*excepto Rusia*).  
💰 Pagos *solo con criptomonedas*.  
⏱️ Entrega en *5 a 14 días hábiles*.

🤖 Este BOT fue creado para *facilitarte la vida*: todo está *completamente automatizado*, hasta el pedido.  
ℹ️ Toca el botón “Información” para ver todos los detalles importantes antes de ordenar.  
🕵️‍♂️ Después de tu pedido, nuestra *secretaria te contactará* para confirmar tu pago manualmente."""
}

buttons = {
    "fr": "🧪 Voir les Produits",
    "en": "🧪 See Products",
    "es": "🧪 Ver Productos"
}

info_buttons = {
    "fr": "📘 Informations",
    "en": "📘 Information",
    "es": "📘 Información"
}

lang_button = {
    "fr": "🌐 Changer de langue",
    "en": "🌐 Change Language",
    "es": "🌐 Cambiar idioma"
}

# =============== Handlers ================================================

def build_language_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"),
            InlineKeyboardButton("🇫🇷 Français", callback_data="lang_fr"),
            InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es"),
        ]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    # Petite intro animée (peut être supprimée si tu veux)
    await context.bot.send_animation(chat_id=chat_id, animation="https://meltlabz.us/assets/loader.gif")

    await context.bot.send_message(
        chat_id=chat_id,
        text="🌐 Please select your language :",
        reply_markup=build_language_menu()
    )

async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = query.data.split("_", 1)[1]  # "en", "fr", "es"
    context.user_data["lang"] = lang  # mémo local de la langue

    text       = descriptions.get(lang, descriptions["en"])
    btn_label  = buttons.get(lang, buttons["en"])
    info_label = info_buttons.get(lang, info_buttons["en"])
    lang_label = lang_button.get(lang, lang_button["en"])

    # URLs dynamiques selon la langue, avec fallback propre
    webapp_url = WEBAPP_URLS.get(lang, WEBAPP_URLS["en"])
    info_url   = INFO_URLS.get(lang, INFO_URLS["en"])

    keyboard = [
        [InlineKeyboardButton(info_label, web_app=WebAppInfo(url=info_url))],
        [InlineKeyboardButton("💬 Chat", url=CHAT_URL),
         InlineKeyboardButton("📞 Contact", url=CONTACT_URL)],
        [InlineKeyboardButton(btn_label, web_app=WebAppInfo(url=webapp_url))],
        [InlineKeyboardButton(lang_label, callback_data="back_lang")],
    ]

    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def back_to_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat.id
    message_id = query.message.message_id

    # Supprimer le menu courant
    await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    # Afficher le sélecteur de langue
    await context.bot.send_message(
        chat_id=chat_id,
        text="🌐 Please select your language :",
        reply_markup=build_language_menu()
    )

# =============== Boot =====================================================

def main():
    keep_alive()
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(select_language, pattern=r"^lang_"))
    app.add_handler(CallbackQueryHandler(back_to_language, pattern=r"^back_lang$"))

    app.run_polling()

if __name__ == "__main__":
    main()
