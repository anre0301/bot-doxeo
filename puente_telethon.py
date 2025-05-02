from telethon import TelegramClient, events
import asyncio
from config import API_ID, API_HASH

# Función que consulta a otro bot
async def consultar_otro_bot(comando, bot_username):
    # Creamos el cliente de Telegram usando los datos de config.py
    client = TelegramClient('mi_sesion', API_ID, API_HASH)
    await client.start()  # Inicia sesión con el cliente

    

