import requests
import string
import secrets

class ScrumPay():
    def __init__(self):

        self.url ="https://pay.scrum-technology.com/api/v2test"
        self.username = "acdfvstrzujfcvn_23ujkuu"
        self.password = "awerf_567miopyh674rf"
        self.id_comercio = "es_gtbyhtttd6strz03dgdfg_y45y5re4",

        #self.url = "https://pay.scrum-technology.com/api/v2pro"
        #self.username = "ri&fgt131gdG_eitalj0rks2"
        #self.password = "1t4eeew45a0_ew02_reew542"
        #self.id_comercio = "eef_htt3534oLFO_3dgdfg_y4ere4"
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
            print(str(e))
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
            print(e)
            return {"success": False, "error": str(e)}



    def generar_codigo_unico(self):
        caracteres = string.ascii_letters + string.digits  # Usar letras y dígitos
        longitud = 10
        codigo_unico = ''.join(secrets.choice(caracteres) for _ in range(longitud))
        return codigo_unico
