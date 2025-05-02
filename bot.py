import telebot
import json
import os
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

# Cargar comandos desde el archivo JSON
with open("comandos.json", "r", encoding="utf-8") as f:
    texto_paginas = json.load(f)
    
# Cargar y guardar usuarios
def cargar_usuarios():
    try:
        with open('usuarios.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def guardar_usuarios(usuarios):
    with open('usuarios.json', 'w') as file:
        json.dump(usuarios, file, indent=4)

# Cargar y guardar saldos
def cargar_saldos():
    try:
        with open('saldos.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def guardar_saldos(saldos):
    with open('saldos.json', 'w') as file:
        json.dump(saldos, file, indent=4)

# /register
@bot.message_handler(commands=['register'])
def cmd_register(message):
    usuarios = cargar_usuarios()
    saldos = cargar_saldos()
    user_id = str(message.from_user.id)

    if user_id in usuarios:
        bot.reply_to(message, f"[⚠️] Hola @{message.from_user.username}, ya estás registrado. Usa /me para ver tu perfil.", parse_mode="Markdown")
        return

    usuario = {
        "first_name": message.from_user.first_name,
        "username": message.from_user.username,
        "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    usuarios[user_id] = usuario
    guardar_usuarios(usuarios)

    saldos[user_id] = 5
    guardar_saldos(saldos)

    bot.reply_to(message, f"[✅] Hola {usuario['first_name']},\n\nTe has registrado correctamente y se te han otorgado 5 monedas.\n\n¡Bienvenido y disfruta de nuestro bot!")

# /cmds
@bot.message_handler(commands=['cmds'])
def cmd_cmds(message):
    texto = (
        "❰ #AXC_DATA❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n"
        "🕵 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔 🕵\n\n"
        "Hola, Bienvenido a nuestro Menú Principal de Comandos\n\n"
        "📌Nuestros comandos se encuentran divididos en secciones para facilitar la interacción del usuario.\n\n"
        "Selecciona una sección en la parte inferior para visualizar los comandos."
    )
    imagen_url = "https://ibb.co/BVwh22Lj"  # URL directa a la imagen

    markup = InlineKeyboardMarkup(row_width=2)
    botones = [
        InlineKeyboardButton("🪪 RENIEC", callback_data="reniec_1"),
        InlineKeyboardButton("👮🏻‍♂️ DELITOS", callback_data="delitos_1"),
        InlineKeyboardButton("⚙️ GENERADOR", callback_data="generador_1"),
        InlineKeyboardButton("☠️ SPAM", callback_data="spam_1"),
        InlineKeyboardButton("💳 BAUCHER", callback_data="baucher_1"),
        InlineKeyboardButton("🎁 GRATIS", callback_data="gratis_1"),
        InlineKeyboardButton("📞 TELEFONIA", callback_data="telefonia_1"),
        InlineKeyboardButton("🚗 SUNARP", callback_data="sunarp_1"),
        InlineKeyboardButton("👨‍👩‍👧 FAMILIA", callback_data="familia_1"),
        InlineKeyboardButton("🔎 SEEKER", callback_data="seeker_1"),
        InlineKeyboardButton("➕ EXTRAS", callback_data="extras_1"),
        InlineKeyboardButton("💎 VIP", callback_data="vip_1")
    ]
    markup.add(*botones)
    bot.send_photo(message.chat.id, photo=imagen_url, caption=texto, reply_markup=markup)


# /me
@bot.message_handler(commands=['me'])
def cmd_me(message):
    usuarios = cargar_usuarios()
    saldos = cargar_saldos()
    user_id = str(message.from_user.id)

    if user_id not in usuarios:
        bot.reply_to(message, "¡No estás registrado! Usa /register.")
        return

    usuario = usuarios[user_id]
    saldo = saldos.get(user_id, 0)
    texto = (
        f"#AXC_BOT💫\n\n"
        f"❰🙎‍♂️❱ ID ➣ {user_id}\n"
        f"❰🗒❱ NOMBRE ➣ {usuario['first_name']}\n"
        f"❰⚡️❱ USUARIO ➣ @{usuario['username']}\n"
        f"❰💰❱ CREDITOS ➣ {saldo + 2} monedas\n"
        f"❰📅❱ ROL ➣ {'VIP' if saldo + 2 >= 10 else 'FREE'}\n"
        f"❰📈❱ PLAN ➣ {'PREMIUM' if saldo + 2 >= 10 else 'FREE'}\n"
        f"❰🗓❱ REGISTRO ➣ {usuario['registration_date']}\n"
        f"❰🔎❱ CONSULTAS ➣ 0\n"
        f"❰📆❱ HOY ➣ 0\n"
        f"❰⏱❱ ANTI-SPAM ➣ 60'\n"
        f"❰💯❱ ESTADO ➣ ACTIVO"
    )
    bot.send_photo(message.chat.id, photo="https://ibb.co/BVwh22Lj", caption=texto)


# CALLBACKS
@bot.callback_query_handler(func=lambda call: True)
def responder_callback(call):
    data = call.data

    # DICCIONARIO DE PAGINAS POR CATEGORIA
    paginas = {
        "reniec": [
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[🪪] RENIEC ONLINE - FREE\nComando ➾ /dni 44443333\nPrecio ➾ 1 Crédito\nResultado ➾ Foto e información completa en (TEXTO).\n\n[🪪] RENIEC ONLINE - BASICO\nComando ➾ /dnif 44443333\nPrecio ➾ 2 Créditos\nResultado ➾ Foto, Firma e información completa en (TEXTO).\n\n[🪪] RENIEC ONLINE - STANDARD\nComando ➾ /dnit 44443333\nPrecio ➾ 3 Créditos\nResultado ➾ Foto, Firma, Huellas e información completa en (TEXTO).\n\n[🪪] NOMBRES DATABASE - BASICO\nComando ➾ /nmdb N¹|AP¹|AP²\nPrecio ➾ 1 Crédito\nResultado ➾ Filtrador de Nombres en (TEXTO Y TXT).\n\n[📍] DIRECCION ONLINE - STANDARD\nComando ➾ /dir Carrion av1\nPrecio ➾ 2 Créditos\nResultado ➾ Filtrador de Direcciones en (TEXTO).\n\n[📍] DIRECCION ONLINE - STANDARD\nComando ➾ /dir2 44443333\nPrecio ➾ 3 Créditos\nResultado ➾ Filtrador de Direcciones en (TEXTO).\n\nPÁGINA ➾ 1/2",
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\nCATEGORÍA ➾ Reniec\nCOMANDOS ➾ 8 Comandos disponibles\nPÁGINA ➾ 2/2\n\n[🪪] RENIEC DATABASE - BASICO\nComando ➾ /dnidb 44443333\nPrecio ➾ 1 Crédito\nResultado ➾ Foto e información completa en (TEXTO).\n\n[🪪] RENIEC DATABASE - STANDARD\nComando ➾ /dnifdb 44443333\nPrecio ➾ 2 Créditos\nResultado ➾ Foto, Firma e información completa en (TEXTO).\n\n[🪪] RENIEC DATABASE - PREMIUM\nComando ➾ /dnitdb 44443333\nPrecio ➾ 3 Créditos\nResultado ➾ Foto, Firma, Huellas e información completa en (TEXTO).\n\nPÁGINA ➾ 2/2"
        ],
        "delitos": [
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[👮🏻‍♂️] PNP ONLINE CIP - BASICO\nComando ➾ /cip 31288473\nPrecio ➾ 3 Créditos\nResultado ➾ Foto, Firma e información del policía en (TEXTO).\n\n[👮🏻‍♂️] PNP ONLINE DNI - STANDARD\nComando ➾ /pdni 05390731\nPrecio ➾ 3 Créditos\nResultado ➾ Datos del policía en (TEXTO).\n\n[👮🏻‍♂️] PNP SUELDOS CIP - STANDARD\nComando ➾ /ptra 31288473\nPrecio ➾ 5 Créditos\nResultado ➾ Sueldos del policía en (TEXTO).\n\n[👮🏻‍♂️] PNP SUELDOS CIP - PREMIUM\nComando ➾ /ptrapdf 05390731|1|2024\nPrecio ➾ 5 Créditos\nResultado ➾ Ficha de sueldos certificado en (PDF).\n\nPÁGINA 1/2",
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[👮🏻‍♂️] VERIFICADOR ANT PENALES - STANDARD\nComando ➾ /antpenv 44443333\nPrecio ➾ 2 Créditos\nResultado ➾ Verifica si el documento registra antecedentes penales en (TEXTO).\n\n[👮🏻‍♂️] VERIFICADOR ANT POLICIALES - STANDARD\nComando ➾ /antpolv 44443333\nPrecio ➾ 2 Créditos\nResultado ➾ Verifica si el documento registra antecedentes policiales en (TEXTO).\n\n[👮🏻‍♂️] VERIFICADOR ANT JUDICIALES - STANDARD\nComando ➾ /antjudv 44443333\nPrecio ➾ 2 Créditos\nResultado ➾ Verifica si el documento registra antecedentes judiciales en (TEXTO).\n\nPÁGINA 2/2"
        ],
        "generador": [
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[🪪] FICHA C4 AZUL - FREE\nComando ➾ /c4 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera una ficha C4 azul en (FOTO).\n\n[🪪] FICHA C4 AZUL - BASICO\nComando ➾ /c4a 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera una ficha C4 azul en (PDF).\n\n[🪪] DNI VIRTUAL - STANDARD\nComando ➾ /dniv 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera copia de DNI azul/amarillo en (FOTO).\n\n[🪪] DNI ELECTRONICO - STANDARD\nComando ➾ /dnivel 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera copia de DNI electrónico en (FOTO).\n\n[🪪] FICHA C4 BLANCO - BASICO\nComando ➾ /c4b 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera una ficha C4 blanco en (FOTO).\n\n[🪪] FICHA C4 BLANCO - STANDARD\nComando ➾ /c4bpdf 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera una ficha C4 blanco en (PDF).\n\n[🪪] FICHA INSCRIPCION - STANDARD\nComando ➾ /c4i 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera una ficha de inscripción en (FOTO).\n\nPÁGINA ➾ 1/2",
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[🪪] FICHA INSCRIPCION - PREMIUM\nComando ➾ /c4ipdf 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera una ficha de inscripción en (PDF).\n\n[🪪] ANTECEDENTE PENALES - STANDARD\nComando ➾ /antpen 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera una ficha antecedentes penales en (FOTO).\n\n[🪪] ANTECEDENTE POLICIALES - STANDARD\nComando ➾ /antpol 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera una ficha antecedentes policiales en (FOTO).\n\n[🪪] ANTECEDENTE JUDICIALES - STANDARD\nComando ➾ /antjud 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera una ficha antecedentes judiciales en (FOTO).\n\nPÁGINA ➾ 2/2"
        ],
        "telefonia": [
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[📞] OSIPTEL ONLINE - PREMIUM\nComando ➾ /telp 44443333\nComando ➾ /telp 999888777\nPrecio ➾ 10 Creditos\nResultado ➾ Devuelve números y titulares desde OSIPTEL en (TEXTO).\n\n[📞] OSIPTEL DATABASE - STANDARD\nComando ➾ /cel 999888777\nPrecio ➾ 5 Creditos\nResultado ➾ Devuelve números y titulares desde OSIPTEL en (TEXTO).\n\n[📞] OSIPTEL DATABASE - STANDARD\nComando ➾ /stel 44443333\nPrecio ➾ 5 Creditos\nResultado ➾ Devuelve números y titulares desde OSIPTEL en (TEXTO).\n\n[📞] CLARO ONLINE - STANDARD\nComando ➾ /claro 999888777\nPrecio ➾ 5 Creditos\nResultado ➾ Devuelve números y titulares desde CLARO en (TEXTO).\n\n[📞] BITEL ONLINE - PREMIUM\nComando ➾ /bitel 999888777\nPrecio ➾ 5 Creditos\nResultado ➾ Devuelve números y titulares desde BITEL en (TEXTO).\n\n[📞] OSIPTEL VERIF - STANDARD\nComando ➾ /osiptelv 44443333\nPrecio ➾ 5 Creditos\nResultado ➾ Devuelve las lineas desde OSIPTEL en (TEXTO).\n\nPágina 1/2",
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[📞] CLARO DATABASE - STANDARD\nComando ➾ /clarodb 44443333\nComando ➾ /clarodb 999888777\nPrecio ➾ 3 Creditos\nResultado ➾ Devuelve números y titulares desde CLARO en (TEXTO).\n\n[📞] MOVISTAR DATABASE - STANDARD\nComando ➾ /movdb 08345781\nComando ➾ /movdb 999888777\nPrecio ➾ 3 Creditos\nResultado ➾ Devuelve números y titulares desde MOVISTAR en (TEXTO).\n\n[📞] BITEL DATABASE - STANDARD\nComando ➾ /biteldb 999888777\nPrecio ➾ 3 Creditos\nResultado ➾ Devuelve números y titulares desde BITEL en (TEXTO).\n\nPágina 2/2"
        ],
        "sunarp": [
            "📄 Página 1/1\n\n[🚗] PLACA VEHÍCULO\nComando ➣ /sunarp ABC123\nPrecio ➣ 2 Créditos\nResultado ➣ Datos de vehículo por placa."
        ],
        "familia": [
            "📄 Página 1/1\n\n[🧑‍🤝‍🧑] VINCULADOS\nComando ➣ /fami 12345678\nPrecio ➣ 2 Créditos\nResultado ➣ Vínculos familiares del DNI."
        ],
        "spam": [
            "📄 Página 1/1\n\n[✉️] SMS SPAM\nComando ➣ /sms 987654321|Texto del mensaje\nPrecio ➣ 1 Crédito\nResultado ➣ Envío de SMS masivo."
        ],
        "seeker": [
            "📄 Página 1/1\n\n[🔎] BUSCADOR IP\nComando ➣ /seek 190.XXX.XXX.1\nPrecio ➣ 1 Crédito\nResultado ➣ Localización aproximada de IP."
        ],
        "baucher": [
            "📄 Página 1/1\n\n[💳] VALIDACIÓN\nComando ➣ /bauch CODIGO\nPrecio ➣ 1 Crédito\nResultado ➣ Verifica validez de baucher."
        ],
        "extras": [
            "📄 Página 1/1\n\n[📁] ARCHIVOS RANDOM\nComando ➣ /extra\nPrecio ➣ Gratis\nResultado ➣ Envía un archivo aleatorio."
        ],
        "gratis": [
            "📄 Página 1/1\n\n[🎁] CRÉDITO DIARIO\nComando ➣ /free\nPrecio ➣ 0 Créditos\nResultado ➣ Reclama 1 crédito diario gratis."
        ],
        "vip": [
            "📄 Página 1/1\n\n[💎] CONSULTA PREMIUM\nComando ➣ /vip 12345678\nPrecio ➣ 5 Créditos\nResultado ➣ Información ultra detallada."
        ]
    }

     # Verificar si la llamada es para una página dentro de una categoría
    if "_" in data and data.split("_")[0] in paginas:
        categoria, pag = data.split("_")
        pagina_actual = int(pag)

        total_paginas = len(paginas[categoria])
        texto = paginas[categoria][pagina_actual - 1]

        botones = []
 # Botones de navegación
        if pagina_actual > 1:
            botones.append(InlineKeyboardButton("⬅️ Atrás", callback_data=f"{categoria}_{pagina_actual - 1}"))
        botones.append(InlineKeyboardButton("🏠 Menú", callback_data="inicio"))
        if pagina_actual < total_paginas:
            botones.append(InlineKeyboardButton("➡️ Adelante", callback_data=f"{categoria}_{pagina_actual + 1}"))

        markup_nav = InlineKeyboardMarkup([botones])

         # Editar el mensaje con la nueva información y los botones
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=texto,
            reply_markup=markup_nav
        )
        return

    # SI EL USUARIO PIDE INICIO (MENÚ PRINCIPAL)
    if "_" in data and data.split("_")[0] in paginas:
        categoria, pag = data.split("_")
        pagina_actual = int(pag)

        total_paginas = len(paginas[categoria])
        texto = paginas[categoria][pagina_actual - 1]

        botones = []

        # Botones de navegación
        if pagina_actual > 1:
            botones.append(InlineKeyboardButton("⬅️ Atrás", callback_data=f"{categoria}_{pagina_actual - 1}"))
        botones.append(InlineKeyboardButton("🏠 Menú", callback_data="inicio"))
        if pagina_actual < total_paginas:
            botones.append(InlineKeyboardButton("➡️ Adelante", callback_data=f"{categoria}_{pagina_actual + 1}"))

        markup_nav = InlineKeyboardMarkup([botones])

        # Editar el mensaje con la nueva información y los botones
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=texto,
            reply_markup=markup_nav
        )
        return

    # Si el usuario pide el menú principal
    if data == "inicio":
        texto = (
            "❰ #AXC DATA❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n"
            "🕵 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔 🕵\n\n"
            "Hola, Bienvenido a nuestro Menú Principal de Comandos\n\n"
            "📌Nuestros comandos se encuentran divididos en secciones para facilitar la interacción del usuario.\n\n"
            "Selecciona una sección en la parte inferior para visualizar los comandos."
        )
        markup = InlineKeyboardMarkup(row_width=2)
        botones = [
            InlineKeyboardButton("🪪 RENIEC", callback_data="reniec_1"),
            InlineKeyboardButton("👮🏻‍♂️ DELITOS", callback_data="delitos_1"),
            InlineKeyboardButton("⚙️ GENERADOR", callback_data="generador_1"),
            InlineKeyboardButton("☠️ SPAM", callback_data="spam_1"),
            InlineKeyboardButton("💳 BAUCHER", callback_data="baucher_1"),
            InlineKeyboardButton("🎁 GRATIS", callback_data="gratis_1"),
            InlineKeyboardButton("📞 TELEFONIA", callback_data="telefonia_1"),
            InlineKeyboardButton("🚗 SUNARP", callback_data="sunarp_1"),
            InlineKeyboardButton("👨‍👩‍👧 FAMILIA", callback_data="familia_1"),
            InlineKeyboardButton("🔎 SEEKER", callback_data="seeker_1"),
            InlineKeyboardButton("➕ EXTRAS", callback_data="extras_1"),
            InlineKeyboardButton("💎 VIP", callback_data="vip_1")
        ]
        markup.add(*botones)

        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=texto,
            reply_markup=markup
        )
        return



# Iniciar el bot
print("✅ BOT INICIADO")
bot.infinity_polling()















