from pyrogram import Client
from pyrogram.types import Message
from Src.Service.x9_service import x9
from dotenv import load_dotenv
from datetime import datetime, timedelta
from queue import Queue
from time import sleep
import os

load_dotenv()

resultado_x9 = Queue()
running = False
tempo_ciclo = int(os.getenv('TIME_CLICO'))
grupo_transport = int(os.getenv('CHAT_ID_GROUP_TRANSPORT'))

def handle_start_x9(client: Client, message: Message):
    global running
    if not running:
        running = True
        data = datetime.now()
        message.reply_text("X9 em execução.")
        print(f"X9 em execução: {data}- {data.timestamp()}")

        while running:
            sleep(1)
            if datetime.now().strftime("%d/%m/%Y %H:%M") == ((data + timedelta(minutes=tempo_ciclo)).strftime("%d/%m/%Y %H:%M")):
                data = datetime.now()
                res = x9(data, tempo_ciclo)
                if res:
                    for ocorrencia in res:
                        print(ocorrencia)
                        # enviar ocorrências
                        client.send_message(grupo_transport, ocorrencia)

            # Verifica se a execução deve continuar ou parar
            if not running:
                message.reply_text("X9 parado.")
                break
    else:
        message.reply_text("X9 em execução.")

def handle_stop_x9(client: Client, message: Message):
    global running
    if running:
        running = False
        message.reply_text("Pedido de parada do X9 iniciado...")
    else:
        message.reply_text("Cancelamento parado")
        
def handle_status_x9(client: Client, message: Message):
    global running
    try:
        if running:
            message.reply_text("X9 em execução")
        else:
            message.reply_text("X9 parado")
    except:
        message.reply_text("X9 parado")