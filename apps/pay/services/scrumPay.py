import requests

class ScrumPay():
    def __init__(self):
        #credenciales de tests
        # self.url ="https://pay.scrum-technology.com/api/v2tests"
        # self.username = "acdfvstrzujfcvn_23ujkuu"
        # self.password = "awerf_567miopyh674rf"
        # self.id_comercio = "es_gtbyhtttd6strz03dgdfg_y45y5re4"

        #credenciales de prod
        self.url = "https://pay.scrum-technology.com/api/v2pro"
        self.username = "ri&fgt131gdG_eitalj0rks2"
        self.password = "1t4eeew45a0_ew02_reew542"
        self.id_comercio = "eef_htt3534oLFO_3dgdfg_y4ere4"
    #/consulta_transaccion.php
    #solicitud_pago.php

    def solicitudPago(self, data):
        url = self.url + "/solicitud_pago.php"
        data["id_comercio"] = self.id_comercio
        try:
            response = requests.post(url,json=data,auth=(self.username, self.password))
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception("error al hacer la solicitud con la pasarela" ) 
        except Exception as e:
            raise Exception("error al hacer la solicitud con la pasarela" ) 
        
    def consultaDePago(self, id_transaccion):
        url = self.url + "/consulta_transaccion.php"
        data = {
            "id_transaccion" : id_transaccion,
            "id_comercio" : self.id_comercio
        }
        
        try:
            response = requests.post(url,json=data,auth=(self.username, self.password))

            if response.status_code == 200:
                return response.json()
            else:
                return {"success": False, "error": "error al hacer la solicitud con la pasarela", "codigo de error": response.status_code}
        except Exception as e:
            return {"success": False, "error": str(e)}




