import asyncio
import random
import pytz
import os
from datetime import datetime, timedelta
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError, BadRequest

# ================================
# VARIÁVEIS DO RAILWAY
# ================================
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT"))

# Fuso horário Brasil
tz = pytz.timezone("America/Sao_Paulo")

# Jogos disponíveis
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

# ================================
# FUNÇÃO PRINCIPAL
# ================================
async def enviar_sinais():
    bot = Bot(token=TOKEN)
    print("🚀 BOT INICIADO | Ciclo: 5 minutos por sinal")

    DURAÇÃO_SINAL = 300  # 5 minutos (fixo)
    AVISO_TEMPO = 30     # 30 segundos antes

    while True:
        try:
            jogo = random.choice(list(jogos.values()))

            giros = random.randint(8, 15)
            normal = random.randint(8, 12)
            turbo = random.randint(1, 3)

            fim = datetime.now(tz) + timedelta(seconds=DURAÇÃO_SINAL)
            hora_fim = fim.strftime("%H:%M")

            mensagem = f"""
🤑 <b>HORA DE FAZER GRANA</b>

{jogo["nome"]}

⭐ Máximo de Giros: {giros}

🔥 APROVEITE AGORA

💰 {normal}X Normal  
🚀 {turbo}X Turbo

💡 Dica: Alterne os giros

⏰ Brecha até: {hora_fim}

ESSA AQUI PAGA MUITO ⤵️
"""

            teclado = InlineKeyboardMarkup([
                [InlineKeyboardButton("🎰 JOGAR AGORA", url=jogo["link"])]
            ])

            # Envia o sinal
            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=jogo["imagem"],
                caption=mensagem,
                parse_mode="HTML",
                reply_markup=teclado
            )

            print(f"✅ Sinal enviado | {jogo['nome']} | Termina às {hora_fim}")

            # AGUARDA ATÉ 30s ANTES DO PRÓXIMO SINAL
            await asyncio.sleep(DURAÇÃO_SINAL - AVISO_TEMPO)

            # Envia aviso de busca de estratégia
            await bot.send_message(
                chat_id=CHAT_ID,
                text="🔎 <b>Buscando novas estratégias...</b>",
                parse_mode="HTML"
            )
            print("🔎 Buscando novas estratégias...")

            # Espera os 30s finais
            await asyncio.sleep(AVISO_TEMPO)

        except (TelegramError, BadRequest) as e:
            print("⚠️ Erro Telegram:", e)
            await asyncio.sleep(5)

        except Exception as erro:
            print("❌ ERRO GERAL:", erro)
            await asyncio.sleep(5)


# ================================
# INICIAR BOT
# ================================
if __name__ == "__main__":
    if TOKEN is None:
        print("❌ ERRO: TELEGRAM_TOKEN não encontrado!")
    else:
        print("✅ Token carregado com sucesso")
    asyncio.run(enviar_sinais())