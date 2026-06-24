import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ===== YOUR REAL COORDINATES =====
HOME_LAT, HOME_LON = 23.19138044, 72.61952561    # AKSHAT ICON
OFFICE_LAT, OFFICE_LON = 23.17589237, 72.62957638  # Siddhraj Z Square
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # We'll set this later

def build_deep_links(pickup_lat, pickup_lon, drop_lat, drop_lon):
    """
    Returns dict of { 'Uber': url, 'Ola': url, 'Rapido': intent }
    """
    uber = (
        f"uber://?action=setPickup"
        f"&pickup[latitude]={pickup_lat}&pickup[longitude]={pickup_lon}"
        f"&dropoff[latitude]={drop_lat}&dropoff[longitude]={drop_lon}"
    )
    ola = (
        f"ola://?"
        f"pickup_lat={pickup_lat}&pickup_lng={pickup_lon}"
        f"&drop_lat={drop_lat}&drop_lng={drop_lon}"
    )
    rapido = "intent://#Intent;package=com.rapido.passenger;scheme=rapido;end;"
    return {"🟢 Uber": uber, "🟣 Ola": ola, "🟠 Rapido": rapido}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey! Just send me:\n"
        "🚀 *morning ride*   – home to office\n"
        "🌙 *evening ride*   – office to home\n\n"
        "I'll give you one‑tap links to all apps. ❤️",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    if text not in ["morning ride", "evening ride"]:
        await update.message.reply_text("Send exactly 'morning ride' or 'evening ride'")
        return

    if text == "morning ride":
        pickup = (HOME_LAT, HOME_LON)
        drop = (OFFICE_LAT, OFFICE_LON)
        direction = "🏡 Home → 🏢 Office"
    else:
        pickup = (OFFICE_LAT, OFFICE_LON)
        drop = (HOME_LAT, HOME_LON)
        direction = "🏢 Office → 🏡 Home"

    links = build_deep_links(*pickup, *drop)

    # Build a vertical inline keyboard
    keyboard = [
        [InlineKeyboardButton(name, url=url)]
        for name, url in links.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"👇 *{direction}*\nTap an app to see the fare. Choose the cheapest! 🛵",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()