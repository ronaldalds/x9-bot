from Src.Api.api_avin import APIavin
from collections import Counter
from datetime import datetime, timedelta

def x9(data: datetime, ciclo: int):
    print(f"Iniciando verificação: {data.strftime('%d/%m/%Y %H:%M:%S')}")
    avin = APIavin()
    duracao = timedelta(minutes=ciclo)
    ajuste_gmt = timedelta(hours=3)
    data_inicial = (data - duracao)
    data_final = data
    dados = avin.alerts_period(inicial=int(data_inicial.timestamp()), final=int(data_final.timestamp()))

    if dados:
        contador = Counter(d['veiculo'] for d in dados)
        res = []
        for veiculo in contador:
            resultado = list(filter(lambda d: d['veiculo'] == veiculo, dados))
            txt = '🚧🚨 VELOCIDADE MÁXIMA EXCEDIDA 🚨🚧\n\n'
            txt += f'{veiculo}\n\n'
            for ocorrencia in resultado:
                data_ocorrencia = datetime.strptime(ocorrencia['data'], "%d/%m/%Y %H:%M:%S")
                data_ocorrencia = data_ocorrencia - ajuste_gmt
                data_ocorrencia = data_ocorrencia.strftime("%d/%m/%Y %H:%M")
                txt += f"{data_ocorrencia}<>{ocorrencia['velocidade']} Km/h\n"

            res.append(txt)
        return res
