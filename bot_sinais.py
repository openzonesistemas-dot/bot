import asyncio
import random
import pytz
import os
from datetime import datetime, timedelta
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest, TelegramError

# ======================================
# CONFIGURAÇÕES VIA VARIÁVEIS DE AMBIENTE
# ======================================

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT"))

if TOKEN is None:
    print("❌ ERRO: TELEGRAM_TOKEN não carregado!")
else:
    print("✅ Token carregado com sucesso:", TOKEN)

if CHAT_ID is None:
    print("❌ ERRO: TELEGRAM_CHAT não carregado!")
else:
    print("✅ Chat ID carregado:", CHAT_ID)

# Fuso horário Brasil
tz = pytz.timezone("America/Sao_Paulo")

# ======================================
# LISTA DE JOGOS
# ======================================

jogos = {
    "tiger": {
        "nome": "🐯 FORTUNE TIGER 🐯",
        "imagem": "https://raster.digital/sinais/imagens/fortunetiger.jpg",
        "link": "https://hype33.online"
    },
    "snake": {
        "nome": "🐍 FORTUNE SNAKE 🐍",
        "imagem": "https://raster.digital/sinais/imagens/fortunesnake.jpg",
        "link": "https://hype33.online"
    },
    "dragon": {
        "nome": "🐉 FORTUNE DRAGON 🐉",
        "imagem": "https://raster.digital/sinais/imagens/fortunedragon.jpg",
        "link": "https://hype33.online"
    },
    "rabbit": {
        "nome": "🐰 RABBIT FORTUNE 🐰",
        "imagem": "https://raster.digital/sinais/imagens/rabbitfortune.jpg",
        "link": "https://hype33.online"
    }
}

# ======================================
# BOT DE ENVIO DE SINAIS
# ======================================

async def enviar_sinais():
    bot = Bot(token=TOKEN)
    print("🚀 BOT INICIADO — Monitorando e enviando sinais")

    while True:
        try:
            # Escolhe o jogo aleatório
            jogo = random.choice(list(jogos.values()))

            giros = random.randint(8, 15)
            normal = random.randint(8, 12)
            turbo = random.randint(1, 3)

            # Duração do sinal (entre 4 e 6 min)
            duracao = random.randint(240, 360)

            fim_brecha = datetime.now(tz) + timedelta(seconds=duracao)
            horario = fim_brecha.strftime("%H:%M")

            # Mensagem de sinal
            mensagem = f"""
🤑 <b>HORA DE FAZER GRANA</b>

{jogo["nome"]}

⭐ Máximo de Giros: {giros}

🔥 APROVEITE AGORA

💰 {normal}X Normal  
🚀 {turbo}X Turbo

💡 Dica: Alterne os giros

⏰ Brecha até: {horario}

ESSA AQUI PAGA MUITO ⤵️
"""

            teclado = InlineKeyboardMarkup([
                [InlineKeyboardButton("🎰 JOGAR AGORA", url=jogo["link"])]
            ])

            # Envia foto + legenda
            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=jogo["imagem"],
                caption=mensagem,
                parse_mode="HTML",
                reply_markup=teclado
            )

            print("✅ Sinal enviado:", jogo["nome"], "| Validade até:", horario)

            # Espera a brecha acabar (menos 30s)
            await asyncio.sleep(duracao - 30)

            # Mensagem de lucro
            mensagem_lucro = """
✅ <b>LUCRANDO COM SINAIS</b>

🤑 Recolha seu lucro e fique atento à próxima oportunidade.

🎁 Cadastre-se  
https://hype33.online

🔎 Buscando novas brechas...
"""

            await bot.send_message(
                chat_id=CHAT_ID,
                text=mensagem_lucro,
                parse_mode="HTML"
            )

            print("💰 Mensagem de lucro enviada.")

            # Delay final antes de iniciar o próximo ciclo
            await asyncio.sleep(30)

        except BadRequest as e:
            print("⚠️ Erro Telegram:", e)
            await asyncio.sleep(10)

        except TelegramError as e:
            print("⚠️ Erro de comunicação com Telegram:", e)
            await asyncio.sleep(10)

        except Exception as erro:
            print("❌ ERRO GERAL:", erro)
            await asyncio.sleep(10)


# ======================================
# EXECUÇÃO
# ======================================

if __name__ == "__main__":
    try:
        asyncio.run(enviar_sinais())
    except KeyboardInterrupt:
        print("\n⛔ Bot finalizado manualmente.")