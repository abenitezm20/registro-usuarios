import os
import logging
import requests
from functools import wraps
from flask import request

from src.errors.errors import ApiError, TokenNotFound, Unauthorized

HEADER_NAME = 'Authorization'
URL_AUTORIZADOR = os.getenv(
    'URL_AUTORIZADOR', 'http://127.0.0.1:3000/autorizador')
URL_VALIDAR_TOKEN = URL_AUTORIZADOR + '/seguridad/validar-token'
URL_GENERAR_TOKEN = URL_AUTORIZADOR + '/seguridad/generar-token'


logger = logging.getLogger(__name__)


def token_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        token_bearer = request.headers.get(HEADER_NAME)
        logger.info(f'Validando token {token_bearer}')

        if token_bearer is None:
            raise TokenNotFound

        email = None
        token = token_bearer.split(' ')[1]
        logger.info(f'URL {URL_VALIDAR_TOKEN}')

        try:
            response = requests.post(
                url=URL_VALIDAR_TOKEN, json={"token": token})

            if response.status_code == 200:
                data = response.json()

                if data['token_valido'] is False:
                    logger.error('Token invalido')
                    raise Unauthorized

                logger.info('Token valido')
                email = data['email']
            else:
                logger.error('Token invalido')
                raise Unauthorized

        except Exception as e:
            logging.error(f'Error validando token con el autorizador {e}')
            raise Unauthorized

        return func(email, *args, **kwargs)
    return wrapper


def get_token(email: str):
    logger.info(f'Obteniendo token para {email}')
    try:
        response = requests.post(
            url=URL_GENERAR_TOKEN, json={"email": email})

        if response.status_code == 200:
            data = response.json()

            if data['token'] is None:
                logger.error('Token invalido')
                raise ApiError

            return data['token']
        else:
            logger.error('Credenciales invalidas')
            raise Unauthorized

    except Exception as e:
        logger.error(f'Error obteniendo token con el autorizador {e}')
        raise ApiError
