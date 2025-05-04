import telebot
import json
import os
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from config import BOT_TOKEN, ADMIN_ID

bot = telebot.TeleBot(BOT_TOKEN)
ID_GRUPO_LOGS = -1002645920112  # Reemplaza con el ID real de tu grupo


# Definición de la función
def cargar_archivo(archivo):
    with open(archivo, 'r') as f:
        return json.load(f)

# Llamada a la función
creditos_file = 'creditos.json'
creditos_data = cargar_archivo(creditos_file)

#comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    photo_url = 'https://ibb.co/N6Gnxx74'  # Enlace directo de la imagen
    caption = """𓆩 𝐀𝐗𝐂 𝐃𝐀𝐓𝐀 𓆪  
Bienvenido al núcleo donde los datos no duermen y el control es absoluto.  
Tu viaje en el mundo del doxing peruano comienza aquí. 🚨📡

╭──▸ 𝐈𝐍𝐈𝐂𝐈𝐀 𝐓𝐔 𝐂𝐀𝐌𝐈𝐍𝐎  
│ 🧬 /register — Regístrate en el sistema  
│ 📂 /cmds — Visualiza los comandos  
│ 🧑‍💼 /me — Consulta tu identidad digital  
│ 🧾 /buy — Adquiere créditos y memebresias  
╰─────────────────────────

❗ 𝗔𝗩𝗜𝗦𝗢  

El uso indebido de este servicio es responsabilidad total del usuario. AXC DATA no se hace responsable por daños o mal uso de los datos obtenidos.

☂ ACTIVA TU PODER, DOMINA LA INFO.☂

𝗗𝗘𝗦𝗔𝗥𝗥𝗢𝗟𝗟𝗔𝗗𝗢𝗥 𝗢𝗙𝗖"""

    # Botón con enlace a tu perfil
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton("🐺 𝗔𝗟𝗕𝗘𝗥𝗧 𝗣𝗘 🐺", url="https://t.me/serviciosalbertpe")
    markup.add(btn)

    # Enviar imagen con el mensaje y el botón
    bot.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=caption,
        reply_markup=markup,
        parse_mode="HTML"
    )

#COMANDO VENDEDORES
@bot.message_handler(commands=['vendedores'])
def cmd_vendedores(message):
    admin_principal_id = 7819787342  # Reemplaza con tu ID real

    if message.from_user.id != admin_principal_id:
        bot.reply_to(message, "🚫 Este comando solo puede ser usado por el administrador principal.")
        return

    sellers = cargar_archivo('sellers.json')

    if not sellers:
        bot.reply_to(message, "🔸 No hay vendedores registrados actualmente.")
        return

    lista_vendedores = ""
    for seller_id in sellers:
        try:
            user = bot.get_chat(seller_id)
            nombre = user.first_name.replace('[', '').replace(']', '')  # Limpiar Markdown si lo tiene
            lista_vendedores += f"🔹 [{nombre}](tg://user?id={seller_id}) - `{seller_id}`\n"
        except Exception as e:
            lista_vendedores += f"🔹 Usuario desconocido - `{seller_id}`\n"

    bot.reply_to(message, f"📋 Lista de *Vendedores Autorizados*:\n\n{lista_vendedores}", parse_mode="Markdown")

# Cargar o inicializar datos de usuarios
if os.path.exists('user_data.json'):
    with open('user_data.json', 'r') as f:
        user_data = json.load(f)
else:
    user_data = {"registration": {}, "topics": {}, "banned": {}, "roles": {}}

def save_user_data():
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f, indent=4)

# Cargar comandos desde el archivo JSON
with open("comandos.json", "r", encoding="utf-8") as f:
    texto_paginas = json.load(f)
    
def is_admin_or_seller(user_id):
    if user_id == ADMIN_ID or user_id in user_data["roles"].get('sellers', []):
        return True
    return False
    
def is_admin_or_seller(user_id):
    if is_admin(user_id):  # Verificar si es admin
        return True
    if is_seller(user_id):  # Verificar si es vendedor
        return True
    return False

# Cargar y guardar usuarios
def cargar_usuarios():
    with open("user_data.json", "r") as file:
        return json.load(file)

def guardar_usuarios(usuarios):
    with open("user_data.json", "w") as file:
        json.dump(usuarios, file, indent=4)

def cargar_archivo(archivo):
    if os.path.exists(archivo):
        with open(archivo, 'r') as file:
            return json.load(file)
    return {}

def guardar_archivo(archivo, data):
    with open(archivo, 'w') as file:
        json.dump(data, file, indent=4)

def cargar_sellers():
    if os.path.exists("sellers.json"):
        with open("sellers.json", "r") as f:
            return json.load(f)
    else:
        return []

def guardar_sellers(data):
    with open("sellers.json", "w") as f:
        json.dump(data, f, indent=4)

