from pyrogram import Client
from pyrogram.types import Message
from threading import Thread
from Src.Service.x9_service import x9
from dotenv import load_dotenv
from datetime import datetime
from queue import Queue
from time import sleep
import os
import schedule

load_dotenv()

resultado_x9 = Queue()
running = False
tempo_ciclo = int(os.getenv('TIME_CLICO'))
grupo_transport = int(os.getenv('CHAT_ID_GROUP_TRANSPORT'))

def chamada():
    # variavel de comunicação de todas as funções para parar o processo quando for necessário
    global running

    # variavel com o momento que for chamado a função
    # data = datetime(day=8, month=7, year=2023, hour=00, minute=00)
    data = datetime.now()

    print(f"iniciando verificação: {data}")

    # executa a pesquisa na api
    res = x9(data, tempo_ciclo)

    # se tiver algum alerta ele grava na fila
    if running and res:
        resultado_x9.put(res)

def agendar_funcao():
    Thread(target=chamada).start()

def handle_start_x9(client: Client, message: Message):
    global running
    if not running:
        running = True
        message.reply_text("X9 em execução.")
        print(f"X9 em execução: {datetime.now()}")

        # cria um agendamento para repetir com o tempo_cilco em minutos
        job_x9 = schedule.every(tempo_ciclo).minutes.do(agendar_funcao)

        while running:
            schedule.run_pending()
            sleep(1)
            # verifica se existe ocorrência
            if not resultado_x9.empty():
                ocorrencias = resultado_x9.get()
                for ocorrencia in ocorrencias:
                    # enviar ocorrências
                    client.send_message(grupo_transport, ocorrencia)

            # Verifica se a execução deve continuar ou parar
            if not running:
                # limpa a fila de resultados
                while not resultado_x9.empty():
                    resultado_x9.get()
                
                schedule.cancel_job(job_x9)
                message.reply_text("X9 parado.")
                break
    else:
        message.reply_text("X9 em execução.")

def handle_stop_x9(client: Client, message: Message):
    global running
    running = False
    message.reply_text("Pedido de parada do X9 iniciado...")
    
def handle_status_x9(client: Client, message: Message):
    global running
    try:
        if running:
            message.reply_text("X9 em execução")
        else:
            message.reply_text("X9 parado")
    except:
        message.reply_text("X9 parado")