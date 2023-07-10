import requests
from parceiros.requests_proxy import post_request, get_request
from datetime import datetime, timedelta
from typing import List

from credito.config import settings

class ParceirosAPI:
    
    BASE_URL = "https://f0e60216-6218-46d2-ae59-a5c0ea8102fa.mock.pstmn.io"
    ENDPOINT_AUTENTICAR = "/autenticar"
    ENDPOINT_OFERTAS = "/ofertas"

    HEADERS = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
    }
    
    ACCESS_TOKEN = None
    EXPIRES_AT = None

    @classmethod
    def obter_access_token(cls):
        """
        Obter access token

        :return token
        """

        try:
            url = f'{cls.BASE_URL}{cls.ENDPOINT_AUTENTICAR}'
            data = {
                'client_id': settings.security.client_id,
                'client_secret': settings.security.client_secret
            }
            response = post_request(url, data=data, headers=cls.HEADERS)
            response = response.json()

            cls.ACCESS_TOKEN = response['access_token']
            expires_in = response['expires_in']
            cls.EXPIRES_AT = datetime.now() + timedelta(seconds=expires_in)
        except requests.exceptions.RequestException :
            raise Exception('Falha ao obter access token')

    @classmethod
    def obter_ofertas(cls, parcelas:int, valor:float) -> List[dict]:
        """
        Obter ofertas de créditos dos parceiros

        :return ofertas
        """
        try:
            if cls.ACCESS_TOKEN is None or datetime.now() >= cls.EXPIRES_AT:
                cls.obter_access_token()

            url = f'{cls.BASE_URL}{cls.ENDPOINT_OFERTAS}'
            headers = {'Authorization': f'Bearer {cls.ACCESS_TOKEN}', **cls.HEADERS}
            params = {'installments': parcelas, 'value': valor}

            response = get_request(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                return data
        except Exception:
            raise Exception('Falha ao consultar ofertas de créditos')