@bot.message_handler(commands=['register'])
def cmd_register(message):
    usuarios = cargar_usuarios()
    saldos = cargar_archivo("saldos.json")
    user_id = str(message.from_user.id)

    if user_id in usuarios:
        bot.reply_to(message, f"[⚠️] Hola @{message.from_user.username}, ya estás registrado. Usa /me para ver tu perfil.", parse_mode="Markdown")
        return

    usuario = {
        "first_name": message.from_user.first_name,
        "username": message.from_user.username,
        "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "plan": "FREE",
        "rol": "FREE"
    }

    usuarios[user_id] = usuario
    guardar_usuarios(usuarios)

    # Asignar 5 créditos al nuevo usuario
    saldos.setdefault("CREDITOS", {})
    saldos["CREDITOS"][user_id] = 5
    guardar_archivo("saldos.json", saldos)

    bot.reply_to(message, f"[✅] Hola {usuario['first_name']},\n\nTe has registrado correctamente y se te han otorgado 5 créditos.\n\n¡Bienvenido y disfruta de nuestro bot!")

# Comando para convertir un usuario en seller
@bot.message_handler(commands=['seller'])
def make_seller(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 No tienes permiso para usar este comando.")
        return

    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        bot.reply_to(message, "Uso correcto: /seller ID_DEL_USUARIO")
        return

    sellers = cargar_sellers()
    user_id = args[1]

    if user_id not in sellers:
        sellers.append(user_id)
        guardar_sellers(sellers)
        bot.reply_to(message, f"✅ Usuario {user_id} ahora es un SELLER.")
    else:
        bot.reply_to(message, f"ℹ️ El usuario {user_id} ya era SELLER.")

@bot.message_handler(commands=['unseller'])
def remove_seller(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 No tienes permiso para usar este comando.")
        return

    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        bot.reply_to(message, "Uso correcto: /unseller ID_DEL_USUARIO")
        return

    sellers = cargar_sellers()
    user_id = args[1]

    if user_id in sellers:
        sellers.remove(user_id)
        guardar_sellers(sellers)
        bot.reply_to(message, f"❌ Usuario {user_id} ya no es SELLER.")
    else:
        bot.reply_to(message, f"ℹ️ El usuario {user_id} no estaba registrado como SELLER.")
        
@bot.message_handler(commands=['cred'])
def cmd_cred(message):
    if not is_admin_or_seller(message.from_user.id):
        bot.reply_to(message, "🚫 No tienes permiso para usar este comando.")
        return

    args = message.text.split()
    if len(args) != 3 or not args[1].isdigit() or not args[2].isdigit():
        bot.reply_to(message, "Uso correcto: /cred ID_DEL_USUARIO CREDITOS_A_AGREGAR")
        return

    user_id = args[1]
    creditos_a_agregar = int(args[2])

    # Cargar datos de créditos
    creditos_data = cargar_archivo('creditos.json')

    # Sumar créditos
    creditos_actuales = creditos_data.get(user_id, 0)
    creditos_data[user_id] = creditos_actuales + creditos_a_agregar
    total_creditos = creditos_data[user_id]

    # Determinar el plan solo por créditos
    if total_creditos >= 1201:
        plan = "PREMIUM"
    elif total_creditos >= 321:
        plan = "STANDARD"
    elif total_creditos >= 30:
        plan = "BÁSICO"
    else:
        plan = "FREE"

    # Guardar los nuevos créditos
    guardar_archivo('creditos.json', creditos_data)

    # Actualizar el plan en el archivo de usuarios
    usuarios = cargar_usuarios()
    if user_id in usuarios:
        usuarios[user_id]["plan"] = plan
        guardar_usuarios(usuarios)

    # Datos para el mensaje
    nombre_vendedor = message.from_user.first_name
    id_vendedor = message.from_user.id
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Mensaje detallado
    texto = f"""
[#AXC_DATA]  

VENDEDOR ➾ [👤 {nombre_vendedor}](tg://user?id={id_vendedor}) - `{id_vendedor}`  
AÑADIÓ ➾ `{creditos_a_agregar}` créditos  
USUARIO ➾ [👤 Usuario](tg://user?id={user_id}) - `{user_id}`  
PLAN ➾ `{plan}`  
TOTAL ➾ `{total_creditos}` créditos acumulados  
FECHA ➾ `{fecha_actual}`
"""

    # Enviar al vendedor
    bot.reply_to(message, texto, parse_mode="Markdown")

    # Enviar al grupo (-1002645920112)
    ID_GRUPO_LOGS = -1002645920112  # Reemplaza con el ID de tu grupo
    bot.send_message(ID_GRUPO_LOGS, texto, parse_mode="Markdown")

        
bot.message_handler(commands=['uncred'])
def cmd_uncred(message):
    if not is_admin_or_seller(message.from_user.id):
        bot.reply_to(message, "🚫 No tienes permiso para usar este comando.")
        return

    args = message.text.split()
    if len(args) != 3 or not args[1].isdigit() or not args[2].isdigit():
        bot.reply_to(message, "Uso correcto: /uncred ID_DEL_USUARIO CREDITOS_A_RESTAR")
        return

    user_id = args[1]
    creditos_a_restar = int(args[2])

    # Cargar los datos de créditos existentes
    creditos_data = cargar_archivo('creditos.json')

    if user_id not in creditos_data:
        creditos_data[user_id] = 0

    if creditos_data[user_id] < creditos_a_restar:
        bot.reply_to(message, f"🚫 El usuario {user_id} no tiene suficientes créditos para restar {creditos_a_restar}. Créditos actuales: {creditos_data[user_id]}")
        return

    creditos_data[user_id] -= creditos_a_restar
    total_creditos = creditos_data[user_id]

    # Determinar nuevo plan
    if total_creditos >= 1201:
        plan = "PREMIUM"
    elif total_creditos >= 321:
        plan = "STANDARD"
    elif total_creditos >= 30:
        plan = "BÁSICO"
    else:
        plan = "FREE"

    guardar_archivo('creditos.json', creditos_data)

    usuarios = cargar_usuarios()
    if user_id in usuarios:
        usuarios[user_id]["plan"] = plan
        guardar_usuarios(usuarios)

    # Info de registro
    nombre_vendedor = message.from_user.first_name
    id_vendedor = message.from_user.id
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")

    texto = f"""
[#AXC_DATA]  

VENDEDOR ➾ [👤 {nombre_vendedor}](tg://user?id={id_vendedor}) - `{id_vendedor}`  
QUITÓ ➾ `{creditos_a_restar}` créditos  
USUARIO ➾ [👤 Usuario](tg://user?id={user_id}) - `{user_id}`  
PLAN ➾ `{plan}`  
TOTAL ➾ `{total_creditos}` créditos restantes  
FECHA ➾ `{fecha_actual}`
"""

    # Enviar al vendedor
    bot.reply_to(message, texto, parse_mode="Markdown")

    # Enviar al grupo de logs
    ID_GRUPO_LOGS = -1002645920112
    bot.send_message(ID_GRUPO_LOGS, texto, parse_mode="Markdown")


        
@bot.message_handler(commands=['sub'])
def cmd_sub(message):
    if not is_admin_or_seller(message.from_user.id):
        bot.reply_to(message, "🚫 No tienes permiso para usar este comando.")
        return

    args = message.text.split()
    if len(args) != 3 or not args[1].isdigit() or not args[2].isdigit():
        bot.reply_to(message, "Uso correcto: /sub ID_DEL_USUARIO DIAS_A_ASIGNAR")
        return

    user_id = args[1]
    dias_a_asignar = int(args[2])

    # Cargar los datos de días restantes
    dias_restantes_data = cargar_archivo('dias_restantes.json')

    # Asignar directamente los días
    dias_restantes_data[user_id] = dias_a_asignar

    # Determinar plan según los días
    if dias_restantes_data[user_id] >= 1201:
        plan = "PREMIUM"
    elif dias_restantes_data[user_id] >= 321:
        plan = "STANDARD"
    elif dias_restantes_data[user_id] >= 30:
        plan = "BÁSICO"
    else:
        plan = "FREE"

    # Guardar datos
    guardar_archivo('dias_restantes.json', dias_restantes_data)

    # Actualizar plan en archivo de usuarios
    usuarios = cargar_usuarios()
    if user_id in usuarios:
        usuarios[user_id]["plan"] = plan
        guardar_usuarios(usuarios)

    # Datos del mensaje
    nombre_vendedor = message.from_user.first_name
    id_vendedor = message.from_user.id
    total_dias = dias_restantes_data[user_id]
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")

    texto = f"""
[#AXC_DATA]  

VENDEDOR ➾ [👤 {nombre_vendedor}](tg://user?id={id_vendedor}) - `{id_vendedor}`  
AÑADIÓ ➾ `{dias_a_asignar}` días de membresía  
USUARIO ➾ [👤 Usuario](tg://user?id={user_id}) - `{user_id}`  
PLAN ➾ `{plan}`  
TOTAL ➾ `{total_dias}` días restantes  
FECHA ➾ `{fecha_actual}`
"""

    # Enviar al vendedor
    bot.reply_to(message, texto, parse_mode="Markdown")

    # Enviar al grupo de logs
    ID_GRUPO_LOGS = -1002645920112
    bot.send_message(ID_GRUPO_LOGS, texto, parse_mode="Markdown")

@bot.message_handler(commands=['unsub'])
def cmd_unsub(message):
    if not is_admin_or_seller(message.from_user.id):
        bot.reply_to(message, "🚫 No tienes permiso para usar este comando.")
        return

    args = message.text.split()
    if len(args) != 3 or not args[1].isdigit() or not args[2].isdigit():
        bot.reply_to(message, "Uso correcto: /unsub ID_DEL_USUARIO DIAS_A_RESTAR")
        return

    user_id = args[1]
    dias_a_restar = int(args[2])

    dias_restantes_data = cargar_archivo('dias_restantes.json')

    if user_id not in dias_restantes_data:
        dias_restantes_data[user_id] = 0

    dias_restantes_data[user_id] -= dias_a_restar

    if dias_restantes_data[user_id] <= 0:
        dias_restantes_data[user_id] = 0
        plan = "FREE"
    elif dias_restantes_data[user_id] >= 1201:
        plan = "PREMIUM"
    elif dias_restantes_data[user_id] >= 321:
        plan = "STANDARD"
    elif dias_restantes_data[user_id] >= 30:
        plan = "BÁSICO"
    else:
        plan = "FREE"

    guardar_archivo('dias_restantes.json', dias_restantes_data)

    usuarios = cargar_usuarios()
    if user_id in usuarios:
        usuarios[user_id]["plan"] = plan
        guardar_usuarios(usuarios)

    nombre_vendedor = message.from_user.first_name
    id_vendedor = message.from_user.id
    total_dias = dias_restantes_data[user_id]
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")

    texto = f"""
[#AXC_DATA]  

VENDEDOR ➾ [👤 {nombre_vendedor}](tg://user?id={id_vendedor}) - `{id_vendedor}`  
QUITÓ ➾ `{dias_a_restar}` días de membresía  
USUARIO ➾ [👤 Usuario](tg://user?id={user_id}) - `{user_id}`  
PLAN ➾ `{plan}`  
TOTAL ➾ `{total_dias}` días restantes  
FECHA ➾ `{fecha_actual}`
"""

    # Responder al vendedor
    bot.reply_to(message, texto, parse_mode="Markdown")

    # Enviar al grupo de logs
    ID_GRUPO_LOGS = -1002645920112
    bot.send_message(ID_GRUPO_LOGS, texto, parse_mode="Markdown")
        
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
    imagen_url = "https://ibb.co/QWCYbw3"  # URL directa a la imagen

    markup = InlineKeyboardMarkup(row_width=2)
    botones = [
        InlineKeyboardButton("🪪 RENIEC", callback_data="reniec_1"),
        InlineKeyboardButton("👮🏻‍♂️ DELITOS", callback_data="delitos_1"),
        InlineKeyboardButton("⚙️ GENERADOR", callback_data="generador_1"),
        InlineKeyboardButton("☠️ SPAM", callback_data="spam_1"),
        InlineKeyboardButton("💳 BAUCHER", callback_data="baucher_1"),
        InlineKeyboardButton("📞 TELEFONIA", callback_data="telefonos_1"),
        InlineKeyboardButton("🚗 SUNARP", callback_data="sunarp_1"),
        InlineKeyboardButton("👨‍👩‍👧 FAMILIA", callback_data="familia_1"),
        InlineKeyboardButton("🕵️  METADATA COMPLETA", callback_data="seeker_1")
    ]
    markup.add(*botones)
    bot.send_photo(message.chat.id, photo=imagen_url, caption=texto, reply_markup=markup)
    


@bot.message_handler(commands=['me'])
def cmd_me(message):
    usuarios = cargar_usuarios()
    creditos_data = cargar_archivo('creditos.json')
    dias_restantes_data = cargar_archivo('dias_restantes.json')
    sellers = cargar_sellers()
    user_id = str(message.from_user.id)

    args = message.text.split()
    if len(args) == 2 and args[1].isdigit():
        if not is_admin_or_seller(message.from_user.id):
            bot.reply_to(message, "🚫 No tienes permiso para ver la información de otros usuarios.")
            return
        user_id = args[1]

    if user_id not in usuarios:
        bot.reply_to(message, "¡No estás registrado! Usa /register.")
        return

    usuario = usuarios[user_id]
    creditos = creditos_data.get(user_id, 0)
    dias_restantes = dias_restantes_data.get(user_id, 0)

    # Asignar ROL
    if user_id in sellers:
        rol = "👑 SELLER"
    elif dias_restantes > 7 or creditos > 30:
        rol = "CLIENTE"
    else:
        rol = "FREE"

    # PRIORIDAD: días_restantes > créditos
    if dias_restantes >= 31:
        plan = "PREMIUM"
    elif 11 <= dias_restantes <= 30:
        plan = "STANDARD"
    elif 3 <= dias_restantes <= 10:
        plan = "BÁSICO"
    elif dias_restantes == 0:
        # Si no tiene días, usar créditos
        if creditos >= 1201:
            plan = "PREMIUM"
        elif 321 <= creditos <= 1200:
            plan = "STANDARD"
        elif 30 <= creditos <= 320:
            plan = "BÁSICO"
        else:
            plan = "FREE"
    else:
        plan = "FREE"

    # ANTI-SPAM según plan
    if plan == "PREMIUM":
        antispam = "5'"
    elif plan == "STANDARD":
        antispam = "15'"
    else:
        antispam = "60'"

    texto = (
        f"#AXC_BOT💫\n\n"
        f"❰🗒❱ 𝗣𝗘𝗥𝗙𝗜𝗟 𝗗𝗘 ➣ <a href='tg://user?id={user_id}'>{usuario['first_name']}</a>\n"
        f"❰🙎‍♂️❱ 𝗜𝗗 ➣ {user_id}\n"
        f"❰⚡️❱ 𝗨𝗦𝗘𝗥 ➣ @{usuario['username']}\n"
        f"❰🗓❱ 𝗥𝗘𝗚𝗜𝗦𝗧𝗥𝗢 ➣ {usuario['registration_date']}\n\n"
        f"𝐄𝐒𝐓𝐀𝐃𝐎 𝐃𝐄 𝐋𝐀 𝐂𝐔𝐄𝐍𝐓𝐀\n\n"
        f"❰💰❱ 𝗖𝗥𝗘𝗗𝗜𝗧𝗢𝗦 ➣ {creditos} créditos\n"
        f"❰⏳❱ 𝗗𝗜𝗔𝗦 𝗥𝗘𝗦𝗧𝗔𝗡𝗧𝗘𝗦 ➣ {dias_restantes} días\n"
        f"❰📅❱ 𝗥𝗢𝗟 ➣ {rol}\n"
        f"❰📈❱ 𝗣𝗟𝗔𝗡 ➣ {plan}\n"
        f"❰🔎❱ 𝗖𝗢𝗡𝗦𝗨𝗟𝗧𝗔𝗦 ➣ 0\n"
        f"❰📆❱ 𝗛𝗢𝗬 ➣ 0\n"
        f"❰⏱❱ 𝗔𝗡𝗧𝗜-𝗦𝗣𝗔𝗠 ➣ {antispam}\n"
        f"❰💯❱ 𝗘𝗦𝗧𝗔𝗗𝗢 ➣ ACTIVO"
    )

    bot.send_photo(
        message.chat.id,
        photo="https://ibb.co/QWCYbw3",
        caption=texto,
        parse_mode='HTML'
    )

def is_admin_or_seller(user_id):
    admins = [7819787342]  # Reemplaza con tu ID
    sellers = cargar_sellers()
    return user_id in admins or str(user_id) in sellers



# CALLBACKS
@bot.callback_query_handler(func=lambda call: True)
def responder_callback(call):
    data = call.data

    # DICCIONARIO DE PAGINAS POR CATEGORIA
    paginas = {
        "reniec": [
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[🪪] RENIEC ONLINE - FREE\nComando ➾ /dni 44443333\nPrecio ➾ 1 Crédito\nResultado ➾ Foto e información completa en (TEXTO).\n\n[🪪] RENIEC ONLINE - BASICO\nComando ➾ /dnif 44443333\nPrecio ➾ 2 Créditos\nResultado ➾ Foto, Firma e información completa en (TEXTO).\n\n[🪪] RENIEC ONLINE - STANDARD\nComando ➾ /dnit 44443333\nPrecio ➾ 3 Créditos\nResultado ➾ Foto, Firma, Huellas e información completa en (TEXTO).\n\n[🪪] NOMBRES DATABASE - BASICO\nComando ➾ /nmdb N¹|AP¹|AP²\nPrecio ➾ 1 Crédito\nResultado ➾ Filtrador de Nombres en (TEXTO Y TXT).\n\n[📍] DIRECCION ONLINE - STANDARD\nComando ➾ /dir Carrion av1\nPrecio ➾ 2 Créditos\nResultado ➾ Filtrador de Direcciones en (TEXTO).\n\n[📍] DIRECCION ONLINE - STANDARD\nComando ➾ /dir2 44443333\nPrecio ➾ 3 Créditos\nResultado ➾ Filtrador de Direcciones en (TEXTO).\n\n𝗣𝗔́𝗚𝗜𝗡𝗔 𝟭/𝟮",
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\nCATEGORÍA ➾ Reniec\nCOMANDOS ➾ 8 Comandos disponibles\nPÁGINA ➾ 2/2\n\n[🪪] RENIEC DATABASE - BASICO\nComando ➾ /dnidb 44443333\nPrecio ➾ 1 Crédito\nResultado ➾ Foto e información completa en (TEXTO).\n\n[🪪] RENIEC DATABASE - STANDARD\nComando ➾ /dnifdb 44443333\nPrecio ➾ 2 Créditos\nResultado ➾ Foto, Firma e información completa en (TEXTO).\n\n[🪪] RENIEC DATABASE - PREMIUM\nComando ➾ /dnitdb 44443333\nPrecio ➾ 3 Créditos\nResultado ➾ Foto, Firma, Huellas e información completa en (TEXTO).\n\n𝗣𝗔́𝗚𝗜𝗡𝗔 𝟮/𝟮"
        ],
        "delitos": [
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[👮🏻‍♂️] PNP ONLINE CIP - BASICO\nComando ➾ /cip 31288473\nPrecio ➾ 3 Créditos\nResultado ➾ Foto, Firma e información del policía en (TEXTO).\n\n[👮🏻‍♂️] PNP ONLINE DNI - STANDARD\nComando ➾ /pdni 05390731\nPrecio ➾ 3 Créditos\nResultado ➾ Datos del policía en (TEXTO).\n\n[👮🏻‍♂️] PNP SUELDOS CIP - STANDARD\nComando ➾ /ptra 31288473\nPrecio ➾ 5 Créditos\nResultado ➾ Sueldos del policía en (TEXTO).\n\n[👮🏻‍♂️] PNP SUELDOS CIP - PREMIUM\nComando ➾ /ptrapdf 05390731|1|2024\nPrecio ➾ 5 Créditos\nResultado ➾ Ficha de sueldos certificado en (PDF).\n\n𝗣𝗔́𝗚𝗜𝗡𝗔 𝟭/𝟮",
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[👮🏻‍♂️] VERIFICADOR ANT PENALES - STANDARD\nComando ➾ /antpenv 44443333\nPrecio ➾ 2 Créditos\nResultado ➾ Verifica si el documento registra antecedentes penales en (TEXTO).\n\n[👮🏻‍♂️] VERIFICADOR ANT POLICIALES - STANDARD\nComando ➾ /antpolv 44443333\nPrecio ➾ 2 Créditos\nResultado ➾ Verifica si el documento registra antecedentes policiales en (TEXTO).\n\n[👮🏻‍♂️] VERIFICADOR ANT JUDICIALES - STANDARD\nComando ➾ /antjudv 44443333\nPrecio ➾ 2 Créditos\nResultado ➾ Verifica si el documento registra antecedentes judiciales en (TEXTO).\n\n𝗣𝗔́𝗚𝗜𝗡𝗔 𝟮/𝟮"
        ],
        "generador": [
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[🪪] FICHA C4 AZUL - FREE\nComando ➾ /c4 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera una ficha C4 azul en (FOTO).\n\n[🪪] FICHA C4 AZUL - BASICO\nComando ➾ /c4a 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera una ficha C4 azul en (PDF).\n\n[🪪] DNI VIRTUAL - STANDARD\nComando ➾ /dniv 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera copia de DNI azul/amarillo en (FOTO).\n\n[🪪] DNI ELECTRONICO - STANDARD\nComando ➾ /dnivel 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera copia de DNI electrónico en (FOTO).\n\n[🪪] FICHA C4 BLANCO - BASICO\nComando ➾ /c4b 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera una ficha C4 blanco en (FOTO).\n\n[🪪] FICHA C4 BLANCO - STANDARD\nComando ➾ /c4bpdf 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera una ficha C4 blanco en (PDF).\n\n[🪪] FICHA INSCRIPCION - STANDARD\nComando ➾ /c4i 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera una ficha de inscripción en (FOTO).\n\n𝗣𝗔́𝗚𝗜𝗡𝗔 𝟭/𝟮",
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[🪪] FICHA INSCRIPCION - PREMIUM\nComando ➾ /c4ipdf 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera una ficha de inscripción en (PDF).\n\n[🪪] ANTECEDENTE PENALES - STANDARD\nComando ➾ /antpen 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera una ficha antecedentes penales en (FOTO).\n\n[🪪] ANTECEDENTE POLICIALES - STANDARD\nComando ➾ /antpol 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera una ficha antecedentes policiales en (FOTO).\n\n[🪪] ANTECEDENTE JUDICIALES - STANDARD\nComando ➾ /antjud 44443333\nPrecio ➾ 5 Créditos\nResultado ➾ Genera una ficha antecedentes judiciales en (FOTO).\n\n𝗣𝗔́𝗚𝗜𝗡𝗔 𝟮/𝟮"
        ],
        "telefonia": [
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[📞] OSIPTEL ONLINE - PREMIUM\nComando ➾ /telp 44443333\nComando ➾ /telp 999888777\nPrecio ➾ 10 Creditos\nResultado ➾ Devuelve números y titulares desde OSIPTEL en (TEXTO).\n\n[📞] OSIPTEL DATABASE - STANDARD\nComando ➾ /cel 999888777\nPrecio ➾ 5 Creditos\nResultado ➾ Devuelve números y titulares desde OSIPTEL en (TEXTO).\n\n[📞] OSIPTEL DATABASE - STANDARD\nComando ➾ /stel 44443333\nPrecio ➾ 5 Creditos\nResultado ➾ Devuelve números y titulares desde OSIPTEL en (TEXTO).\n\n[📞] CLARO ONLINE - STANDARD\nComando ➾ /claro 999888777\nPrecio ➾ 5 Creditos\nResultado ➾ Devuelve números y titulares desde CLARO en (TEXTO).\n\n[📞] BITEL ONLINE - PREMIUM\nComando ➾ /bitel 999888777\nPrecio ➾ 5 Creditos\nResultado ➾ Devuelve números y titulares desde BITEL en (TEXTO).\n\n[📞] OSIPTEL VERIF - STANDARD\nComando ➾ /osiptelv 44443333\nPrecio ➾ 5 Creditos\nResultado ➾ Devuelve las lineas desde OSIPTEL en (TEXTO).\n\n𝗣𝗔́𝗚𝗜𝗡𝗔 𝟭/𝟮",
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[📞] CLARO DATABASE - STANDARD\nComando ➾ /clarodb 44443333\nComando ➾ /clarodb 999888777\nPrecio ➾ 3 Creditos\nResultado ➾ Devuelve números y titulares desde CLARO en (TEXTO).\n\n[📞] MOVISTAR DATABASE - STANDARD\nComando ➾ /movdb 08345781\nComando ➾ /movdb 999888777\nPrecio ➾ 3 Creditos\nResultado ➾ Devuelve números y titulares desde MOVISTAR en (TEXTO).\n\n[📞] BITEL DATABASE - STANDARD\nComando ➾ /biteldb 999888777\nPrecio ➾ 3 Creditos\nResultado ➾ Devuelve números y titulares desde BITEL en (TEXTO).\n\n𝗣𝗔́𝗚𝗜𝗡𝗔 𝟮/𝟮"
        ],
        "sunarp": [
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[🚗] PLACA ONLINE - BASICO\n\nComando ➾ /vec 44443333\nPrecio ➾ 3 Creditos\nResultado ➾ Obtén información sobre los dueños de la placa en (TEXTO).\n\n[🚗] PLACA ONLINE - BASICO\n\nComando ➾ /pla ABC123\nPrecio ➾ 1 Creditos\nResultado ➾ Obtén información sobre el auto en (FOTO).\n\n[🚗] PLACA ONLINE - STANDARD\n\nComando ➾ /plat ABC123\nPrecio ➾ 3 Creditos\nResultado ➾ Obtén información completa de la placa en (TEXTO).\n\n[🚗] TIVE ONLINE - STANDARD\n\nComando ➾ /tive ABC123\nPrecio ➾ 10 Creditos\nResultado ➾ Obtén tive en (FOTO).\n\n[🚗] TIVE ONLINE - PREMIUM\n\nComando ➾ /tivepdf ABC123\nPrecio ➾ 15 Creditos\nResultado ➾ Obtén tive en (PDF).\n\n[🚗] BOLETA INFORMATIVA - STANDARD\n\nComando ➾ /plab ABC123\nPrecio ➾ 15 Creditos\nResultado ➾ Obtén boleta informativa en (PDF).\n\n📄 𝗣𝗔́𝗚𝗜𝗡𝗔 𝟭/𝟮",
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[🚗] TIVE ETR ONLINE - STANDARD\n\nComando ➾ /tivev ABC123\nPrecio ➾ 5 Creditos\nResultado ➾ Obtén tive eléctrónico ambas caras en (FOTO).\n\n[🚗] TIVE ETR ONLINE - PREMIUM\n\nComando ➾ /tivevpdf ABC123\nPrecio ➾ 10 Creditos\nResultado ➾ Obtén tive eléctrónico ambas caras en (PDF).\n\n📄 𝗣𝗔́𝗚𝗜𝗡𝗔 𝟮/𝟮"
        ],
        "familia": [
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[👨‍👩‍👧] ARBOL GENEALOGICO - STANDARD\n\nComando ➾ /ag 44443333\nPrecio ➾ 5 Creditos\nResultado ➾ Arbol genealogico de familiares en (TEXTO).\n\n[👨‍👩‍👧] ARBOL GENEALOGICO - PREMIUM\n\nComando ➾ /agv 44443333\nPrecio ➾ 10 Creditos\nResultado ➾ Arbol genealogico de familiares en (FOTO).\n\n[👨‍👩‍👧] SISFOH ONLINE - STANDARD\n\nComando ➾ /hogar 44443333\nPrecio ➾ 5 Creditos\nResultado ➾ Integrantes del hogar en tiempo real en (TEXTO).\n\n[👨‍👩‍👧] SISFOH DATABASE - STANDARD\n\nComando ➾ /hogardb 44443333\nPrecio ➾ 3 Creditos\nResultado ➾ Integrantes del hogar DataBase en (TEXTO).\n\n 𝗣𝗔́𝗚𝗜𝗡𝗔 𝟭/𝟭"
        ],
        "spam": [
            "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[☠️] SPM ONLINE - BASICO\n\nComando ➾ /spm 999888777\nPrecio ➾ 3 Creditos\nResultado ➾ Realiza un spm de llamadas (TEXTO).\n\n[☠️] SPM FUENTE 2 - STANDARD\n\nComando ➾ /spmi 999888777\nPrecio ➾ 4 Creditos\nResultado ➾ Realiza un spm de llamadas y whatsapp (TEXTO).\n\n[☠️] SPM FUENTE 3 - STANDARD\n\nComando ➾ /spmm 999888777\nPrecio ➾ 5 Creditos\nResultado ➾ Verifica si el spm de llamadas y whatsapp en (TEXTO).\n\n[☠️] SPM FUENTE 4 - PREMIUM\n\nComando ➾ /spmw 999888777\nPrecio ➾ 10 Creditos\nResultado ➾ Realiza un spm masivo de llamadas en (TEXTO).\n\n 𝗣𝗔́𝗚𝗜𝗡𝗔 𝟭/𝟭"
        ],
        "seeker": [
           "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[🔎] DATA ONLINE - BASICO\n\nComando ➾ /dnis 44443333\nPrecio ➾ 2 Creditos\nResultado ➾ Informacion completa de SEEKER en (TEXTO).\n\n[🔎] TELEFONOS ONLINE - STANDARD\n\nComando ➾ /tels 44443333\nPrecio ➾ 3 Creditos\nResultado ➾ Informacion TELEFONOS de SEEKER en (TEXTO).\n\n[🔎] TRABAJOS ONLINE - STANDARD\n\nComando ➾ /tras 44443333\nPrecio ➾ 3 Creditos\nResultado ➾ Informacion de TRABAJOS de SEEKER en (TEXTO).\n\n[🔎] FAMILIARES ONLINE - STANDARD\n\nComando ➾ /fams 44443333\nPrecio ➾ 3 Creditos\nResultado ➾ Informacion de FAMILIARES de SEEKER en (TEXTO).\n\n[🔎] SEEKER ONLINE - PREMIUM\n\nComando ➾ /seeker 44443333\nPrecio ➾ 10 Creditos\nResultado ➾ Informacion Completa de SEEKER en (TEXTO).\n\n𝗣𝗔́𝗚𝗜𝗡𝗔 𝟭/𝟮",
           "[🔎] SUNAT ONLINE - STANDARD\n\nComando ➾ /sunats 44443333\nPrecio ➾ 3 Creditos\nResultado ➾ Informacion de SUNATS de SEEKER en (TEXTO).\n\n[🔎] CORREO ONLINE - STANDARD\n\nComando ➾ /cors 44443333\nPrecio ➾ 3 Creditos\nResultado ➾ Informacion de CORREOS de SEEKER en (TEXTO).\n\n[🔎] VEHICULOS ONLINE - STANDARD\n\nComando ➾ /vecs 44443333\nPrecio ➾ 3 Creditos\nResultado ➾ Informacion de VEHICULOS de SEEKER en (TEXTO).\n\n[🔎] AFP ONLINE - STANDARD\n\nComando ➾ /afps 44443333\nPrecio ➾ 3 Creditos\nResultado ➾ Informacion de AFP de SEEKER en (TEXTO).\n\n𝗣𝗔́𝗚𝗜𝗡𝗔 𝟮/𝟮"
        ],
        "baucher": [
           "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[💳] PLIN FAKE - BASICO\n\nComando ➾ /plin 10|LUIS PEDRO|1\nPrecio ➾ 1 Creditos\nResultado ➾ Genera un baucher fake en (FOTO).\n\n[💳] INTERBANK FAKE - STANDARD\n\nComando ➾ /ibk 3051234567891|3|10000\nPrecio ➾ 2 Creditos\nResultado ➾ Genera un baucher fake en (FOTO).\n\n[💳] BCP FAKE - STANDARD\n\nComando ➾ /bcp Dominio|3051|8000\nPrecio ➾ 2 Creditos\nResultado ➾ Genera un baucher fake en (FOTO).\n\n𝗣𝗔́𝗚𝗜𝗡𝗔 𝟭/𝟭"
        ],
        "extras": [
           "❰ #AXC_BOT ❱ ➣ 𝗔𝗫𝗖 𝗗𝗔𝗧𝗔\n\n[🌎] META DATA - STANDARD\n\nComando ➾ /meta 00000001\nPrecio ➾ 10 Creditos\nResultado ➾ Informacion completa de METADATA en (TEXTO).\n\n[🎓] SUNEDU ONLINE - STANDARD\n\nComando ➾ /sunedu 00000001\nPrecio ➾ 5 Creditos\nResultado ➾ Informacion brindado por SUNEDU en (TEXTO).\n\n[💼] SUNAT ONLINE - STANDARD\n\nComando ➾ /ruc 20428729201\nComando ➾ /ruc 44443333\nPrecio ➾ 3 Creditos\nResultado ➾ Informacion del ruc en (TEXTO).\n\n[🛠] TRABAJOS SUNAT - STANDARD\n\nComando ➾ /tra 44443333\nPrecio ➾ 3 Creditos\nResultado ➾ Informacion de los trabajos en (TEXTO).\n\n[🛠] SUELDOS SUNAT - STANDARD\n\nComando ➾ /sueld 44443333\nPrecio ➾ 3 Creditos\nResultado ➾ Informacion de los sueldos en (TEXTO).\n\n[✉️] CORREO ELECTRONICO - STANDARD\n\nComando ➾ /cor 44443333\nComando ➾ /cor sano@gmail.com\nPrecio ➾ 3 Creditos\nRespuesta ➾ Busca correos por DNI.\n\n𝗣𝗔́𝗚𝗜𝗡𝗔 𝟭/𝟭"
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
            InlineKeyboardButton("📞 TELEFONIA", callback_data="telefonia_1"),
            InlineKeyboardButton("🚗 SUNARP", callback_data="sunarp_1"),
            InlineKeyboardButton("👨‍👩‍👧 FAMILIA", callback_data="familia_1"),
            InlineKeyboardButton("🕵️  METADATA COMPLETA", callback_data="seeker_1")
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















