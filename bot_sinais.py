import os
import asyncio
import random
import pytz
from datetime import datetime, timedelta
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest, TelegramError

# ================================
# CONFIGURAÇÕES VIA RAILWAY
# ================================

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT"))

# FUSO HORÁRIO BRASIL
tz = pytz.timezone("America/Sao_Paulo")

jogos = {
    "tiger": {
        "nome": "🐯 FORTUNE TIGER 🐯",
        "imagem": "https://raster.digital/sinais/imagens/fortunetiger.jpg",
        "link": "https://hype33.fun"
    },
    "snake": {
        "nome": "🐍 FORTUNE SNAKE 🐍",
        "imagem": "https://raster.digital/sinais/imagens/fortunesnake.jpg",
        "link": "https://hype33.fun"
    },
    "dragon": {
        "nome": "🐉 FORTUNE DRAGON 🐉",
        "imagem": "https://raster.digital/sinais/imagens/fortunedragon.jpg",
        "link": "https://hype33.fun"
    },
    "rabbit": {
        "nome": "🐰 RABBIT FORTUNE 🐰",
        "imagem": "https://raster.digital/sinais/imagens/rabbitfortune.jpg",
        "link": "https://hype33.fun"
    }
}

# ================================
# BOT
# ================================

async def enviar_sinais():

    bot = Bot(token=TOKEN)

    print("🚀 BOT INICIADO NO RAILWAY")

    while True:
        try:

            jogo = random.choice(list(jogos.values()))

            giros = random.randint(8, 15)
            normal = random.randint(8, 12)
            turbo = random.randint(1, 3)

            duracao = 300  # 5 minutos

            tempo = datetime.now(tz) + timedelta(seconds=duracao)
            hora = tempo.strftime("%H:%M")

            mensagem = f"""
🤑 <b>HORA DE FAZER GRANA</b>

{jogo["nome"]}

⭐ Máximo de Giros: {giros}

🔥 APROVEITE AGORA

💰 {normal}X Normal  
🚀 {turbo}X Turbo

💡 Dica: Alterne os giros

⏰ Brecha até: {hora}

ESSA AQUI PAGA MUITO ⤵️
"""

            teclado = InlineKeyboardMarkup([
                [InlineKeyboardButton("🎰 JOGAR AGORA", url=jogo["link"])]
            ])

            # 🔥 Versão PTB 21+: métodos NÃO são async
            bot.send_photo(
                chat_id=CHAT_ID,
                photo=jogo["imagem"],
                caption=mensagem,
                parse_mode="HTML",
                reply_markup=teclado
            )

            print("✅ Sinal enviado:", jogo["nome"], "| Próximo às:", hora)

            await asyncio.sleep(duracao - 30)

            # MENSAGEM DE ANÁLISE 30s ANTES
            mensagem_lucro = """
🔥 <b>ANÁLISE CONCLUÍDA</b>

🤑 Recolha seu lucro e prepare-se…

🔎 <b>BUSCANDO NOVAS BRECHAS...</b>

⏳ Falta pouco para o próximo sinal!
"""

            bot.send_message(
                chat_id=CHAT_ID,
                text=mensagem_lucro,
                parse_mode="HTML"
            )

            print("🔎 Mensagem de 'buscando brechas' enviada")

            await asyncio.sleep(30)

        except BadRequest as e:
            print("⚠️ Erro Telegram:", e)
            await asyncio.sleep(10)

        except TelegramError as e:
            print("⚠️ Falha Telegram:", e)
            await asyncio.sleep(10)

        except Exception as erro:
            print("❌ ERRO GERAL:", erro)
            await asyncio.sleep(10)

# ================================
# EXECUÇÃO
# ================================

if __name__ == "__main__":
    asyncio.run(enviar_sinais())