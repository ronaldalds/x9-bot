from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv
import os
from Src.Middleware.authentication import authorization
from Src.Controller.x9_controller import handle_start_x9, handle_stop_x9, handle_status_x9


load_dotenv()

version = "0.0.4"

app = Client(
    name=os.getenv("BOT_NAME_TELEGRAM"), 
    api_hash=os.getenv("API_HASH_TELEGRAM"),
    api_id=os.getenv("API_ID_TELEGRAM"),
    bot_token=os.getenv("BOT_TOKEN_TELEGRAM")
    )

chat_adm = [
    os.getenv("CHAT_ID_ADM"),
]

@app.on_message(filters.command("start"))
def start(client, message: Message):
    message.reply_text(f"""
/logistica - Setor Logistica
/chat - Para informa seu chat_id
""")

@app.on_message(filters.command("logistica"))
@authorization(chat_adm)
def financeiro(client, message: Message):
    message.reply_text(f"""
/iniciar_x9 - Iniciar x9
/parar_x9 - Parar x9
/status_x9 - Status x9
""")

@app.on_message(filters.command("chatgroup"))
@authorization(chat_adm)
def handle_chatgroup_id(client: Client, message: Message):
    client.send_message(chat_adm[0], message)

@app.on_message(filters.command("chat"))
def handle_chat_id(client: Client, message: Message):
    text = f"{message.chat.first_name}.{message.chat.last_name} - ID:{message.from_user.id}"
    client.send_message(message.from_user.id, text)
    print(text)

# iniciar x9
@app.on_message(filters.command("iniciar_x9"))
@authorization(chat_adm)
def iniciar_x9(client: Client, message: Message):
    handle_start_x9(client, message)

# parar x9
@app.on_message(filters.command("parar_x9"))
@authorization(chat_adm)
def parar_x9(client: Client, message: Message):
    handle_stop_x9(client, message)

# status x9
@app.on_message(filters.command("status_x9"))
@authorization(chat_adm)
def status_x9(client: Client, message: Message):
    handle_status_x9(client, message)

# stop service
@app.on_message(filters.command("stop_service"))
@authorization(chat_adm)
def stop(client: Client, message: Message):
    print("Service Stopping")
    app.stop()

print("Service Telegram Up!")
print(f"Version {version}")
app.run()

