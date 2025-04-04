import re
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Configuração básica do logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Dicionário para armazenar a soma dos valores por data
valores_por_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem de instrução para o usuário."""
    await update.message.reply_text(
        "Olá! Siga as regras para enviar os valores:\n"
        "- Para valores até 50 (múltiplos de 5), envie apenas o número (ex.: 10, 25, 50).\n"
        "- Para valores acima de 50 ou que não sejam múltiplos de 5, envie o número seguido de 'a' (ex.: 67 a, 100 a).\n\n"
        "Use /total_hoje para ver a soma acumulada do dia."
    )

async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Processa as mensagens recebidas (texto ou legenda) e soma os valores
    de acordo com as regras:
      - Se não tiver 'a': o valor deve ser até 50 e múltiplo de 5.
      - Se tiver 'a': o valor deve ser acima de 50 ou não ser múltiplo de 5.
    """
    msg = update.effective_message
    # Pega o texto ou, se não houver, a legenda (caso seja uma imagem ou PDF com legenda)
    text = msg.caption or msg.text
    if not text:
        return  # Nada para processar

    text = text.strip()
    logger.info("Recebido: %s", repr(text))

    # Regex simples: captura um ou mais dígitos, seguido de espaços opcionais e uma letra "a" opcional
    padrao = r'^(\d+)\s*(a?)\s*$'
    match = re.fullmatch(padrao, text)
    if not match:
        await msg.reply_text("Formato inválido. Envie apenas um número ou um número seguido de 'a'.")
        return

    num_str, a_flag = match.groups()
    try:
        valor = int(num_str)
    except Exception as e:
        logger.error("Erro ao converter número: %s", e)
        await msg.reply_text("Erro ao processar o número. Tente novamente.")
        return

    # Validação conforme as regras:
    if a_flag:  # Se a mensagem tem 'a'
        # Para valores com 'a', o valor deve ser acima de 50 ou não ser múltiplo de 5.
        if valor <= 50 and (valor % 5 == 0):
            await msg.reply_text("Valor inválido. Para valores até 50 que são múltiplos de 5, não use 'a'.")
            return
    else:  # Se não tiver 'a'
        # Para valores sem 'a', o valor deve ser até 50 e ser múltiplo de 5.
        if valor > 50 or (valor % 5 != 0):
            await msg.reply_text("Valor inválido. Para valores acima de 50 ou que não sejam múltiplos de 5, adicione 'a' ao final.")
            return

    # Se passou na validação, soma o valor
    hoje = datetime.now().date()
    valores_por_data.setdefault(hoje, 0)
    valores_por_data[hoje] += valor
    logger.info("Valor %d registrado para %s. Total: %d", valor, hoje, valores_por_data[hoje])
    await msg.reply_text(f"Valor de {valor} registrado com sucesso.\nTotal acumulado hoje: {valores_por_data[hoje]}")

async def total_hoje(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Exibe o total acumulado dos valores do dia atual."""
    hoje = datetime.now().date()
    total = valores_por_data.get(hoje, 0)
    await update.message.reply_text(f"Total de valores registrados hoje: {total}")

def main() -> None:
    """Inicializa e executa o bot."""
    # Substitua 'SEU_TOKEN_AQUI' pelo token do seu bot
    token = 'Coloque Seu token aqui'
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("total_hoje", total_hoje))
    # Aceita todas as mensagens, para capturar tanto textos quanto legendas
    app.add_handler(MessageHandler(filters.ALL, process_message))

    logger.info("Bot rodando...")
    app.run_polling()

if __name__ == '__main__':
    main()
