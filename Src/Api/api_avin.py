import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

class APIavin:
    def __init__(self):
        self._headers = {
            'apikey': os.getenv('APIKEY'),
            'secretkey': os.getenv('SECRETKEY')
        }
        self._velocidade = int(os.getenv('VELOCIDADE'))
        self._type_alert = os.getenv('TYPE_ALERT')

    def alerts_period(self, inicial, final):
        try:
            response = requests.get(f"https://ws.fulltrack2.com/alerts/period/initial/{inicial}/final/{final}", headers=self._headers)
            if response.status_code == 200:
                data = response.json()
                try:
                    for ocorrencia in data['data']:
                        if ocorrencia['ras_eal_id_alerta_tipo'] == self._type_alert:
                            alerts = self.veiculo_id(ocorrencia['ras_eal_id_veiculo'], inicial, final)
                    return alerts
                except:
                    return False
            else:
                raise Exception(f'Error ao obeter alerts API {response.status_code}')
        except requests.exceptions.ConnectionError:
            time.sleep(5)
            self.alerts_period(inicial, final)

    def veiculo_id(self, id, inicial, final):
        try:
            response = requests.get(f"https://ws.fulltrack2.com/events/interval/id/{id}/begin/{inicial}/end/{final}", headers=self._headers)
            if response.status_code == 200:
                data = response.json()
                alerts_velocidade = []
                for alert in data['data']:
                    velocidade = alert['ras_eve_velocidade']
                    if int(velocidade) >= self._velocidade:
                        ocorrencia = {}
                        ocorrencia['veiculo'] = f"{alert['ras_vei_veiculo']} - {alert['ras_vei_placa']}"
                        ocorrencia['data'] = alert['ras_eve_data_gps']
                        ocorrencia['velocidade'] = alert['ras_eve_velocidade']
                        alerts_velocidade.append(ocorrencia)
                return alerts_velocidade
            
            else:
                raise Exception(f'Error ao obeter veiculo API {response.status_code}')
        except requests.exceptions.ConnectionError:
            time.sleep(5)
            self.veiculo_id(id, inicial, final)