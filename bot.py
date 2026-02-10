import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ["TOKEN"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛍️ *Bem-vindo ao MelhorPreço Agora*\n\n"
        "Aqui você encontra o *melhor preço*, *avaliações reais* e *entrega confiável* ✅\n\n"
        "✍️ Digite qual produto você está procurando\n"
        "_Exemplo: air fryer, fone bluetooth, carrinho de bebê_",
        parse_mode="Markdown"
    )

async def produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["produto"] = update.message.text

    keyboard = [
        [InlineKeyboardButton("🛒 Mercado Livre – ⭐ Melhor Avaliação", callback_data="mercadolivre")],
        [InlineKeyboardButton("💰 Shopee – 🔥 Melhor Preço", callback_data="shopee")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🔍 *Comparando as melhores ofertas disponíveis…*\n\n"
        "Selecione onde deseja comprar 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def escolha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    produto = context.user_data.get("produto", "produto")

    if query.data == "mercadolivre":
        link = f"https://www.mercadolivre.com.br/jm/search?as_word={produto}"
    else:
        link = f"https://shopee.com.br/search?keyword={produto}"

    await query.edit_message_text(
        f"✅ *Ótima escolha!*\n\n"
        f"Este produto está entre os *mais vendidos* e com *excelente avaliação* ✅\n\n"
        f"👉 Clique abaixo para acessar a oferta:\n"
        f"{link}\n\n"
        "⏰ _Preços e estoque podem variar._",
        parse_mode="Markdown"
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, produto))
app.add_handler(MessageHandler(filters.ALL, escolha))

app.run_polling()
