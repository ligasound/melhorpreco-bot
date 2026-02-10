import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ["TOKEN"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛍️ *Bem-vindo ao MelhorPreço Agora*\n\n"
        "Digite o produto que você está procurando 👇",
        parse_mode="Markdown",
    )

async def produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["produto"] = update.message.text

    keyboard = [
        [InlineKeyboardButton("🛒 Mercado Livre", callback_data="ml")],
        [InlineKeyboardButton("💰 Shopee", callback_data="shopee")],
    ]

    await update.message.reply_text(
        "Escolha onde deseja pesquisar:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def escolha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    produto = context.user_data.get("produto", "")

    if query.data == "ml":
        link = f"https://www.mercadolivre.com.br/jm/search?as_word={produto}"
    else:
        link = f"https://shopee.com.br/search?keyword={produto}"

    await query.edit_message_text(
        f"✅ Aqui está o link:\n{link}"
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, produto))
app.add_handler(CallbackQueryHandler(escolha))

app.run_polling()
