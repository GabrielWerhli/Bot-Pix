from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime, timedelta
import pytz
import asyncio

# Token do bot
TOKEN = "Seu_Token"

# Fuso horário de Brasília
br_tz = pytz.timezone('America/Sao_Paulo')

# Armazenamento das somas
daily_total = 0
weekly_total = 0
last_total_reset = datetime.now(br_tz).date()

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot de soma iniciado. Envie valores em mensagens e use /total para ver os totais.")

# Lida com valores enviados
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global daily_total, weekly_total, last_total_reset

    msg = update.message.text.strip()
    try:
        value = float(msg.replace(",", "."))  # Aceita número com vírgula ou ponto
    except ValueError:
        return

    now = datetime.now(br_tz).date()

    # Se mudou o dia, resetar o valor diário
    if now != last_total_reset:
        daily_total = 0
        last_total_reset = now

    daily_total += value
    weekly_total += value

# Comando /total
async def total(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global daily_total

    msg = f"💰 Total do dia: R$ {daily_total:.2f}\n📆 Total da semana: R$ {weekly_total:.2f}"
    sent = await update.message.reply_text(msg)

    # Apaga a mensagem de comando e a resposta em 30 segundos
    await asyncio.sleep(30)
    try:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
        await context.bot.delete_message(chat_id=sent.chat_id, message_id=sent.message_id)
    except:
        pass

    daily_total = 0  # Reseta o total do dia após exibir

# Comando /limpar
async def limpar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    message_id = update.message.message_id

    # Número de mensagens a serem apagadas
    num_messages = 100

    for i in range(num_messages):
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id - i)
        except:
            pass
        await asyncio.sleep(0.1)  # Pequeno atraso para evitar sobrecarga na API

# Função principal
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("total", total))
    app.add_handler(CommandHandler("limpar", limpar))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🤖 Bot rodando...")
    app.run_polling()

if __name__ == '__main__':
    main()
