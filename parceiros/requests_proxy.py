
import requests
from requests import exceptions as requests_exceptions
from ratelimit import limits, sleep_and_retry
from backoff import on_exception, expo

MAX_CALLS_PER_MINUTE = 120
PERIOD = 60
MAX_RETRIES = 15

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=PERIOD)
def check_rate_limit():
    """
    Função auxiliar utilizada para verificar o limite global de
    requisições para API de Parceiros.
    """
    pass

@on_exception(expo, requests_exceptions.ConnectionError, max_tries=MAX_RETRIES)
def post_request(url=None, **kwargs):
    check_rate_limit()
    return requests.post(url, **kwargs)

@on_exception(expo, requests_exceptions.ConnectionError, max_tries=MAX_RETRIES)
def get_request(url=None, **kwargs):
    check_rate_limit()
    return requests.get(url, **kwargs)
