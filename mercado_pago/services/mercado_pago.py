import requests
from conf_fire_base import MERCADOPAGO_SECRET_KEY, REGION_ACTUAL

class MercadoPagoService():
    def __init__(self):

        self.url = "https://api.mercadopago.com"
        self.sk = MERCADOPAGO_SECRET_KEY
        self.headers = {
            "Authorization": "Bearer " + self.sk,
            "Content-Type": "application/json"
        }

    def get_payment(self, id):
        url = self.url + "/v1/payments/" + str(id)
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception("error al conectar con mercado pago" ) 
        except Exception as e:
            raise Exception("error al conectar con mercado pago" ) 
        




